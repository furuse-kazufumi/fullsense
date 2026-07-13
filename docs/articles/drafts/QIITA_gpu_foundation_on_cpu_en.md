---
title: "Building the Research Foundation on CPU Alone, Before the GPU Box Arrives —— Making Scale a Config-and-Flag Change, Not a Rewrite"
tags:
  - AI
  - GPU
  - MuJoCo
  - jax
  - WorldModels
private: false
public_private: false
---

# Building the Research Foundation on CPU Alone, Before the GPU Box Arrives —— Making Scale a Config-and-Flag Change, Not a Rewrite

> For: people running world-model, evolutionary-computation, and robotics simulations on a home PC / people who "want to add a GPU soon" but "don't want to rewrite the code."
> Prerequisites: If you can read Python, you're set. torch / jax / MuJoCo jargon is unpacked as it comes up.
> Everything here is CPU-verified. But the GPU measurements (speedup factors, MJX batching) have **not been run even once yet**—and I draw that line honestly in the body.

---

## 0. TL;DR (conclusion first)

- A PC with a GPU arrives this week. **Instead of waiting**, I got the CPU-only world-model + robot-evolution codebase (`onocollo`) into a shape where the moment I drop it onto the GPU box is "setup + flag change," not "rewrite."
- First I **measured instead of guessing**: the whole codebase is 100% serial, single-environment MuJoCo, the bottlenecks are (1) the rocket-evaluation experiment, (2) ADR grasping, and (3) swimmer QD; the world model (Dreamer/RSSM) is already CUDA-clean, but the V→M→C pixel path had CPU-hardcoded obstacles. I implemented three **portable wins** that can be built on CPU (stdlib parallel map / `device="auto"` wiring / cross-platform environment bootstrap).
- But honestly, **neither the GPU speedup nor MJX's batched physics has been run even once** (there's no GPU yet). So I shipped the biggest candidate win (MJX) not as a "port" but as a "**go/no-go throughput measurement to run first**." "Don't port the control loop before you measure"—keeping that rule is itself the theme of this article.

---

## 1. Glossary (map first)

| Term | Unpacked |
|---|---|
| onocollo | My own CPU-complete research codebase. A world model (learns from pixels) and robot evolution/QD sims bundled into one. |
| world model | A model that reproduces the environment in its head. The classic pixel→latent→predict→control V→M→C structure. |
| V→M→C | The 3-stage pipeline of Vision (a VAE that compresses images) → Memory (an RNN that predicts over time) → Controller (chooses actions). |
| VAE (variational autoencoder) | A net that compresses/reconstructs images into a small latent vector. The 64×64-pixel convolutions are where the GPU helps most. |
| Dreamer / RSSM | The modern take on world models. Rolls latent states forward to learn a policy "in a dream." RSSM = recurrent state space model. |
| MuJoCo | A physics simulator. Its C engine solves rigid bodies and contacts. The foundation for the rocket, grasping, and walking. |
| MJX | The GPU version of MuJoCo, rewritten in jax. It can step thousands of **identically shaped** models together on the GPU in parallel (batched physics). |
| jax | A numerical library that does autodiff + vectorization on GPU/TPU. `jax.vmap` "applies a function in bulk." |
| bottleneck | The single heaviest spot that dominates total run time. Polishing anything else is wasted until you speed this up. |
| embarrassingly parallel | The state where each job is independent of the others, so you speed up just by splitting and handing them out. |
| process-parallel | Distribute independent evaluations across multiple CPU cores (processes) and run them at once. A straightforward speedup that needs no GPU. |
| ADR (adversarial / automatic domain randomization) | An evaluation that hardens robot grasping under deliberately harsh conditions. Here, the heavy grasp-rollout loop. |
| QD (quality-diversity) | Evolution that grows not just "a fast solution" but "a map of diverse, good solutions." Used for the swimmer's morphology search. |
| go/no-go gate | A gate that independently measures "will this even get faster?" before the real port. Decide up front: if NO-GO, don't port. |

---

## 2. The situation: the GPU box arrives this week. Wait, or prepare?

`onocollo` has been built on a "CPU-first, then 1 GPU" promise. On my underpowered home laptop CPU (torch is `2.12.0+cpu`), it **bundles a world model and robot evolution into a single codebase**. The world model learns landing and grasping from pixels via V→M→C / Dreamer-style stacks; the robot side runs rocket landing, ADR grasping, and swimmer morphology evolution in MuJoCo.

