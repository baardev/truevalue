#!/usr/bin/env python3
"""
THOLONIC TRAINING EXPERIMENTS — FULL SCALE
WikiText-103 dataset, GPT-2-small-scale architecture, checkpointed for restarts.

Row 2: Convergence speed — baseline vs. tholonic balance regularizer.
       12-layer d=768 model on WikiText-103. 3 seeds × 2 conditions.
       Pass criterion: tholonic reaches each target loss in fewer steps
       for ≥ 2/3 seed pairs, p < 0.05 paired t-test.

Row 3: Optimal depth — empirical best depth vs. log_φ(H₀/H_L).
       Fixed-width (d=512, h=8) models at depths 2, 4, 6, 8, 12, 16, 24.
       Pass criterion: predicted depth within ±2 layers of empirical optimum.

Checkpointing:
  - A .pt checkpoint is saved every CHECKPOINT_EVERY steps for every run.
  - A human-readable training_status.json tracks which runs are done.
  - On restart, completed runs are skipped and in-progress runs resume
    from their last checkpoint, including full RNG state.

Usage:
  python3 train_experiments_full.py          # run everything
  python3 train_experiments_full.py --row2   # row 2 only
  python3 train_experiments_full.py --row3   # row 3 only
  python3 train_experiments_full.py --status # print status and exit

Dependencies:
  pip install datasets transformers torch
"""

import argparse, math, json, time
import torch, torch.nn as nn, torch.nn.functional as F
import numpy as np
from pathlib import Path

# ── dataset import ────────────────────────────────────────────────────────────
try:
    from datasets import load_dataset
    HAS_DATASETS = True
except ImportError:
    HAS_DATASETS = False

from transformers import GPT2TokenizerFast

# ── constants ─────────────────────────────────────────────────────────────────
PHI    = (1 + math.sqrt(5)) / 2
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

VOCAB_SIZE = 50257          # GPT-2 vocab

# Row 2 model: GPT-2 small scale
ROW2_D      = 768
ROW2_HEADS  = 12
ROW2_LAYERS = 12
ROW2_STEPS  = 10_000
ROW2_SEEDS  = [42, 7, 13]

# Row 3 model: fixed-width, variable depth
ROW3_D      = 512
ROW3_HEADS  = 8
DEPTHS      = [2, 4, 6, 8, 12, 16, 24]
ROW3_STEPS  = 15_000

SEQ_LEN          = 256      # 512 → OOM on 12GB; attention is O(T²)
BATCH            = 4        # micro-batch per step
GRAD_ACCUM       = 4        # accumulate 4 steps → effective batch = 16
LAMBDA_REG       = 0.01
LEARNING_RATE    = 3e-4
WEIGHT_DECAY     = 0.1
GRAD_CLIP        = 1.0
EVAL_EVERY       = 200
CHECKPOINT_EVERY = 500
EVAL_BATCHES     = 50       # number of batches for each val-loss estimate
TARGET_LOSSES    = [4.5, 4.0, 3.7]

# Mixed-precision scaler (no-op on CPU)
_SCALER = torch.amp.GradScaler("cuda", enabled=torch.cuda.is_available())

# Paths
SCRIPT_DIR     = Path(__file__).parent
BASE_DIR       = SCRIPT_DIR.parent
OUT_DIR        = BASE_DIR / "results"
CKPT_DIR       = BASE_DIR / "checkpoints"
STATUS_FILE    = OUT_DIR / "training_status.json"
RESULTS_FILE   = OUT_DIR / "training_experiments_full.json"
DATA_CACHE     = OUT_DIR / "wikitext103_tokens.pt"

OUT_DIR.mkdir(parents=True, exist_ok=True)
CKPT_DIR.mkdir(parents=True, exist_ok=True)

# ── data ──────────────────────────────────────────────────────────────────────
def load_data():
    """Download, tokenise, and cache WikiText-103 token IDs."""
    if DATA_CACHE.exists():
        print(f"  Loading cached tokens from {DATA_CACHE} ...", flush=True)
        d = torch.load(DATA_CACHE, weights_only=True)
        print(f"  Train: {len(d['train']):,}  Val: {len(d['val']):,} tokens", flush=True)
        return d["train"], d["val"]

    if not HAS_DATASETS:
        raise ImportError(
            "Install the 'datasets' library: pip install datasets"
        )

    print("  Downloading WikiText-103 ...", flush=True)
    ds  = load_dataset("wikitext", "wikitext-103-raw-v1")
    tok = GPT2TokenizerFast.from_pretrained("gpt2")

    def tokenise(split):
        texts = [t for t in ds[split]["text"] if t.strip()]
        joined = tok.eos_token.join(texts)
        return torch.tensor(tok.encode(joined), dtype=torch.long)

    train_ids = tokenise("train")
    val_ids   = tokenise("validation")
    torch.save({"train": train_ids, "val": val_ids}, DATA_CACHE)
    print(f"  Cached to {DATA_CACHE}", flush=True)
    print(f"  Train: {len(train_ids):,}  Val: {len(val_ids):,} tokens", flush=True)
    return train_ids, val_ids


