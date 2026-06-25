#!/usr/bin/env python3
"""
EXPERIMENT 3.2 — ACTIVATION STEERING

For each transformer layer l, we inject a random unit-vector perturbation
scaled to 10% of that layer's activation norm. We then track how the
perturbation magnitude decays across the subsequent layers.

This is the cleanest possible test of self-stabilisation: if the φ-equilibrium
zone is a genuine structural attractor, perturbations introduced at or before
that zone should be damped more aggressively than perturbations introduced
outside it.

Metric:
    For a perturbation injected at layer l, compute the "half-life" h(l):
    the number of subsequent layers required for the perturbation magnitude
    to fall below 50% of its injection magnitude.

    Formally:
        shift_m = || h_m^perturbed - h_m^clean || (for m > l)
        half_life(l) = smallest m-l such that shift_m / shift_{l+1} < 0.5

    A SHORTER half-life means faster absorption = stronger self-stabilisation.

Tholonic prediction:
    Perturbations injected at layers within the φ-equilibrium zone (45–80% depth)
    should have a shorter mean half-life than perturbations injected outside it.
    A model PASSES if mean half-life(φ-zone) < mean half-life(outside).

Two noise types are run:
    - Random: zero-mean Gaussian, IID per dimension (tests general stability)
    - Structured: the mean hidden state across positions (positional leak noise,
      same as Experiment 3.1 — confirms that the two experiments agree)

Output: activation_steering_results.json
"""

import json, math
import torch
import numpy as np
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer

DTYPE        = torch.bfloat16 if torch.cuda.is_available() else torch.float32
DEVICE       = "cuda" if torch.cuda.is_available() else "cpu"
NOISE_SCALE  = 0.10   # noise is 10% of layer activation norm
N_DRAWS      = 3      # random noise draws per layer per text
PHI_ZONE     = (0.45, 0.80)
RESULTS_FILE = Path(__file__).parent / "activation_steering_results.json"

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
    if hasattr(m, "transformer") and hasattr(m.transformer, "h"):
        return list(m.transformer.h)
    if hasattr(m, "model") and hasattr(m.model, "layers"):
        return list(m.model.layers)
    if hasattr(m, "model") and hasattr(m.model, "decoder") \
            and hasattr(m.model.decoder, "layers"):
        return list(m.model.decoder.layers)
    if hasattr(m, "gpt_neox") and hasattr(m.gpt_neox, "layers"):
        return list(m.gpt_neox.layers)
    raise ValueError(f"Cannot locate transformer layers in {type(model).__name__}")


# ── hidden state collection via our own hooks ─────────────────────────────────
#
# Many architectures collect hidden states internally with hooks that fire
# BEFORE user hooks, meaning output.hidden_states always reflects clean values
# at the injection layer.  We bypass this by not using output_hidden_states=True
# and instead collecting states ourselves.

