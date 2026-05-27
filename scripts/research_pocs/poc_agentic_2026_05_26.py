# SPDX-License-Identifier: Apache-2.0
"""小PoC #5: 調査機能を持つ agentic 個体 (S3, AGENT 軸)。

問い: 個体に「調査機能」(知らない事実を読取専用KBに問い合わせて答える)を与えると、
  (1) 調査コスト λ が「選択的調査」(価値の高い gap だけ調べる)を**創発**させ、
  (2) 無条件調査(always)・調査なし(never)の両極を上回り、
  (3) 進化が最適閾値 θ*≈λ·c を自力で見つけるか。
= AGENT-3「調査はコスト計上(無料だと無限調査に退化)」の検証。

モデル(決定論・numpy): F 事実, 各事実 f に価値 v[f]。各個体は innate に一部の事実を知る(継承)。
genome = θ(調査の価値閾値)。タスク=全 F 事実を解く。
  知っている → reward v[f], コスト0 / 知らない & v[f]>θ → 調査して reward v[f]-λc / それ以外 → 0。
最適 θ* = λc (価値がコストを超える gap だけ調べる)。進化が θ→λc を見つければ「賢い調査」創発。
"""
from __future__ import annotations
import numpy as np

F = 40            # 事実数
POP = 60
GENS = 150
C = 1.0           # 調査の基礎コスト
ALPHA = 0.4       # innate に知っている事実の割合


def fitness_of(theta: np.ndarray, knows: np.ndarray, v: np.ndarray, lam: float) -> np.ndarray:
    """各個体の総 reward。theta:(P,) knows:(P,F) v:(F,)"""
    P = theta.shape[0]
    rew = np.zeros(P)
    for i in range(P):
        for f in range(F):
            if knows[i, f]:
                rew[i] += v[f]
            elif v[f] > theta[i]:           # 価値が閾値超→調査
                rew[i] += v[f] - lam * C
            # else: 調べない=0
    return rew


def evolve(lam: float, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    v = rng.random(F)
    theta = rng.random(POP) * 1.0           # 初期 θ ∈ [0,1]
    knows = rng.random((POP, F)) < ALPHA    # innate 知識(継承される)
    for _ in range(GENS):
        rew = fitness_of(theta, knows, v, lam)
        # トーナメント選択 + elitism
        order = np.argsort(-rew)
        elite = order[:2]
        new_theta = list(theta[elite])
        new_knows = list(knows[elite])
        while len(new_theta) < POP:
            i, j = rng.integers(0, POP, 2)
            w = i if rew[i] >= rew[j] else j
            new_theta.append(np.clip(theta[w] + 0.05 * rng.standard_normal(), 0, 1.5))
            km = knows[w].copy()
            flip = rng.random(F) < 0.01       # 知識も僅かに変異(獲得/忘却)
            km[flip] = ~km[flip]
            new_knows.append(km)
        theta = np.array(new_theta)
        knows = np.array(new_knows)
    rew = fitness_of(theta, knows, v, lam)
    # baseline: 同じ最終 knows で θ=0(always 調査) / θ=∞(never 調査)
    always = fitness_of(np.zeros(POP), knows, v, lam)
    never = fitness_of(np.full(POP, 9.0), knows, v, lam)
    return {
        "lam": lam,
        "theta_opt(=lam*c)": round(lam * C, 3),
        "theta_evolved_mean": round(float(theta.mean()), 3),
        "fitness_evolved": round(float(rew.mean()), 2),
        "fitness_always": round(float(always.mean()), 2),
        "fitness_never": round(float(never.mean()), 2),
        "theta_std(diversity)": round(float(theta.std()), 3),
    }


def main():
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"PoC #5: agentic 個体の選択的調査 (F={F}, POP={POP}, GENS={GENS}, c={C}, innate α={ALPHA})")
    print("-" * 92)
    for lam in (0.0, 0.3, 0.6, 0.9):
        r = evolve(lam)
        print(f"λ={r['lam']:.1f} | θ*={r['theta_opt(=lam*c)']:.2f} θ_eflved={r['theta_evolved_mean']:.3f} "
              f"| fit: evolved={r['fitness_evolved']:.2f} always={r['fitness_always']:.2f} "
              f"never={r['fitness_never']:.2f} | θ_std={r['theta_std(diversity)']:.3f}")
    print("-" * 92)
    print("解釈: θ_evolved が θ*=λc を追えば『コストに見合う調査だけ』を進化が自力獲得。"
          "evolved ≥ max(always, never) なら選択的調査が両極より優位＝AGENT-3 成立。")


if __name__ == "__main__":
    main()
