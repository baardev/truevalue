#!/usr/bin/env python3
"""
EXPERIMENT 3.1 — ATTENTION MASK PERTURBATION

For each transformer layer l, we inject a structured noise vector into the
hidden state at that layer and measure how far the perturbation propagates
through subsequent layers.

The noise is structured: it is the mean hidden state across token positions
added back to every position (scaled by NOISE_FRAC). This simulates a
corrupted causal mask: a token that should see only its own context now
also sees a diluted signal from all other positions. An architecturally
D-dominant layer (one actively enforcing causal structure) should correct
this leak; a C-dominant layer will propagate it.

Tholonic prediction:
  Perturbations injected into or before the φ-equilibrium zone (45–80% depth)
  should show faster downstream decay than those injected outside it, because
  the φ-zone is a self-stabilising attractor. Perturbation decay is measured as:

      decay(l, m) = || h_m^perturbed - h_m^clean || / || h_{l+1}^perturbed - h_{l+1}^clean ||

  A model PASSES if the mean decay rate across perturbations injected in the
  φ-zone is faster (higher) than for perturbations injected outside it.

Output: attn_mask_perturbation_results.json
"""

import json, math
import torch
import numpy as np
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer

DTYPE        = torch.bfloat16 if torch.cuda.is_available() else torch.float32
DEVICE       = "cuda" if torch.cuda.is_available() else "cpu"
NOISE_FRAC   = 0.05    # fraction of mean-pool activation added as noise
N_TEXTS      = 8       # prompts to average over
PHI_ZONE     = (0.45, 0.80)
RESULTS_FILE = Path(__file__).parent / "attn_mask_perturbation_results.json"

MODELS = [
    ("openai-community/openai-gpt",         "GPT-1",         "GPT-1",   12),
    ("distilgpt2",                           "distilGPT-2",   "GPT-2",    6),
    ("gpt2",                                 "GPT-2 small",   "GPT-2",   12),
    ("gpt2-medium",                          "GPT-2 medium",  "GPT-2",   24),
    ("gpt2-large",                           "GPT-2 large",   "GPT-2",   36),
    ("gpt2-xl",                              "GPT-2 XL",      "GPT-2",   48),
    ("EleutherAI/gpt-neo-125m",              "GPT-Neo 125m",  "GPT-Neo", 12),
    ("EleutherAI/gpt-neo-1.3B",              "GPT-Neo 1.3B",  "GPT-Neo", 24),
    ("EleutherAI/pythia-160m",               "Pythia 160m",   "Pythia",  12),
    ("EleutherAI/pythia-410m",               "Pythia 410m",   "Pythia",  24),
    ("facebook/opt-125m",                    "OPT 125m",      "OPT",     12),
    ("Qwen/Qwen2.5-0.5B",                    "Qwen2.5-0.5B",  "Qwen",    24),
    ("Qwen/Qwen3-0.6B",                      "Qwen3-0.6B",    "Qwen",    28),
    ("TinyLlama/TinyLlama-1.1B-Chat-v1.0",  "TinyLlama 1.1B","LLaMA",   22),
    ("mistralai/Mistral-7B-v0.1",            "Mistral-7B",    "Mistral", 32),
    ("meta-llama/Meta-Llama-3-8B",           "Llama-3-8B",    "LLaMA-3", 32),
    ("google/gemma-2b",                      "Gemma-2B",      "Gemma",   18),
    ("microsoft/phi-2",                      "Phi-2",         "Phi",     32),
    ("microsoft/Phi-3-mini-4k-instruct",     "Phi-3-mini",    "Phi",     32),
    ("tiiuae/falcon-7b",                     "Falcon-7B",     "Falcon",  32),
]

TEXTS = [
    "The study of neural networks reveals deep structural patterns that recur at every scale.",
    "Artificial intelligence is transforming how we understand cognition and decision-making.",
    "Language models learn statistical regularities from vast corpora of human-generated text.",
    "The golden ratio appears throughout nature in spirals, seeds, and branching structures.",
    "A transformer processes tokens in parallel using self-attention and feed-forward layers.",
    "Gradient descent optimizes model weights by propagating error signals backward through layers.",
    "The alignment problem asks how AI systems can remain beneficial as their capabilities grow.",
    "Recursive systems exhibit self-similar structure across multiple levels of organisation.",
]


# ── layer access ──────────────────────────────────────────────────────────────