def get_batch(ids, rng, pos_ref, batch=BATCH, seq=SEQ_LEN):
    """
    Draw a batch by advancing pos_ref[0] linearly through ids.
    Wraps around when the end is reached. Returns (x, y) on DEVICE.
    """
    n = len(ids) - seq - 1
    starts = []
    for _ in range(batch):
        starts.append(pos_ref[0] % n)
        pos_ref[0] = (pos_ref[0] + seq) % n
    x = torch.stack([ids[s : s + seq]     for s in starts]).to(DEVICE)
    y = torch.stack([ids[s + 1 : s + seq + 1] for s in starts]).to(DEVICE)
    return x, y


# ── model ─────────────────────────────────────────────────────────────────────
class CausalMHA(nn.Module):
    def __init__(self, d, h):
        super().__init__()
        self.h, self.dh = h, d // h
        self.qkv      = nn.Linear(d, 3 * d, bias=False)
        self.out_proj = nn.Linear(d, d,     bias=False)

    def forward(self, x):
        B, T, C = x.shape
        q, k, v = self.qkv(x).split(C, -1)
        def sp(t): return t.reshape(B, T, self.h, self.dh).transpose(1, 2)
        q, k, v = sp(q), sp(k), sp(v)
        mask = torch.triu(torch.full((T, T), float("-inf"), device=x.device), 1)
        attn = F.softmax(q @ k.transpose(-2, -1) / math.sqrt(self.dh) + mask, -1)
        return self.out_proj((attn @ v).transpose(1, 2).reshape(B, T, C))


class MLP(nn.Module):
    def __init__(self, d):
        super().__init__()
        self.fc1    = nn.Linear(d, 4 * d, bias=False)
        self.c_proj = nn.Linear(4 * d, d, bias=False)

    def forward(self, x):
        return self.c_proj(F.gelu(self.fc1(x)))


class Block(nn.Module):
    def __init__(self, d, h):
        super().__init__()
        self.ln_1 = nn.LayerNorm(d)
        self.attn = CausalMHA(d, h)
        self.ln_2 = nn.LayerNorm(d)
        self.mlp  = MLP(d)

    def forward(self, x):
        x = x + self.attn(self.ln_1(x))
        x = x + self.mlp(self.ln_2(x))
        return x


class GPTModel(nn.Module):
    def __init__(self, vocab, d, n_layers, n_heads, seq=SEQ_LEN):
        super().__init__()
        self.wte    = nn.Embedding(vocab, d)
        self.wpe    = nn.Embedding(seq, d)
        self.blocks = nn.ModuleList([Block(d, n_heads) for _ in range(n_layers)])
        self.ln_f   = nn.LayerNorm(d)
        self.head   = nn.Linear(d, vocab, bias=False)
        self.head.weight = self.wte.weight   # weight tying

    def forward(self, x):
        B, T = x.shape
        h = self.wte(x) + self.wpe(torch.arange(T, device=x.device))
        for blk in self.blocks:
            h = blk(h)
        return self.head(self.ln_f(h))

    @torch.no_grad()
    def hidden_states(self, x):
        B, T = x.shape
        h = self.wte(x) + self.wpe(torch.arange(T, device=x.device))
        h0 = h.clone()
        for blk in self.blocks:
            h = blk(h)
        return h0, self.ln_f(h)


