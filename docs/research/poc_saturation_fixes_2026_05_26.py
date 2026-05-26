# SPDX-License-Identifier: Apache-2.0
"""小PoC: 固定ものさしの飽和 vs 適応難易度(Red Queen)の勾配維持。

12h ラン分析の核心(「眼鏡=固定 quiz が飽和すると選択圧が消える」)を最小モデルで
isolate して再現し、Perplexity Q4 の核心レシピ(条件カリキュラム=難易度を集団に追従)が
飽和を回避するかを検証する。Agent A(選択演算子の sweep)とは直交(こちらは fitness/難易度側)。

決定論・numpy のみ・実 LLM 無し。各個体 = 5 軸の competence ベクトル c∈[0,1]^5。
軸 i のタスク: pass if c_i >= 難易度 d_i。total = 平均 pass 率。
- baseline: d 固定(易しい, multistep だけ難) → c が閾値超え後は報酬が増えず飽和。
- adaptive: d_i = 集団の c_i の p 分位 → 常に ~ (1-p) が pass → 中央超えに勾配 → c が登り続ける。
"""
from __future__ import annotations
import numpy as np

N_AXES = 5
POP = 24
GENS = 200
RNG = np.random.default_rng(0)


def evaluate(pop: np.ndarray, d: np.ndarray) -> np.ndarray:
    """各個体の total score = 軸別 pass(c_i>=d_i) の平均."""
    return (pop >= d[None, :]).mean(axis=1)


def evolve(mode: str) -> dict:
    rng = np.random.default_rng(0)
    # founder: 全員ほぼ同一(12h ラン同様 founder 同質) + 微小ノイズ
    pop = np.clip(0.3 + 0.02 * rng.standard_normal((POP, N_AXES)), 0, 1)
    # baseline 固定難易度: 4 軸は易しい(0.3), multistep 相当 1 軸だけ難(0.7)
    d_fixed = np.array([0.3, 0.3, 0.7, 0.3, 0.3])
    hist_best, hist_mean, hist_div = [], [], []
    for g in range(GENS):
        if mode == "baseline_fixed":
            d = d_fixed
        elif mode in ("adaptive_difficulty", "adaptive_plus_novelty"):
            # 条件カリキュラム: 各軸の難易度 = 集団 competence の 60 分位(常に ~40% pass)
            d = np.quantile(pop, 0.60, axis=0)
        else:
            raise ValueError(mode)
        scores = evaluate(pop, d)
        # novelty = 行動空間(=competence)での k-NN 平均距離(多様性維持の選択圧)
        if mode == "adaptive_plus_novelty":
            dist = np.linalg.norm(pop[:, None, :] - pop[None, :, :], axis=2)
            novelty = np.sort(dist, axis=1)[:, 1:6].mean(axis=1)  # 5-NN
        else:
            novelty = None
        # 観測は「真の能力」(難易度非依存) = c の平均。飽和すると能力が伸び止まる。
        true_cap = pop.mean(axis=1)
        hist_best.append(float(true_cap.max()))
        hist_mean.append(float(true_cap.mean()))
        hist_div.append(float(np.linalg.norm(pop - pop.mean(0), axis=1).mean()))
        # トーナメント選択 + elitism + ガウス変異
        new = [pop[int(np.argmax(scores))].copy()]  # elite(選択信号=score 最大; 交絡除去)
        while len(new) < POP:
            i, j = rng.integers(0, POP, 2)
            # adaptive_plus_novelty は子の半分を novelty トーナメントで選ぶ(50/50 quality/novelty)
            if novelty is not None and len(new) % 2 == 0:
                winner = pop[i] if novelty[i] >= novelty[j] else pop[j]
            else:
                winner = pop[i] if scores[i] >= scores[j] else pop[j]
            child = np.clip(winner + 0.05 * rng.standard_normal(N_AXES), 0, 1)
            new.append(child)
        pop = np.array(new)
    return {
        "mode": mode,
        "final_mean_cap": hist_mean[-1],
        "final_best_cap": hist_best[-1],
        "mean_cap_gen10": hist_mean[10],
        "mean_cap_gen50": hist_mean[50],
        "plateau_gen": _plateau_gen(hist_mean),
        "final_div": hist_div[-1],
    }


def _plateau_gen(series: list[float], eps: float = 1e-3, window: int = 20) -> int:
    """平均能力が window 世代 eps 未満しか伸びなくなった最初の世代(=飽和点)."""
    for g in range(window, len(series)):
        if series[g] - series[g - window] < eps:
            return g
    return -1  # 飽和せず


def main() -> None:
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"PoC: 固定ものさし飽和 vs 適応難易度 (POP={POP}, GENS={GENS}, axes={N_AXES})")
    print("-" * 78)
    for mode in ("baseline_fixed", "adaptive_difficulty", "adaptive_plus_novelty"):
        r = evolve(mode)
        print(f"[{mode:22s}] final_mean_cap={r['final_mean_cap']:.3f} "
              f"best={r['final_best_cap']:.3f} "
              f"gen10={r['mean_cap_gen10']:.3f} gen50={r['mean_cap_gen50']:.3f} "
              f"plateau@gen={r['plateau_gen']} div={r['final_div']:.3f}")
    print("-" * 78)
    print("期待: baseline は早期に plateau(能力が閾値超えで伸び止まる) / "
          "adaptive は plateau せず能力が登り続ける(Red Queen=勾配維持)。")


if __name__ == "__main__":
    main()