def get_layers(model):
    """Return a list of transformer block modules, architecture-agnostic."""
    m = model
    # GPT-2, GPT-Neo, Falcon
    if hasattr(m, "transformer") and hasattr(m.transformer, "h"):
        return list(m.transformer.h)
    # LLaMA, Mistral, Gemma, Phi, Qwen
    if hasattr(m, "model") and hasattr(m.model, "layers"):
        return list(m.model.layers)
    # OPT
    if hasattr(m, "model") and hasattr(m.model, "decoder") \
            and hasattr(m.model.decoder, "layers"):
        return list(m.model.decoder.layers)
    # Pythia / GPT-NeoX
    if hasattr(m, "gpt_neox") and hasattr(m.gpt_neox, "layers"):
        return list(m.gpt_neox.layers)
    raise ValueError(f"Cannot locate transformer layers in {type(model).__name__}")


# ── hidden state collection via our own hooks ─────────────────────────────────
#
# Background: many architectures (e.g. newer GPT-2 variants) collect hidden
# states internally using hooks that fire BEFORE user-registered hooks, so
# output.hidden_states always reflects the unmodified pass.  We work around
# this by NOT using output_hidden_states=True and instead collecting the
# states ourselves via forward (and pre-forward) hooks.  This guarantees the
# modified output at inject_layer is captured at index l+1, not the clean value.

@torch.no_grad()
def collect_hidden_states(model, input_ids, inject_layer=None, noise_vec=None):
    """
    Run the model and collect hidden states at every layer boundary using hooks.

    Returns a list of n_layers+1 float32 CPU tensors:
        index 0  = embedding (input to block 0)
        index i  = output of block i-1  (= input to block i)
        index L  = output of the last block

    If inject_layer is not None, noise_vec is added to the output of that block.
    The MODIFIED output is stored at index inject_layer+1, not the clean value,
    because we capture inside our own hook rather than relying on the model's
    internal collection.
    """
    layers = get_layers(model)
    n = len(layers)
    buf = [None] * (n + 1)

    def make_hook(idx):
        def hook(module, inp, out):
            is_seq = isinstance(out, (tuple, list))
            h = out[0] if is_seq else out
            if inject_layer is not None and idx == inject_layer:
                nv = noise_vec.to(h.device, h.dtype)
                h = h + nv
                if is_seq:
                    out = type(out)([h] + list(out[1:]))
                else:
                    out = h
            buf[idx + 1] = h.detach().float()
            return out  # return (possibly modified) output
        return hook

    def pre_hook_0(module, inp):
        # inp is a tuple; first element is the hidden state entering block 0
        buf[0] = inp[0].detach().float()

    handles = [layer.register_forward_hook(make_hook(i)) for i, layer in enumerate(layers)]
    handles.append(layers[0].register_forward_pre_hook(pre_hook_0))
    try:
        model(input_ids.to(DEVICE))
    finally:
        for h in handles:
            h.remove()

    return buf


# ── per-model measurement ─────────────────────────────────────────────────────

def measure_decay_profile(model, tok, n_layers):
    """
    For each injection layer l (0..n_layers-1), compute the mean downstream
    decay rate across N_TEXTS prompts.

    decay_rate[l] = mean over texts of:
        1 - (mean shift at layers l+2..L) / (shift at layer l+1)

    A higher value means the perturbation was absorbed faster.

    Returns: decay_rates list (one per layer), phi_advantage (positive = phi zone faster)
    """
    per_layer_decays = []  # decay_rates[l] averaged over texts

    for l in range(n_layers):
        text_decays = []
        for text in TEXTS[:N_TEXTS]:
            ids = tok(text, return_tensors="pt", truncation=True, max_length=64)["input_ids"]
            if ids.shape[1] < 4:
                continue

            clean_hs = collect_hidden_states(model, ids)
            # noise = mean-pool of the clean hidden state at layer l, scaled by NOISE_FRAC
            # shape: (1, seq, hidden)
            h_l = clean_hs[l + 1]  # +1 because index 0 is embedding
            noise = h_l.mean(dim=1, keepdim=True).expand_as(h_l) * NOISE_FRAC

            pert_hs = collect_hidden_states(model, ids, inject_layer=l, noise_vec=noise)

            # Compute shift at each subsequent layer relative to injection shift
            # pert_hs[l+1] is the modified output of block l (captured in our hook)
            injection_shift = (pert_hs[l + 1] - clean_hs[l + 1]).norm().item()
            if injection_shift < 1e-8:
                continue

            downstream_shifts = []
            for m in range(l + 2, n_layers + 1):
                shift_m = (pert_hs[m] - clean_hs[m]).norm().item()
                downstream_shifts.append(shift_m / injection_shift)

            if downstream_shifts:
                # decay rate: 1 - mean(downstream / injection)
                # higher = faster decay = better absorption
                text_decays.append(1.0 - float(np.mean(downstream_shifts)))

        per_layer_decays.append(float(np.mean(text_decays)) if text_decays else float("nan"))

    # φ-advantage: mean decay in φ-zone minus mean decay outside
    # positive = φ-zone absorbs faster (tholonic prediction)
    phi_vals, out_vals = [], []
    for l, rate in enumerate(per_layer_decays):
        if math.isnan(rate):
            continue
        frac = l / n_layers
        if PHI_ZONE[0] <= frac <= PHI_ZONE[1]:
            phi_vals.append(rate)
        else:
            out_vals.append(rate)

    phi_mean = float(np.mean(phi_vals))   if phi_vals else float("nan")
    out_mean = float(np.mean(out_vals))   if out_vals else float("nan")
    phi_adv  = round(phi_mean - out_mean, 4) \
               if not math.isnan(phi_mean) and not math.isnan(out_mean) else float("nan")

    verdict = "PASS" if (not math.isnan(phi_adv) and phi_adv > 0) else "FAIL"
    return per_layer_decays, phi_adv, phi_mean, out_mean, verdict