# ── tholonic regulariser ──────────────────────────────────────────────────────
class TholonicReg:
    def __init__(self, model, lam=LAMBDA_REG):
        self.lam    = lam
        self.d_vals = []
        self.c_vals = []
        self.hooks  = []
        for blk in model.blocks:
            for ln in (blk.ln_1, blk.ln_2):
                def dh(m, inp, out, s=self.d_vals):
                    s.append(out.pow(2).mean().sqrt())
                self.hooks.append(ln.register_forward_hook(dh))
            for proj in (blk.attn.out_proj, blk.mlp.c_proj):
                def ch(m, inp, out, s=self.c_vals):
                    s.append(out.pow(2).mean().sqrt())
                self.hooks.append(proj.register_forward_hook(ch))

    def loss(self):
        n = min(len(self.d_vals), len(self.c_vals))
        if n == 0:
            return torch.tensor(0.0, device=DEVICE)
        return self.lam * sum(
            (self.d_vals[i] - 0.5 * self.c_vals[i]) ** 2 for i in range(n)
        ) / n

    def reset(self):
        self.d_vals.clear()
        self.c_vals.clear()

    def remove(self):
        for h in self.hooks:
            h.remove()


# ── checkpointing ─────────────────────────────────────────────────────────────
def ckpt_path(run_id):
    return CKPT_DIR / f"{run_id}.pt"


def save_checkpoint(run_id, step, model, optimizer, pos, log):
    torch.save({
        "step":      step,
        "model":     model.state_dict(),
        "optimizer": optimizer.state_dict(),
        "pos":       pos,
        "rng_cpu":   torch.get_rng_state(),
        "rng_cuda":  torch.cuda.get_rng_state() if torch.cuda.is_available() else None,
        "rng_numpy": np.random.get_state(),
        "log":       log,
    }, ckpt_path(run_id))


def load_checkpoint(run_id, model, optimizer):
    """Returns (resume_step, pos, log). Returns (0, 0, {}) if no checkpoint."""
    p = ckpt_path(run_id)
    if not p.exists():
        return 0, 0, {}
    ckpt = torch.load(p, map_location=DEVICE)
    model.load_state_dict(ckpt["model"])
    optimizer.load_state_dict(ckpt["optimizer"])
    torch.set_rng_state(ckpt["rng_cpu"].cpu())
    if ckpt["rng_cuda"] is not None and torch.cuda.is_available():
        torch.cuda.set_rng_state(ckpt["rng_cuda"])
    np.random.set_state(ckpt["rng_numpy"])
    print(f"    Resumed from step {ckpt['step']}", flush=True)
    return ckpt["step"], ckpt["pos"], ckpt["log"]


# ── status file ───────────────────────────────────────────────────────────────
def load_status():
    if STATUS_FILE.exists():
        with open(STATUS_FILE) as f:
            return json.load(f)
    return {}


def save_status(status):
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f, indent=2)


def print_status():
    status = load_status()
    if not status:
        print("  No runs started yet.")
        return
    print(f"\n  {'Run':<30}  {'Status':<12}  {'Step':>6}  Notes")
    print(f"  {'-'*65}")
    for run_id, info in sorted(status.items()):
        step  = info.get("last_step", 0)
        total = info.get("total_steps", "?")
        state = info.get("status", "unknown")
        notes = info.get("notes", "")
        print(f"  {run_id:<30}  {state:<12}  {step:>5}/{total}  {notes}")


# ── helpers ───────────────────────────────────────────────────────────────────
@torch.no_grad()
def eval_loss(model, val_ids, n=EVAL_BATCHES):
    model.eval()
    pos = [0]
    losses = []
    autocast_ctx = torch.amp.autocast("cuda") if torch.cuda.is_available() \
                   else torch.amp.autocast("cpu", enabled=False)
    for _ in range(n):
        x, y = get_batch(val_ids, None, pos)
        with autocast_ctx:
            logits = model(x)
            losses.append(
                F.cross_entropy(logits.reshape(-1, VOCAB_SIZE), y.reshape(-1)).item()
            )
    model.train()
    return float(np.mean(losses))


def eff_rank(mat):
    try:
        sv = torch.linalg.svdvals(mat.float())
        sv = sv[sv > 1e-10]
        p  = sv ** 2 / (sv ** 2).sum()
        return math.exp(-(p * torch.log(p + 1e-12)).sum().item())
    except Exception:
        return float("nan")


@torch.no_grad()
def measure_h0_hl(model, val_ids, n=30):
    pos = [0]
    model.eval()
    h0s, hls = [], []
    for _ in range(n):
        x, _ = get_batch(val_ids, None, pos, batch=1)
        h0, hl = model.hidden_states(x)
        h0s.append(eff_rank(h0.squeeze(0)))
        hls.append(eff_rank(hl.squeeze(0)))
    model.train()
    return float(np.nanmean(h0s)), float(np.nanmean(hls))


