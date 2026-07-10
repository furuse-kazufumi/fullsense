# SPDX-License-Identifier: Apache-2.0
"""Qiita #48 spikelab section figures, generated from real spikelab simulations.

Labels are in English (avoid matplotlib JP font tofu); prose explains in Japanese.
Run: PYTHONPATH=D:/projects/spikelab/src python make_spikelab_figures.py
"""
from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from spikelab import (
    LIF,
    Network,
    Projection,
    ShortTermPlasticity,
    SpikeMonitor,
    STDP,
    SurrogateSNN,
    to_numpy,
)

OUT = os.path.dirname(os.path.abspath(__file__))
EXC = "#2b8cbe"
POT = "#2ca25f"
DEP = "#de2d26"
plt.rcParams.update({"figure.dpi": 120, "font.size": 11, "axes.grid": True,
                     "grid.alpha": 0.3, "axes.spines.top": False, "axes.spines.right": False})


def fig_membrane():
    grp = LIF(1, tau_m=20.0, v_thresh=-50.0, v_reset=-65.0, refractory_ms=3.0)
    dt, steps = 0.1, 1200
    vs = []
    for _ in range(steps):
        s = bool(to_numpy(grp.step(18.0, dt))[0])
        v = float(to_numpy(grp.v)[0])
        vs.append(20.0 if s else v)
    t = np.arange(steps) * dt
    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.plot(t, vs, color=EXC, lw=1.4)
    ax.axhline(-50.0, color=DEP, ls="--", lw=1, label="threshold")
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("membrane V (mV)")
    ax.set_title("LIF neuron: integrate, fire, reset (spikelab, CPU)")
    ax.legend(loc="upper right", frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "membrane_trace.png"))
    plt.close(fig)


def fig_raster():
    rng = np.random.default_rng(1)
    n_in, n_out = 40, 30
    src, dst = LIF(n_in, refractory_ms=2.0), LIF(n_out, refractory_ms=3.0)
    w = (rng.random((n_out, n_in)) < 0.15) * 45.0
    net = Network()
    net.connect(src, dst, w, delay_ms=1.5, tau_syn=6.0)
    m_src = net.add_monitor(SpikeMonitor(src))
    m_dst = net.add_monitor(SpikeMonitor(dst))
    dt, steps = 0.1, 3000
    for _ in range(steps):
        drive = 14.0 + 8.0 * rng.standard_normal(n_in)
        net.run(dt, dt_ms=dt, inputs={src: drive})
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.scatter(m_src.spike_times, m_src.spike_indices, s=3, color=EXC, label="input layer")
    ax.scatter(m_dst.spike_times, m_dst.spike_indices + n_in, s=3, color=POT, label="output layer")
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("neuron index")
    ax.set_title("Spike raster: noise-driven input drives an output layer (spikelab)")
    ax.legend(loc="upper right", frameon=False, markerscale=3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "raster.png"))
    plt.close(fig)


def measure_dw(dt_pair_ms, w0=0.5, dt=0.1):
    pre, post = LIF(1), LIF(1)
    proj = Projection(pre, post, np.array([[w0]]))
    rule = STDP(proj, a_plus=0.01, a_minus=0.012, tau_pre=20.0, tau_post=20.0)
    gap = int(round(abs(dt_pair_ms) / dt))
    pre_step, post_step = (0, gap) if dt_pair_ms >= 0 else (gap, 0)
    for k in range(gap + 1):
        rule.update(np.array([1.0]) if k == pre_step else np.array([0.0]),
                    np.array([1.0]) if k == post_step else np.array([0.0]), dt)
    return float(to_numpy(proj.w)[0, 0]) - w0


def fig_stdp():
    xs = np.arange(-40.0, 40.1, 2.0)
    dws = np.array([measure_dw(float(x)) for x in xs])
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axhline(0, color="gray", lw=0.8)
    ax.axvline(0, color="gray", lw=0.8)
    ax.plot(xs[xs > 0], dws[xs > 0], "o-", color=POT, label="LTP (pre before post)")
    ax.plot(xs[xs < 0], dws[xs < 0], "o-", color=DEP, label="LTD (post before pre)")
    ax.fill_between(xs[xs > 0], 0, dws[xs > 0], color=POT, alpha=0.15)
    ax.fill_between(xs[xs < 0], 0, dws[xs < 0], color=DEP, alpha=0.15)
    ax.set_xlabel("dt = t_post - t_pre (ms)")
    ax.set_ylabel("weight change dw")
    ax.set_title("STDP learning window (spikelab, real sim output)")
    ax.legend(loc="upper left", frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "stdp_window.png"))
    plt.close(fig)