# ── main ──────────────────────────────────────────────────────────────────────

def assess(hf_name, display_name, family, n_exp):
    tok = AutoTokenizer.from_pretrained(hf_name, trust_remote_code=True,
                                        local_files_only=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        hf_name,
        trust_remote_code=True,
        dtype=DTYPE,
        low_cpu_mem_usage=True,
        local_files_only=True,
    ).to(DEVICE)
    model.eval()
    n = model.config.num_hidden_layers

    try:
        get_layers(model)
    except ValueError as e:
        return {"hf_name": hf_name, "display_name": display_name, "family": family,
                "error": str(e)}

    decay_profile, phi_adv, phi_mean, out_mean, verdict = measure_decay_profile(model, tok, n)

    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return {
        "hf_name":        hf_name,
        "display_name":   display_name,
        "family":         family,
        "n_layers":       n,
        "decay_profile":  [round(v, 5) if not math.isnan(v) else None for v in decay_profile],
        "phi_advantage":  phi_adv,    # positive = φ-zone absorbs faster (PASS)
        "phi_mean_decay": round(phi_mean, 4) if not math.isnan(phi_mean) else None,
        "out_mean_decay": round(out_mean, 4) if not math.isnan(out_mean) else None,
        "verdict":        verdict,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("  EXPERIMENT 3.1 — ATTENTION MASK PERTURBATION")
    print("  Noise: mean-pool position leak (NOISE_FRAC=0.05)")
    print("  Prediction: φ-zone (45–80%) absorbs perturbation faster")
    print("  (positive φ-advantage = PASS)")
    print("=" * 70)

    results = []
    n_pass = 0

    for hf_name, display_name, family, n_exp in MODELS:
        print(f"\n  Assessing {display_name} ...", flush=True)
        try:
            r = assess(hf_name, display_name, family, n_exp)
            results.append(r)
            if r.get("verdict") == "PASS":
                n_pass += 1
            pa = r.get("phi_advantage")
            pm = r.get("phi_mean_decay")
            om = r.get("out_mean_decay")
            pa_s = f"{pa:+.4f}" if pa is not None and not math.isnan(pa) else "n/a"
            pm_s = f"{pm:.4f}"  if pm is not None else "n/a"
            om_s = f"{om:.4f}"  if om is not None else "n/a"
            print(f"    φ-advantage={pa_s}  φ-zone decay={pm_s}  "
                  f"outside decay={om_s}  → {r.get('verdict', 'ERROR')}")
        except Exception as ex:
            import traceback
            print(f"    ERROR: {ex}")
            traceback.print_exc()
            results.append({"hf_name": hf_name, "display_name": display_name,
                             "family": family, "error": str(ex)})

    n = len([r for r in results if "verdict" in r])
    print("\n" + "=" * 70)
    print(f"  SUMMARY — Attention Mask Perturbation (Experiment 3.1)")
    print(f"  {'Model':<18} {'φ-advantage':>12} {'φ decay':>9} {'out decay':>10} {'Verdict':>8}")
    print(f"  {'-'*60}")
    for r in results:
        if "verdict" in r:
            pa = r.get("phi_advantage")
            pm = r.get("phi_mean_decay")
            om = r.get("out_mean_decay")
            pa_s = f"{pa:>+12.4f}" if pa is not None and not math.isnan(pa) else f"{'n/a':>12}"
            pm_s = f"{pm:>9.4f}"   if pm is not None else f"{'n/a':>9}"
            om_s = f"{om:>10.4f}"  if om is not None else f"{'n/a':>10}"
            print(f"  {r['display_name']:<18} {pa_s} {pm_s} {om_s} {r['verdict']:>8}")
        else:
            print(f"  {r['display_name']:<18}  ERROR: {r.get('error','?')}")

    if n:
        print(f"\n  Pass rate: {n_pass}/{n} = {n_pass/n*100:.0f}%")
        print(f"  Tholonic prediction: φ-zone decay rate > outside zone decay rate")
        print(f"  (positive φ-advantage means the prediction is supported)")

    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved → {RESULTS_FILE}")
    print("=" * 70)