@torch.no_grad()
def collect_hidden_states(model, input_ids, inject_layer=None, noise_vec=None):
    """
    Run the model and collect hidden states at every layer boundary.
    Returns a list of n_layers+1 float32 tensors:
        index 0  = embedding (input to block 0)
        index i  = output of block i-1

    If inject_layer is set, noise_vec is added to block inject_layer's output,
    and the MODIFIED value is stored at index inject_layer+1.
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
            return out
        return hook

    def pre_hook_0(module, inp):
        buf[0] = inp[0].detach().float()

    handles = [layer.register_forward_hook(make_hook(i)) for i, layer in enumerate(layers)]
    handles.append(layers[0].register_forward_pre_hook(pre_hook_0))
    try:
        model(input_ids.to(DEVICE))
    finally:
        for h in handles:
            h.remove()

    return buf


# ── half-life computation ─────────────────────────────────────────────────────

def half_life(shifts_relative):
    """
    Given shifts_relative[0..k] = shift at layers l+1, l+2, ..., l+k+1
    (each normalised by the injection shift at l+1), return the half-life:
    the smallest index m such that shifts_relative[m] < 0.5.
    If never reached, return len(shifts_relative) (maximum).
    """
    for i, s in enumerate(shifts_relative):
        if s < 0.5:
            return i
    return len(shifts_relative)


# ── per-model measurement ─────────────────────────────────────────────────────

def measure_half_lives(model, tok, n_layers):
    """
    For each injection layer, compute the mean half-life across texts and draws.
    Returns:
        hl_random[l]    — mean half-life for random noise
        hl_structured[l] — mean half-life for structured (mean-pool) noise
        phi_advantage_random    — mean HL outside φ-zone minus mean HL inside (positive=PASS)
        phi_advantage_structured
    """
    hl_random     = []
    hl_structured = []

    for l in range(n_layers):
        hl_r_list, hl_s_list = [], []

        for text in TEXTS:
            ids = tok(text, return_tensors="pt", truncation=True, max_length=64)["input_ids"]
            if ids.shape[1] < 4:
                continue

            clean_hs = collect_hidden_states(model, ids)
            h_l = clean_hs[l + 1]   # shape: (1, seq, hidden)
            act_norm = h_l.norm().item()
            if act_norm < 1e-8:
                continue

            noise_scale = act_norm * NOISE_SCALE

            # ── random noise ──────────────────────────────────────────────────
            for _ in range(N_DRAWS):
                rand_noise = torch.randn_like(h_l)
                rand_noise = rand_noise / rand_noise.norm() * noise_scale

                pert_hs = collect_hidden_states(model, ids, inject_layer=l,
                                                noise_vec=rand_noise)
                inj_shift = (pert_hs[l + 1] - clean_hs[l + 1]).norm().item()
                if inj_shift < 1e-8:
                    continue

                rel = []
                for m in range(l + 2, n_layers + 1):
                    rel.append((pert_hs[m] - clean_hs[m]).norm().item() / inj_shift)
                hl_r_list.append(half_life(rel))

            # ── structured noise (mean-pool positional leak) ───────────────────
            struct_noise = h_l.mean(dim=1, keepdim=True).expand_as(h_l) * (NOISE_SCALE * 2)
            struct_norm  = struct_noise.norm().item()
            if struct_norm > 1e-8:
                struct_noise = struct_noise / struct_norm * noise_scale

            pert_hs = collect_hidden_states(model, ids, inject_layer=l,
                                            noise_vec=struct_noise)
            inj_shift = (pert_hs[l + 1] - clean_hs[l + 1]).norm().item()
            if inj_shift > 1e-8:
                rel = []
                for m in range(l + 2, n_layers + 1):
                    rel.append((pert_hs[m] - clean_hs[m]).norm().item() / inj_shift)
                hl_s_list.append(half_life(rel))

        hl_random.append(float(np.mean(hl_r_list))     if hl_r_list else float("nan"))
        hl_structured.append(float(np.mean(hl_s_list)) if hl_s_list else float("nan"))

    def phi_advantage(half_lives):
        phi_vals, out_vals = [], []
        for l, hl in enumerate(half_lives):
            if math.isnan(hl):
                continue
            frac = l / n_layers
            if PHI_ZONE[0] <= frac <= PHI_ZONE[1]:
                phi_vals.append(hl)
            else:
                out_vals.append(hl)
        phi_m = float(np.mean(phi_vals)) if phi_vals else float("nan")
        out_m = float(np.mean(out_vals)) if out_vals else float("nan")
        # positive advantage = outside HL longer than phi HL = phi absorbs faster = PASS
        adv = round(out_m - phi_m, 3) \
              if not math.isnan(phi_m) and not math.isnan(out_m) else float("nan")
        return adv, phi_m, out_m

    adv_r, phi_r, out_r = phi_advantage(hl_random)
    adv_s, phi_s, out_s = phi_advantage(hl_structured)

    return (hl_random, hl_structured,
            adv_r, phi_r, out_r,
            adv_s, phi_s, out_s)


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

    (hl_rand, hl_struct,
     adv_r, phi_r, out_r,
     adv_s, phi_s, out_s) = measure_half_lives(model, tok, n)

    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    verdict_rand   = "PASS" if (not math.isnan(adv_r) and adv_r > 0) else "FAIL"
    verdict_struct = "PASS" if (not math.isnan(adv_s) and adv_s > 0) else "FAIL"
    # overall: both noise types must pass
    verdict = "PASS" if verdict_rand == "PASS" and verdict_struct == "PASS" else "FAIL"

    return {
        "hf_name":          hf_name,
        "display_name":     display_name,
        "family":           family,
        "n_layers":         n,
        "half_life_random":     [round(v, 3) if not math.isnan(v) else None for v in hl_rand],
        "half_life_structured": [round(v, 3) if not math.isnan(v) else None for v in hl_struct],
        # positive = φ-zone absorbs faster = PASS
        "phi_advantage_random":     adv_r,
        "phi_mean_hl_random":       round(phi_r, 3) if not math.isnan(phi_r) else None,
        "out_mean_hl_random":       round(out_r, 3) if not math.isnan(out_r) else None,
        "phi_advantage_structured": adv_s,
        "phi_mean_hl_structured":   round(phi_s, 3) if not math.isnan(phi_s) else None,
        "out_mean_hl_structured":   round(out_s, 3) if not math.isnan(out_s) else None,
        "verdict_random":    verdict_rand,
        "verdict_structured": verdict_struct,
        "verdict":           verdict,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("  EXPERIMENT 3.2 — ACTIVATION STEERING")
    print("  Noise: random Gaussian + structured (mean-pool) at 10% activation norm")
    print("  Metric: half-life (layers until perturbation < 50% of injection)")
    print("  Prediction: φ-zone (45–80%) has shorter half-life (faster absorption)")
    print("  (positive φ-advantage = φ-zone HL shorter than outside = PASS)")
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
            adv_r = r.get("phi_advantage_random", float("nan"))
            adv_s = r.get("phi_advantage_structured", float("nan"))
            print(f"    rand-adv={adv_r:+.3f} ({r.get('verdict_random','?')})  "
                  f"struct-adv={adv_s:+.3f} ({r.get('verdict_structured','?')})  "
                  f"→ overall {r.get('verdict','?')}")
        except Exception as ex:
            import traceback
            print(f"    ERROR: {ex}")
            traceback.print_exc()
            results.append({"hf_name": hf_name, "display_name": display_name,
                             "family": family, "error": str(ex)})

    n = len([r for r in results if "verdict" in r])
    print("\n" + "=" * 70)
    print(f"  SUMMARY — Activation Steering (Experiment 3.2)")
    print(f"  {'Model':<18} {'rand-adv':>10} {'struct-adv':>11} "
          f"{'rand':>6} {'struct':>7} {'overall':>8}")
    print(f"  {'-'*63}")
    for r in results:
        if "verdict" in r:
            print(f"  {r['display_name']:<18} "
                  f"{r['phi_advantage_random']:>+10.3f} "
                  f"{r['phi_advantage_structured']:>+11.3f} "
                  f"{r['verdict_random']:>6} {r['verdict_structured']:>7} "
                  f"{r['verdict']:>8}")
        else:
            print(f"  {r['display_name']:<18}  ERROR: {r.get('error','?')}")

    if n:
        print(f"\n  Overall pass rate: {n_pass}/{n} = {n_pass/n*100:.0f}%")
        print(f"  Prediction: φ-zone half-life < outside half-life (positive advantage)")

    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved → {RESULTS_FILE}")
    print("=" * 70)