Then a PC with a GPU was set to arrive this week. The normal move here would be "think about GPU support once the box shows up"—but that scripts a familiar day: it arrives, and I realize "oh, running this code on the GPU takes a fair bit of rewriting," and I burn several days. I've done exactly that, many times.

So I decided: **do the "GPU support" on CPU, before the box arrives.** One goal:

> Make the moment of loading onto the GPU box a **setup + flag change**, not a **rewrite**.

This article is the record of how honestly I could build that "preparation" on CPU alone—and **where I honestly admitted "not run yet."**

---

## 3. Measure first: the compute map (no guessing your way to GPU support)

A discipline we keep across all of FullSense: "when a result is suspiciously good, doubt the breakdown," and "don't move your hands before you measure." GPU support is the same—**don't pick your porting target by "probably this is slow."** The first thing I did was an audit—a **compute map** of the whole codebase, i.e., a map of "which loop eats how much compute, where, and which accelerator helps it most."

What I found was blunt and simple:

> The codebase is currently **100% serial, single-environment MuJoCo**. `Simulation` just steps one `MjModel`+`MjData` in a Python loop. No code path has `multiprocessing`, `jax`, or `mjx` anywhere.

Meanwhile, the evolution, QD, and evaluation loops are **independent across candidate × episode × seed**—that is, they're embarrassingly parallel, yet they don't use one bit of that parallelism. That's the headroom. As a map, it looks like this:

| Workload | Where | Cost | Best accelerator |
|---|---|---|---|
| **Rocket evaluation experiment** | inner loops in `rocket_eval_experiment.py`, `landing.py` | **#1** — 1600 steps × thousands/seed × 10 seeds + PID grid re-tuning ≈ 10M `mj_step`/seed | **MJX** (single fixed `RocketSpec` → homogeneous batch, ideal) or process-parallel over 10 seeds (cheapest, portable) |
| **ADR robust / neural grasping** | `adr/capture.py` | #2 — `num_incoming × (1 + num_actuators)` rollouts × population × seed | **process-parallel** (near-linear). IK/contact inside the loop is Python, so MJX is partly a poor fit |
| **Swimmer / morphology QD** | `evolve/evolution.py`, `qd.py` | #3 — short (~430-step) rollouts, **a different model per genome** | **process-parallel over the population** (MJX would need a per-morphology batch) |
| **World model V→M→C** | VAE / MDN-RNN training in `train.py` | GPU-favorable convolutions + sequence training | **torch CUDA** (`device="auto"`) |
| **Dreamer / RSSM** | `dreamer.py`, `rssm.py` | Small MLP/GRU; GPU only helps once dimensions grow | **torch CUDA**, already device-clean |
| Controller ES | `train.py` | serial, single-sample | none — leave on CPU (GPU is a net loss) |

This map decided everything about **"what, in what order"** from here on. Based on the audit, not on guessing.

Two important asymmetries showed up here:

1. **The world-model side was already mostly GPU-ready.** The Dreamer/RSSM stack was device-clean from the start. But **CPU-hardcoded obstacles** remained in the classic V→M→C pixel path (VAE pixel training, MDN-RNN, and the VAE-encode bridge).
2. **The robot side isn't parallelized across a single core.** But since each loop is a collection of independent candidates, it can be sped up on many cores **without even needing a GPU**.

In other words, what I'd been lumping together as "GPU support" was actually **three wins of different natures**. Build them in order.

---

## 4. Portable win A: run the evolution loops on many cores (no GPU, no jax)

This is the one that helps most and costs least. I added a `--workers` / `parallel_map` path to the evolution, QD, and evaluation loops. The implementation is a single function in `onocollo.parallel`, and **the only dependency is the standard-library `concurrent.futures`** (no jax, no ray, no joblib).

The key to the design is keeping it **byte-for-byte identical to serial**. `--workers 1` (the default) doesn't change by a single bit from before. On a many-core box, the same experiment just runs faster.