def fig_surrogate():
    u = np.linspace(-1.5, 3.5, 400)
    beta = 3.0
    sig = 1.0 / (1.0 + np.exp(-beta * (u - 1.0)))
    hard = (u >= 1.0).astype(float)
    sg = beta * sig * (1.0 - sig)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(u, hard, color="#555", lw=2, label="forward: hard spike")
    ax.plot(u, sig, color=EXC, lw=2, ls="--", label="smooth spike (logistic)")
    ax.plot(u, sg / sg.max(), color=DEP, lw=2, label="backward: surrogate gradient")
    ax.axvline(1.0, color="gray", lw=0.8)
    ax.set_xlabel("membrane potential u (threshold = 1)")
    ax.set_ylabel("value")
    ax.set_title("Surrogate gradient: step forward, smooth backward (spikelab)")
    ax.legend(loc="center left", frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "surrogate.png"))
    plt.close(fig)


def fig_learning():
    steps_t, n_in = 12, 6
    pat_a = np.zeros((steps_t, n_in))
    pat_a[:, :2] = 1.0
    pat_b = np.zeros((steps_t, n_in))
    pat_b[:, 4:] = 1.0
    tgt_a, tgt_b = np.array([3.0, 0.0]), np.array([0.0, 3.0])
    net = SurrogateSNN(n_in, 8, 2, mem_decay=0.9, surrogate_beta=5.0, seed=11)
    losses = []
    for step in range(300):
        if step % 2 == 0:
            net.train_step(pat_a, tgt_a, lr=0.02)
        else:
            net.train_step(pat_b, tgt_b, lr=0.02)
        la = net.loss_and_grads(pat_a, tgt_a, hard=True)[0]
        lb = net.loss_and_grads(pat_b, tgt_b, hard=True)[0]
        losses.append(la + lb)
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.plot(losses, color=EXC, lw=1.8)
    ax.set_xlabel("training step")
    ax.set_ylabel("total loss (MSE of spike counts)")
    ax.set_title("Surrogate-gradient SNN learns a 2-pattern task on CPU (spikelab)")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "learning_curve.png"))
    plt.close(fig)


def fig_stp():
    dt, isi_steps, n_spikes = 0.1, 200, 8
    fig, ax = plt.subplots(figsize=(7, 3.6))
    configs = [("depressing", dict(U=0.6, tau_facil=0.0, tau_rec=300.0), DEP),
               ("facilitating", dict(U=0.15, tau_facil=200.0, tau_rec=150.0), POT)]
    for label, kw, col in configs:
        stp = ShortTermPlasticity(1, **kw)
        eff = []
        for i in range(n_spikes * isi_steps):
            spk = np.array([1.0]) if i % isi_steps == 0 else np.array([0.0])
            e = float(to_numpy(stp.transmit(spk, dt))[0])
            if i % isi_steps == 0:
                eff.append(e)
        ax.plot(range(1, n_spikes + 1), np.array(eff) / eff[0], "o-", color=col, label=label)
    ax.set_xlabel("spike number in train")
    ax.set_ylabel("relative efficacy (norm. to 1st)")
    ax.set_title("Short-term plasticity: same synapse, opposite dynamics (spikelab)")
    ax.legend(loc="center right", frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "short_term_plasticity.png"))
    plt.close(fig)


def main():
    fig_membrane()
    fig_raster()
    fig_stdp()
    fig_surrogate()
    fig_learning()
    fig_stp()
    print("wrote figures to", OUT)
    for f in sorted(os.listdir(OUT)):
        if f.endswith(".png"):
            print(" ", f, os.path.getsize(os.path.join(OUT, f)), "bytes")


if __name__ == "__main__":
    main()
