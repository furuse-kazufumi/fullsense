# SPDX-License-Identifier: Apache-2.0
"""小PoC #4: ORCH 最大の穴 — 実ルーター(非oracle)は oracle best_of に近づけるか。

Agent C + 自己PoC#3 の一致結論: MoA が単一bestを上回るのは competence-aware routing(best_of)
の時だけ、投票(majority)では届かない。ただし best_of は **oracle**(正答個体を完璧routing)の上限。
本PoC: **現実的なルーター**が oracle にどこまで近づくかを測る。
  - confidence-router: 各 sub-skill で最も自信のあるメンバへ routing(較正品質 κ に依存)。
  - specialty-router: behavior descriptor(=どのドメインの専門家か)で routing。
        ← QD 用に既に計算する記述子が routing キーに使える相乗効果の検証。
  - majority(baseline) / oracle best_of(上限) と比較。

決定論・numpy。専門家分散集団(自己PoC#3 同型)。
"""
from __future__ import annotations
import numpy as np

M_SKILLS, G_DOMAINS = 20, 4
PER = M_SKILLS // G_DOMAINS
POP, K = 24, 4
HI, LO = 0.85, 0.20  # 専門ドメイン / 専門外の正答確率


def build(seed: int):
    rng = np.random.default_rng(seed)
    specialty = np.zeros((POP, G_DOMAINS), dtype=bool)   # 各個体の専門ドメイン(=記述子)
    comp = np.full((POP, M_SKILLS), LO)
    for i in range(POP):
        for g in rng.choice(G_DOMAINS, size=int(rng.integers(1, 3)), replace=False):
            specialty[i, g] = True
            comp[i, g * PER:(g + 1) * PER] = HI
    # 実際の正誤を sample(決定論)
    correct = (rng.random((POP, M_SKILLS)) < comp).astype(int)
    return rng, specialty, comp, correct


def select_diverse(specialty, correct, k):
    """max-coverage greedy(自己PoC#3 同型, 記述子=specialty で被覆)."""
    chosen, covered = [], np.zeros(M_SKILLS, dtype=bool)
    for _ in range(k):
        best_i, best_gain = -1, -1
        for i in range(POP):
            if i in chosen:
                continue
            gain = int((correct[i].astype(bool) & ~covered).sum())
            if gain > best_gain:
                best_gain, best_i = gain, i
        chosen.append(best_i); covered |= correct[best_i].astype(bool)
    return chosen


def domain_of(m):
    return m // PER


def evaluate(seed: int, kappa: float) -> dict:
    rng, specialty, comp, correct = build(seed)
    members = select_diverse(specialty, correct, K)
    cm = correct[members]                     # (K, M) 実正誤
    spec = specialty[members]                 # (K, G)
    # confidence: 較正品質 κ。κ=1 で正誤を反映, κ=0 で乱数。
    conf = kappa * cm + (1 - kappa) * rng.random((K, M_SKILLS))
    single_best = max(members, key=lambda i: correct[i].sum())
    res = {"single_best": float(correct[single_best].mean()),
           "oracle_best_of": float(cm.any(axis=0).mean()),
           "majority": float((cm.sum(axis=0) > K / 2).mean())}
    # confidence-router: sub-skill 毎に最自信メンバの正誤
    pick = conf.argmax(axis=0)
    res["conf_router"] = float(cm[pick, np.arange(M_SKILLS)].mean())
    # specialty-router: sub-skill m のドメイン専門メンバへ(複数なら最初, 不在なら最自信)
    sp = []
    for m in range(M_SKILLS):
        g = domain_of(m)
        cand = [k for k in range(K) if spec[k, g]]
        k = cand[0] if cand else int(conf[:, m].argmax())
        sp.append(cm[k, m])
    res["specialty_router"] = float(np.mean(sp))
    return res


def main():
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"PoC #4: 実ルーターは oracle best_of に近づけるか (POP={POP}, K={K}, seeds平均)")
    print("-" * 86)
    seeds = range(20)
    for kappa in (0.0, 0.3, 0.6, 0.9):
        agg: dict[str, list] = {}
        for s in seeds:
            for k2, v in evaluate(s, kappa).items():
                agg.setdefault(k2, []).append(v)
        m = {k2: np.mean(v) for k2, v in agg.items()}
        print(f"κ={kappa:.1f} | single={m['single_best']:.3f} majority={m['majority']:.3f} "
              f"conf_router={m['conf_router']:.3f} specialty_router={m['specialty_router']:.3f} "
              f"oracle={m['oracle_best_of']:.3f}")
    print("-" * 86)
    print("解釈: conf_router が κ↑で oracle に近づけば「較正された自信で routing 可能」。"
          "specialty_router(記述子routing)が majority/single を安定して上回れば QD記述子が routingキーに流用可。")


if __name__ == "__main__":
    main()
