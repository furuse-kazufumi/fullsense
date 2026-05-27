# SPDX-License-Identifier: Apache-2.0
"""小PoC #6: factor-subspace QD (Agent A が挙げた限界への対処)。

Agent A の正直な限界: novelty/lexicase は「記述子**全体**の多様性」は保つが、巨大 latent の下では
「**意味次元(factor)の多様性**」は保証しない(factor drift)。
本PoC: 全体 novelty に加え **factor-subspace の novelty を別途課す**と factor 多様性を保護できるか。

モデル(決定論・numpy): genome = [factor(小・意味) | latent(大・中立)]。
- cond A "full-only": novelty = 全 genome の k-NN 距離(latent が支配 → factor は hitchhiking で drift)。
- cond B "full+factor": novelty = 0.5*full + 0.5*factor部分空間の k-NN(factor を明示保護)。
measure: factor_spread(意味次元の std 平均) と latent_spread を世代追跡。
期待: A は factor_spread が縮小(drift)、B は維持。両者とも latent_spread は高い。
"""
from __future__ import annotations
import numpy as np

FDIM, LDIM = 6, 100
POP, GENS, K = 80, 120, 5


def knn_novelty(X: np.ndarray, k: int) -> np.ndarray:
    d = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)
    return np.sort(d, axis=1)[:, 1:k + 1].mean(axis=1)


def spread(X: np.ndarray) -> float:
    return float(X.std(axis=0).mean())


def run(mode: str, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    fac = rng.standard_normal((POP, FDIM))
    lat = rng.standard_normal((POP, LDIM))
    fhist = []
    for _ in range(GENS):
        full = np.concatenate([fac, lat], axis=1)
        if mode == "full_only":
            nov = knn_novelty(full, K)
        else:  # full + factor-subspace
            nov = 0.5 * knn_novelty(full, K) + 0.5 * knn_novelty(fac, K)
        # 最も novel な上位半数を親に、各2子(ガウス変異)
        parents = np.argsort(-nov)[: POP // 2]
        nf, nl = [], []
        for p in parents:
            for _ in range(2):
                nf.append(fac[p] + 0.1 * rng.standard_normal(FDIM))
                nl.append(lat[p] + 0.1 * rng.standard_normal(LDIM))
        fac, lat = np.array(nf[:POP]), np.array(nl[:POP])
        fhist.append(spread(fac))
    return {"mode": mode, "factor_spread_init": round(fhist[0], 3),
            "factor_spread_final": round(fhist[-1], 3),
            "latent_spread_final": round(spread(lat), 3),
            "factor_retention_%": round(100 * fhist[-1] / fhist[0], 1)}


def main():
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"PoC #6: factor-subspace QD (FDIM={FDIM}, LDIM={LDIM}, POP={POP}, GENS={GENS}, 8seed平均)")
    print("-" * 88)
    for mode in ("full_only", "full_plus_factor"):
        agg: dict[str, list] = {}
        for s in range(8):
            for k, v in run(mode, s).items():
                if isinstance(v, (int, float)):
                    agg.setdefault(k, []).append(v)
        m = {k: round(float(np.mean(v)), 3) for k, v in agg.items()}
        print(f"[{mode:16s}] factor_spread {m['factor_spread_init']:.3f}→{m['factor_spread_final']:.3f} "
              f"(retention {m['factor_retention_%']:.1f}%)  latent_spread_final={m['latent_spread_final']:.3f}")
    print("-" * 88)
    print("解釈: full_only で factor_spread が縮小し full_plus_factor で維持されれば、"
          "factor-subspace QD が意味次元多様性を保護=A の限界への有効策(S1 新要件)を proxy 実証。")


if __name__ == "__main__":
    main()