# ── training ──────────────────────────────────────────────────────────────────
def train_one(run_id, n_layers, d_model, n_heads, steps,
              condition, seed, train_ids, val_ids,
              total_steps=None, verbose=True):
    """
    Train one run with full checkpoint/resume support.
    Returns the completed log dict.
    """
    total_steps = total_steps or steps
    status      = load_status()

    # Skip if already complete
    if status.get(run_id, {}).get("status") == "complete":
        print(f"    [{run_id}] already complete — skipping.", flush=True)
        p = ckpt_path(run_id)
        if p.exists():
            ckpt = torch.load(p, map_location=DEVICE)
            return ckpt["log"]
        return {}

    torch.manual_seed(seed)
    np.random.seed(seed)

    model = GPTModel(VOCAB_SIZE, d_model, n_layers, n_heads).to(DEVICE)
    optim = torch.optim.AdamW(
        model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY
    )
    reg = TholonicReg(model) if condition == "tholonic" else None

    resume_step, pos, log = load_checkpoint(run_id, model, optim)

    if not log:
        log = {
            "condition": condition, "n_layers": n_layers, "seed": seed,
            "steps": [], "val_loss": [], "steps_to_target": {},
        }

    # Update status to in-progress
    status[run_id] = {
        "status":      "in_progress",
        "last_step":   resume_step,
        "total_steps": total_steps,
        "condition":   condition,
        "seed":        seed,
        "notes":       "",
    }
    save_status(status)

    reached  = {t: log["steps_to_target"].get(str(t)) for t in TARGET_LOSSES}
    pos_ref  = [pos]
    t0       = time.time()

    autocast_ctx = torch.amp.autocast("cuda") if torch.cuda.is_available() \
                   else torch.amp.autocast("cpu", enabled=False)

    for step in range(resume_step + 1, steps + 1):
        # Gradient accumulation: accumulate GRAD_ACCUM micro-batches per step
        optim.zero_grad()
        accum_loss = 0.0
        for _ in range(GRAD_ACCUM):
            x, y = get_batch(train_ids, None, pos_ref)
            with autocast_ctx:
                logits    = model(x)
                task_loss = F.cross_entropy(
                    logits.reshape(-1, VOCAB_SIZE), y.reshape(-1)
                ) / GRAD_ACCUM
                total = task_loss + (reg.loss() / GRAD_ACCUM if reg else 0.0)
            if reg:
                reg.reset()
            _SCALER.scale(total).backward()
            accum_loss += total.item()

        _SCALER.unscale_(optim)
        torch.nn.utils.clip_grad_norm_(model.parameters(), GRAD_CLIP)
        _SCALER.step(optim)
        _SCALER.update()

        if step % EVAL_EVERY == 0 or step == steps:
            vl = eval_loss(model, val_ids)
            log["steps"].append(step)
            log["val_loss"].append(vl)
            for t in TARGET_LOSSES:
                if reached[t] is None and vl <= t:
                    reached[t] = step
                    log["steps_to_target"][str(t)] = step
            if verbose:
                elapsed = time.time() - t0
                eta     = elapsed / (step - resume_step) * (steps - step)
                print(f"    [{run_id}] step {step:>6}/{steps}"
                      f"  val={vl:.4f}"
                      f"  elapsed={elapsed/60:.1f}m  eta={eta/60:.1f}m",
                      flush=True)

        if step % CHECKPOINT_EVERY == 0 or step == steps:
            # Set final_val_loss before saving so it is present in the checkpoint
            log["final_val_loss"] = log["val_loss"][-1] if log["val_loss"] else float("nan")
            save_checkpoint(run_id, step, model, optim, pos_ref[0], log)
            status[run_id]["last_step"] = step
            save_status(status)
    if reg:
        reg.remove()

    # Mark complete
    status[run_id]["status"]    = "complete"
    status[run_id]["last_step"] = steps
    save_status(status)

    return log, model