```python
def parallel_map(fn, items, *, workers=1, backend="auto"):
    # backend="auto": serial if workers<=1, otherwise process
    if backend == "auto":
        backend = "serial" if workers <= 1 else "process"
    if backend == "serial":
        return [fn(x) for x in items]
    if backend == "process":
        seq = list(items)
        with ProcessPoolExecutor(max_workers=workers) as pool:
            # submit in input order and collect by index (not as_completed)
            # → output order = input order is structurally guaranteed
            futures = [pool.submit(fn, x) for x in seq]
            return [f.result() for f in futures]
```

The point is that it's a **plug-compatible replacement** for `[fn(x) for x in items]`. If `fn` is a pure function of its argument (onocollo's seeded evaluations are), then parallel output = serial output. And because it collects **by index** rather than via `as_completed` (completion order), **the returned order is always input order** regardless of worker completion order—determinism doesn't break.

Usage looks like this. Just spread the 10 independent seeds of the rocket evaluation across your cores:

```bash
# rocket evaluation — spread 10 independent seeds across cores
PYTHONPATH=src py -3.11 scripts/rocket_eval_experiment.py \
    --condition P --seeds 0-9 --workers 8 --out out/rocket/eval_exp
```

I embedded the honest caveats too. On Windows, the start method is `spawn`, so `fn` and each item must be picklable (no lambdas/closures—use module-level functions), and the calling script must be guarded with `if __name__ == "__main__":`—otherwise, under spawn, each worker re-imports the parent module and **forks infinitely**. As for determinism, each seed writes its own JSON in a self-contained, paired-common-random-numbers run, so parallel output = serial output (verified with a `--quick` smoke test). The frozen-PID cache is warmed once before fan-out to avoid write races.

**This is a win that works even now, with no GPU yet.** It gets faster by your core count even on my laptop, and scales linearly as-is on the new many-core box. Without using a single GPU.

---

## 5. Portable win B: move world-model training to CUDA (one flag)

Crush the obstacle on the world-model side. Make `WMConfig.device` a three-value `"auto" | "cpu" | "cuda"`, where `"auto"` resolves to `cuda` if there's a GPU and `cpu` if not. The guts are just this, in `utils.resolve_device`:

```python
def resolve_device(device: str) -> str:
    """Resolve a config device string into a concrete torch device."""
    if device == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    return device  # pass "cpu"/"cuda"/"cuda:0" etc. through as-is
```

Dreamer/RSSM were device-clean to begin with, so the work was **wiring the device through the classic V→M→C path**. I threaded `device` through the VAE pixel training, the MDN-RNN, and the VAE-encode bridge so the **whole pipeline loads onto the GPU with one flag**. And it stays byte-for-byte identical on CPU—meaning "making it GPU-ready changed the CPU results" never happens.

The call site looks like this:

```python
import dataclasses
import onocollo as oc
from onocollo import default_config

# world model V/M/C on GPU (scaled up from the tiny preset):
cfg = dataclasses.replace(default_config(), device="auto")
oc.run_pipeline(cfg)
```

### Where the GPU truly helps (honestly)

This is the part where it matters not to exaggerate. **The GPU clearly helps only in the ConvVAE pixel training (64×64×3, four strided-convolution layers).** At the default tiny dimensions (deter ≤ 64), the RSSM/Dreamer compute is light, and **the GPU's launch overhead can actually dominate**—the GPU only wins once you raise `z_dim` / `deter` / `batch` / `train_iters`.

So the point of the GPU box isn't to "make the micro preset faster," it's to **run non-tiny settings that CPU can't handle**. Scaling up the presets (larger `z_dim`, more `train_steps`, longer sequences) is the correct use; expecting the tiny preset to just get faster is a misread. Unless you write this asymmetry into the docs, you'll misread "huh, it's not faster" on the GPU box.

---

## 6. Linux-only win C: MJX batched rocket —— but "measure first"

Now, the #1 bottleneck on the compute map was the rocket evaluation. And this is also MJX's **one clean fit**. Because it's a single, fixed-shape `RocketSpec` model, thousands of rollouts form a **homogeneous batch** that `jax.vmap` + MJX can vectorize on the GPU. In theory, the biggest win.

Here comes the **honesty fork**.

MJX is jax's GPU physics, and its **official CUDA wheels are Linux-only** (Windows needs WSL2). And—**it isn't installed on my CPU workstation, and I've never verified it**. In theory the biggest win, but the measurements are zero.

