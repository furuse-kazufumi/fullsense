# SPDX-License-Identifier: Apache-2.0
"""小PoC: ORCH-4 を headroom のある難タスクで検証(C の proxy は飽和で判定不能だった)。

問い: 単一個体が満点を取れない「専門家が分散した難タスク」で、
  - 多様な MoA アンサンブル > 単一 best か?
  - 多様性選抜 > 冗長選抜 か? (Self-MoA 反証=多様性は自動優位でない を踏まえ正直に)

モデル(決定論・numpy): M=20 sub-skill を G=4 ドメイン(各5)に分割。各個体は 1-2 ドメインの
specialist(その範囲だけ competence 高)。タスク=全 M sub-question。個体 m を正答する条件は
competence[m] >= 0.5。
- single_best = 総 competence 最大個体 (≈ 1-2 ドメインしかカバーできず満点不可)。
- MoA best-of(=oracle routing): sub-skill 毎に「メンバの誰か1人でも competent なら正答」。
- MoA majority: sub-skill 毎にメンバ過半が competent なら正答(より厳しい)。
- diverse 選抜 = ドメイン被覆を最大化する greedy / redundant 選抜 = 総スコア top-k。
"""
from __future__ import annotations
import numpy as np

M_SKILLS = 20
G_DOMAINS = 4
PER = M_SKILLS // G_DOMAINS
POP = 24
K = 4
RNG = np.random.default_rng(7)


def make_population() -> np.ndarray:
    """各個体 = M 次元 competence。1-2 ドメインに specialize。"""
    pop = np.zeros((POP, M_SKILLS))
    for i in range(POP):
        n_dom = RNG.integers(1, 3)  # 1 or 2 domains
        doms = RNG.choice(G_DOMAINS, size=n_dom, replace=False)
        for dgi in doms:
            sl = slice(dgi * PER, (dgi + 1) * PER)
            pop[i, sl] = np.clip(0.8 + 0.15 * RNG.standard_normal(PER), 0, 1)  # strong in-domain
        # 弱い汎用能力
        pop[i] = np.maximum(pop[i], np.clip(0.15 + 0.1 * RNG.standard_normal(M_SKILLS), 0, 1))
    return pop


def solves(vec: np.ndarray) -> np.ndarray:
    return vec >= 0.5  # bool per sub-skill


def score_single(vec: np.ndarray) -> float:
    return float(solves(vec).mean())


def domain_coverage(members: np.ndarray) -> int:
    """メンバ集合が competent なドメイン数(diversity 指標)."""
    covered = 0
    for g in range(G_DOMAINS):
        sl = slice(g * PER, (g + 1) * PER)
        if solves(members[:, sl]).any():
            covered += 1
    return covered


def moa_best_of(members: np.ndarray) -> float:
    """sub-skill 毎に誰か1人でも解ければ正答(oracle routing の上限)."""
    return float(solves(members).any(axis=0).mean())


def moa_majority(members: np.ndarray) -> float:
    """sub-skill 毎にメンバ過半が解ければ正答(厳しい集約)."""
    return float((solves(members).sum(axis=0) > members.shape[0] / 2).mean())


def select_redundant(pop: np.ndarray, k: int) -> np.ndarray:
    totals = solves(pop).sum(axis=1)
    idx = np.argsort(-totals)[:k]
    return pop[idx]


def select_diverse(pop: np.ndarray, k: int) -> np.ndarray:
    """greedy max-coverage: 既選択が解けない sub-skill を最も補う個体を順に選ぶ."""
    chosen: list[int] = []
    covered = np.zeros(M_SKILLS, dtype=bool)
    for _ in range(k):
        best_i, best_gain = -1, -1
        for i in range(POP):
            if i in chosen:
                continue
            gain = int((solves(pop[i]) & ~covered).sum())
            if gain > best_gain:
                best_gain, best_i = gain, i
        chosen.append(best_i)
        covered |= solves(pop[best_i])
    return pop[chosen]


def main() -> None:
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    pop = make_population()
    sb = max(range(POP), key=lambda i: score_single(pop[i]))
    print(f"PoC ORCH-4 (headroom 有り難タスク, M={M_SKILLS}, domains={G_DOMAINS}, POP={POP}, K={K})")
    print("-" * 78)
    print(f"single_best         : score={score_single(pop[sb]):.3f} "
          f"(coverage={domain_coverage(pop[sb:sb+1])}/{G_DOMAINS})  <- 満点取れない=headroom 有り")
    for name, sel in (("redundant(top-k)", select_redundant), ("diverse(max-cover)", select_diverse)):
        members = sel(pop, K)
        print(f"MoA {name:18s}: best_of={moa_best_of(members):.3f} "
              f"majority={moa_majority(members):.3f} coverage={domain_coverage(members)}/{G_DOMAINS}")
    print("-" * 78)
    print("解釈: single_best < 1.0(headroom 有り)の難タスクで, diverse MoA(best_of)が単一 best を"
          "上回れば ORCH-4 成立。majority は厳しく, 冗長選抜との差が diversity の価値。")


if __name__ == "__main__":
    main()