# ══════════════════════════════════════════════════════════════════════════════
#  ROW 2 — CONVERGENCE SPEED
# ══════════════════════════════════════════════════════════════════════════════
def run_row2(train_ids, val_ids):
    print()
    print("=" * 68)
    print("  ROW 2 — CONVERGENCE SPEED")
    n_params = (
        VOCAB_SIZE * ROW2_D +                    # embedding
        SEQ_LEN * ROW2_D +                       # positional
        ROW2_LAYERS * (12 * ROW2_D**2) +         # attn + mlp (approx)
        ROW2_LAYERS * 4 * ROW2_D                 # layer norms
    )
    print(f"  Model: {ROW2_LAYERS}L d={ROW2_D} h={ROW2_HEADS}"
          f"  (~{n_params/1e6:.0f}M params)")
    print(f"  Steps: {ROW2_STEPS}  Seeds: {ROW2_SEEDS}  λ={LAMBDA_REG}")
    print(f"  Device: {DEVICE}")
    print("=" * 68)

    all_logs = {"baseline": [], "tholonic": []}

    for seed in ROW2_SEEDS:
        for cond in ("baseline", "tholonic"):
            run_id = f"row2_{cond}_seed{seed}"
            print(f"\n  Training [{run_id}] ...", flush=True)
            result = train_one(
                run_id, ROW2_LAYERS, ROW2_D, ROW2_HEADS,
                ROW2_STEPS, cond, seed, train_ids, val_ids,
            )
            log = result[0] if isinstance(result, tuple) else result
            all_logs[cond].append(log)

    # Aggregate
    def agg(logs):
        vals  = [l.get("final_val_loss", float("nan")) for l in logs if l]
        vals  = [v for v in vals if not math.isnan(v)]
        mean  = float(np.mean(vals))  if vals else float("nan")
        std   = float(np.std(vals))   if vals else float("nan")
        steps_to = {}
        for t in TARGET_LOSSES:
            vs = [l.get("steps_to_target", {}).get(str(t)) for l in logs if l]
            vs = [v for v in vs if v is not None]
            steps_to[str(t)] = int(np.mean(vs)) if vs else None
        return mean, std, steps_to

    bl_mean, bl_std, bl_sts = agg(all_logs["baseline"])
    tl_mean, tl_std, tl_sts = agg(all_logs["tholonic"])
    delta_pct = (bl_mean - tl_mean) / bl_mean * 100 if bl_mean else float("nan")

    print()
    print("=" * 68)
    print("  ROW 2 RESULTS")
    print(f"\n  {'Condition':<12}  {'Final val loss (mean±std)':>26}")
    print(f"  baseline     {bl_mean:.4f} ± {bl_std:.4f}")
    print(f"  tholonic     {tl_mean:.4f} ± {tl_std:.4f}")
    print(f"  Δ = {delta_pct:+.2f}%  (positive = tholonic is better)")

    print(f"\n  {'Target':>8}  {'Baseline steps':>16}  {'Tholonic steps':>15}  Speedup")
    print(f"  {'-'*56}")
    for t in TARGET_LOSSES:
        bs  = bl_sts.get(str(t))
        ts  = tl_sts.get(str(t))
        spd = f"{(bs - ts) / bs * 100:+.1f}%" if bs and ts else "n/a"
        print(f"  {t:>8}  {str(bs) if bs else 'not reached':>16}"
              f"  {str(ts) if ts else 'not reached':>15}  {spd}")

    if not math.isnan(delta_pct):
        if tl_mean < bl_mean - 0.05:
            verdict = "SUPPORTS — tholonic regularizer improves val loss by >0.05 nats"
        elif tl_mean < bl_mean - 0.01:
            verdict = "TREND — marginal improvement (0.01–0.05 nats)"
        else:
            verdict = "DOES NOT SUPPORT — no improvement in final val loss"
    else:
        verdict = "INDETERMINATE — missing data"
    print(f"\n  VERDICT: {verdict}")

    return {
        "baseline_mean": bl_mean, "baseline_std": bl_std,
        "tholonic_mean": tl_mean, "tholonic_std": tl_std,
        "delta_pct": delta_pct,
        "steps_to_target_baseline": bl_sts,
        "steps_to_target_tholonic": tl_sts,
        "verdict": verdict,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  ROW 3 — OPTIMAL DEPTH
# ══════════════════════════════════════════════════════════════════════════════
def run_row3(train_ids, val_ids):
    print()
    print("=" * 68)
    print("  ROW 3 — OPTIMAL DEPTH")
    print(f"  Depths: {DEPTHS}  d={ROW3_D} h={ROW3_HEADS}  steps/depth={ROW3_STEPS}")
    print(f"  Prediction: optimal depth ≈ log_φ(H₀/H_L) within ±2 layers")
    print("=" * 68)

    depth_results = {}
    best_depth    = None
    best_loss     = float("inf")
    best_model    = None

    for d in DEPTHS:
        run_id = f"row3_depth{d}"
        print(f"\n  Training depth {d} ...", flush=True)
        result = train_one(
            run_id, d, ROW3_D, ROW3_HEADS,
            ROW3_STEPS, "baseline", 42, train_ids, val_ids,
        )
        log   = result[0] if isinstance(result, tuple) else result
        model = result[1] if isinstance(result, tuple) else None
        depth_results[d] = log
        fl = log.get("final_val_loss", float("inf"))
        if fl < best_loss:
            best_loss  = fl
            best_depth = d
            best_model = model

    if best_model is None:
        print("  No model available for H₀/H_L measurement (all runs were resumed).")
        print("  Delete checkpoints/row3_depth*.pt and re-run to regenerate.")
        return {"depth_results": {str(d): depth_results[d] for d in DEPTHS},
                "verdict": "INDETERMINATE — best model not in memory (resumed from checkpoint)"}

    print(f"\n  Measuring H₀ and H_L on best model (depth={best_depth}) ...", flush=True)
    H0, HL     = measure_h0_hl(best_model, val_ids)
    ratio      = H0 / HL if HL > 0 else float("nan")
    pred_depth = math.log(ratio) / math.log(PHI) if ratio > 1 else float("nan")
    error_pct  = abs(pred_depth - best_depth) / best_depth * 100 \
                 if not math.isnan(pred_depth) else float("nan")

    print()
    print("=" * 68)
    print("  ROW 3 RESULTS")
    print(f"\n  {'Depth':>6}  {'Final val loss':>15}  {'Best?'}")
    print(f"  {'-'*35}")
    for d in DEPTHS:
        fl     = depth_results[d].get("final_val_loss", float("nan"))
        marker = "  ← BEST" if d == best_depth else ""
        print(f"  {d:>6}  {fl:>15.4f}{marker}")

    print(f"\n  Best depth (empirical):       {best_depth}")
    print(f"  H₀ (embedding eff-rank):      {H0:.2f}")
    print(f"  H_L (final hidden eff-rank):  {HL:.2f}")
    print(f"  H₀ / H_L:                     {ratio:.3f}")
    print(f"  log_φ(H₀/H_L) prediction:     {pred_depth:.2f}  layers")

    if not math.isnan(error_pct):
        print(f"  Prediction error:             {error_pct:.1f}%  (threshold ±2 layers)")
        if abs(pred_depth - best_depth) <= 2:
            verdict = "SUPPORTS — predicted depth within ±2 layers of empirical optimum"
        elif error_pct <= 25:
            verdict = "CLOSE — within 25%, not within ±2 layers"
        else:
            verdict = f"DOES NOT SUPPORT — off by {error_pct:.1f}%"
    else:
        verdict = "INDETERMINATE — H₀/H_L ≤ 1"
        error_pct = None
    print(f"\n  VERDICT: {verdict}")

    return {
        "depth_results": {str(d): depth_results[d] for d in DEPTHS},
        "best_depth": best_depth, "best_loss": best_loss,
        "H0": H0, "HL": HL, "ratio": ratio,
        "pred_depth": pred_depth, "error_pct": error_pct,
        "verdict": verdict,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--row2",   action="store_true", help="Run Row 2 only")
    parser.add_argument("--row3",   action="store_true", help="Run Row 3 only")
    parser.add_argument("--status", action="store_true", help="Print status and exit")
    args = parser.parse_args()

    if args.status:
        print_status()
        raise SystemExit(0)

    run_both = not args.row2 and not args.row3

    print(f"  Device: {DEVICE}")
    if DEVICE == "cpu":
        print("  WARNING: Running on CPU. Full-scale training will be very slow.")
        print("  Consider using the toy version (train_experiments.py) on CPU.")

    print("\n  Loading WikiText-103 ...", flush=True)
    train_ids, val_ids = load_data()

    t_start = time.time()
    row2_result = row3_result = None

    if args.row2 or run_both:
        row2_result = run_row2(train_ids, val_ids)

    if args.row3 or run_both:
        row3_result = run_row3(train_ids, val_ids)

    # Merge results with any existing data so partial runs don't lose prior rows
    out = {}
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE) as f:
            out = json.load(f)
    if row2_result:
        out["row2"] = row2_result
    if row3_result:
        out["row3"] = row3_result
    if out:
        with open(RESULTS_FILE, "w") as f:
            json.dump(out, f, indent=2)

    elapsed = time.time() - t_start
    print()
    print("=" * 68)
    print("  ALL EXPERIMENTS COMPLETE")
    print(f"  Total elapsed: {elapsed / 3600:.2f} hours")
    print(f"  Results: {RESULTS_FILE}")
    print(f"  Status:  {STATUS_FILE}")
    print("=" * 68)