| Tier | Windows | Linux |
|---|---|---|
| **torch CUDA** (world-model training) | ✅ native | ✅ native |
| **many-core process parallelism** (evolution loops) | ✅ native | ✅ native |
| **MJX** (jax GPU physics batch) | ❌ WSL2 required | ✅ native |

The single worst thing to do here is **write up a port while pretending unverified GPU code "works."** It's easy to write out the whole MJX rollout and put "thousands of times faster on GPU!" in an article, but that would be a lie.

So instead of porting, I shipped a **gate that runs a go/no-go throughput probe first**. The rule is one line:

> **Don't port the control loop before the gate passes.**

The gate runs like this. First, measure only the necessary condition:

```bash
# go/no-go throughput gate (measures only the raw open-loop physics)
PYTHONPATH=src py -3.11 scripts/mjx_spike.py --batch 2048 --steps 200
```

This compares an **open-loop batched step without a controller** (control is deliberately dropped to isolate the physics) against a serial C engine extrapolated to the same `batch*steps` workload, and prints `GO` / `MARGINAL` / `NO-GO` against a 5× threshold.

- **`NO-GO`** → stop. If GPU-vectorized stepping isn't fundamentally faster on this model+GPU, porting the control loop won't save it. Stay on the process-parallel `--workers` path.
- **`MARGINAL`** → retry with a larger `--batch` (4096, 8192). Fixed jit/launch overhead amortizes at scale. Re-judge.
- **`GO`** → only now proceed to the real port.

And even if `GO` comes up, **numerical verification** waits after the port. MJX doesn't match the C engine bit-for-bit (the contact-solver internals differ), so until I've confirmed that the rocket's landing statistics match `landing.py` within tolerance over a few CPU seeds, I **must not silently swap the scoring rollouts of a pre-registered experiment onto a different physics engine.** The rocket lands on its legs—contact-rich dynamics are exactly where the MJX solver drifts most from the C engine.

Honestly, all I "shipped" on CPU is this:

- `onocollo/mujoco/mjx_batch.py` — `has_mjx()`, `require_mjx()` (a clear install error), `mjx_throughput_probe(...)` (standard mjx API, not run on CPU).
- `scripts/mjx_spike.py` — the runnable gate. On a box without MJX support, it prints "not available" and exits non-zero (**it does not fabricate results**).
- `tests/test_mjx_batch.py` — verifies the guard paths on CPU (here `has_mjx()` is False, `require_mjx()` raises an actionable error, and the probe refuses to run).

**Don't call unverified things "working." Ship the gate, and do the port after the gate**—that's honesty, implemented.

---

## 7. Make setup and verification "one command"

I bootstrapped the three wins so I can bring them up **in one command** on the day the box arrives. The design is "dry-run by default"—nothing touches the machine until I can commit and read it.

```bash
# dry-run first (prints the exact pip plan for this machine, installs nothing):
py -3.11 scripts/setup_gpu_env.py
# run it:
py -3.11 scripts/setup_gpu_env.py --run
# verify what actually came up (torch CUDA / MuJoCo render / jax・MJX):
py -3.11 scripts/verify_gpu_env.py
```

`setup_gpu_env.py` detects the NVIDIA GPU via `nvidia-smi` and installs the **CUDA torch wheel** instead of `+cpu`. It adds `onocollo[dev,mujoco]`, `cma`, and media encoders, and installs `jax[cuda12]` + `mujoco-mjx` **only on Linux**. `MUJOCO_GL` is auto-selected by `onocollo.viz.backend` (glfw on Windows/macOS, egl on a headless Linux GPU box). If MJX is requested on Windows, it **prints a WSL2 note and skips**—without fabricating anything.

`verify_gpu_env.py` is a non-destructive probe: it exits 0 if the core path (numpy + torch + onocollo import) passes, and the GPU/MJX lines are **reported but don't drop the verdict** (they're optional tiers). It prints torch's CUDA availability, an actual MuJoCo offscreen render, and jax devices in a table.

The day-one checklist on a new box is just this:

1. `setup_gpu_env.py --run` → `verify_gpu_env.py` (expect `torch CUDA: ok`, and on Linux `jax devices: ok`).
2. sanity: `pytest -q` (green except the 5 known hygiene fails; more below).
3. the free many-core win: re-run the rocket evaluation with `--workers <cores>` and confirm it matches serial seeds.
4. the torch CUDA win: watch `run_pipeline(replace(default_config(), device="auto"))` load onto the GPU, then scale up the config.
5. Linux only: the MJX go/no-go gate. If it passes, batch the rollouts; if not, stay on process-parallel and **record why**.

### Honest aside: the 5 failing tests are "contradictory tests," not an implementation bug

Currently pytest has **only 5 failures** (`test_import_hygiene.py`; the rest are green). Honestly, these 5 are a case where **the test suites contradict each other.** The facade design exposes `onocollo.train` as a callable while keeping the real submodule reachable too—one commit wrote 5 tests demanding "the module wins under explicit import," while older tests demand "the facade wins" for the same trigger. The two are mutually exclusive and **impossible to satisfy under any `__init__.py` implementation** (I've empirically confirmed that removing the train branch from `__setattr__` just swaps which 3 fail—it never reaches zero). The research core (`rocket/`, `adr/`, `evolve/`, `vae/mdnrnn/rssm/dreamer`) is ruff+mypy clean. Since it's not a blocker for GPU work, I parked which way to settle the contract as a product decision. **Don't turn failing things into "passing"**—that's the same discipline.

---

## 8. Lessons (gift-to-reader)

- **Scale should be a "config + flag change," not a "rewrite."** Design it that way and you can make the day the GPU box arrives "a day for running experiments" instead of "a day burned on porting." The 3 lines of `device="auto"`, the one `parallel_map` function, the dry-run-by-default bootstrap—no grand machinery needed. What's needed is the will to narrow the swap-point down to one.
- **Measure the bottleneck before you port.** Don't pick your porting target by "probably this is slow." Take a compute map and you find the win isn't one kind but three of different natures (many-core / torch CUDA / MJX), and that the most effective one is the riskiest (Linux-only, unverified). The map decides the order.
- **Don't pretend unverified GPU code "works."** The bigger the candidate win (MJX), the more you want to write it up and say "it's fast." But if you can't verify it locally, what you ship is **a go/no-go gate, not a port.** Deciding "if NO-GO, don't port" up front is the insurance that keeps you from burning days.
- **80% of GPU support is done on CPU.** Device wiring, parallelization, environment bootstrap, numerical-match verification—there's a lot of honest preparation you can do without a GPU. The time spent waiting for a GPU can be time spent preparing rather than waiting.

---

## 9. To be continued

The preparation is done. Next is the episode where **the box arrives and I actually run the day-one procedure**:

- Parallelize all the evolution loops with `--workers`, confirm byte-for-byte match with serial → **the measured speedup factor** (which I don't have yet; I'll put it out honestly with real data from the GPU box).
- Load the world model onto the GPU with `device="auto"`, scaling the tiny preset up to the non-tiny it couldn't run on CPU → where the ConvVAE pixel training tips into being GPU-favorable.
- On Linux, run the MJX go/no-go. **Whether it's `GO` or `NO-GO`—that itself is still unknown.** Does it clear the 5× threshold? Does the contact-rich rocket match the C engine numerically? If it passes, batched physics over thousands of rollouts; if not, stay gracefully on process-parallel and record why.

To repeat honestly, **neither this article's GPU speedup nor its MJX batching has run even once.** What exists now is only "a CPU-verified foundation" and "a gate." That's exactly why, next time, I'll report **whether my predictions held or missed**—with the breakdown—in the same style as when I honestly reported the rocket's draw.

(The code is `onocollo` = world-model core + MuJoCo robot-evolution env + a portable `parallel_map` + `device="auto"` wiring + the go/no-go gate + setup/verify scripts + honest docs, a reusable template. The GPU-box experiments load onto the same shape.)

---

> Note: The source of truth for the plan is `docs/GPU_PLAYBOOK.md` (day-1 procedure and compute map), the MJX gate is `docs/MJX_SCAFFOLD.md`, and the health check is `docs/DEV_BASELINE.md`. The implementation is `scripts/setup_gpu_env.py` / `verify_gpu_env.py`, `src/onocollo/parallel.py`, and `utils.resolve_device`. This article is a draft; the GPU-box experiments have not been run yet.
