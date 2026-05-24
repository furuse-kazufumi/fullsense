#!/usr/bin/env python3
"""眼鏡 — 高速化 PoC を批判的に採点する評価レンズ (lleval 流 honest disclosure).

ユーザー指示「単に高速というだけでは、少し疑わないといけない」「lleval のような眼鏡で
PoC する必要もあるかもしれない」に対応。自分で設計した PoC の speedup 数値を**そのまま
信じず**、独立したルーブリックで「速さの裏に何を犠牲にしたか」を採点する。

lleval の honest-disclosure 軸 (latency/quality/stability/safety/honesty + meta) と
judge self-preference 検出を、PoC の**メタ評価**に転用:

* speed だけ高くても、**quality_cost / hidden_cost / generalizability_risk /
  self_preference_risk** が高ければ「採用」してはいけない。
* 全 PoC は simulation/toy → generalizability_risk は最低でも中。実測で再検証するまで
  「速い」は仮説に留める。

採点 (各 0=無/1=中/2=重)。reproducibility のみ 2=良。
``suspicion = quality_cost + hidden_cost + generalizability_risk + self_preference_risk``
(高いほど疑わしい)。``trust`` は suspicion と reproducibility から導く 0..1。

    py -3.11 tools/poc_lens.py
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field


@dataclass(frozen=True)
class PoCEval:
    name: str
    headline: str                 # 主張された速度/効果
    quality_cost: int             # 速さのために犠牲にした品質/正確性 (0..2)
    hidden_cost: int              # 隠れコスト (無駄計算/電力/帯域) (0..2)
    generalizability_risk: int    # toy/sim → 実環境の距離 (0..2)
    self_preference_risk: int     # ベンチを結論に有利に設計していないか (0..2)
    reproducibility: int          # seed 固定 + tests (0..2, 2=良)
    speed_cost_note: str          # 「速さの裏」一言
    flags: tuple[str, ...] = field(default_factory=tuple)

    @property
    def suspicion(self) -> int:
        return (
            self.quality_cost
            + self.hidden_cost
            + self.generalizability_risk
            + self.self_preference_risk
        )

    @property
    def trust(self) -> float:
        # suspicion 0..8 を 0..1 に反転し、reproducibility (0..2) で +/-。clamp [0,1]。
        base = 1.0 - self.suspicion / 8.0
        adj = (self.reproducibility - 1) * 0.1   # repro 2→+0.1, 0→-0.1
        return max(0.0, min(1.0, base + adj))

    @property
    def verdict(self) -> str:
        # 速いだけでは採用しない。汎化/self-pref が高ければ「実測で再検証」必須。
        if self.generalizability_risk >= 2 or self.self_preference_risk >= 2:
            return "実測で再検証 (採用保留)"
        if self.suspicion >= 4:
            return "条件付き (トレードオフ明示)"
        return "有望 (低疑い)"


# 8 PoC を「自分で批判的に」採点 (honest: 自作ベンチの弱みを正直に計上)
REGISTRY: tuple[PoCEval, ...] = (
    PoCEval(
        "Speculative Mesh", "LAN 最大 9.18x",
        quality_cost=0, hidden_cost=2, generalizability_risk=2, self_preference_risk=1,
        reproducibility=2,
        speed_cost_note="miss が latency-neutral でも wasted_compute(電力)大。全 simulation。",
        flags=("simulation-only", "wasted-compute-high-at-low-hit-rate"),
    ),
    PoCEval(
        "Antifragile", "局所最適脱出 0%→100%",
        quality_cost=0, hidden_cost=2, generalizability_risk=2, self_preference_risk=2,
        reproducibility=2,
        speed_cost_note="landscape を panic 有利に設計 (self-pref)。panic 47.7/60 世代=評価爆発。",
        flags=("rigged-toy-landscape", "high-panic-cost", "real-fitness-unmeasured"),
    ),
    PoCEval(
        "適応推論予算 (IBPO)", "44% 計算削減",
        quality_cost=2, hidden_cost=0, generalizability_risk=2, self_preference_risk=1,
        reproducibility=2,
        speed_cost_note="速いだけの罠: 推定器ノイズで精度 65.8% まで低下 (速いが間違える)。",
        flags=("quality-drops-with-noise", "estimator-accuracy-critical"),
    ),
    PoCEval(
        "予測検証ゲート (#1)", "verifier 29-80% 削減",
        quality_cost=1, hidden_cost=0, generalizability_risk=1, self_preference_risk=1,
        reproducibility=2,
        speed_cost_note="有効候補 ~3-4% を誤却下 (良い ChangeOp を失う)。",
        flags=("false-reject-valid-candidates",),
    ),
    PoCEval(
        "KV-cache mesh 差分 (#2)", "LAN 29.85x",
        quality_cost=0, hidden_cost=1, generalizability_risk=2, self_preference_risk=1,
        reproducibility=2,
        speed_cost_note="locality(差分小)を仮定。WAN 全敗。実 KV 一貫性は未検証。",
        flags=("simulation-only", "assumes-high-locality", "lan-only"),
    ),
    PoCEval(
        "Combo-A (Antifragile×Mesh)", "wall-clock W=8→6.82x",
        quality_cost=0, hidden_cost=2, generalizability_risk=2, self_preference_risk=2,
        reproducibility=2,
        speed_cost_note="Antifragile の rigged landscape を継承。並行 peer コスト増。",
        flags=("inherits-rigged-landscape", "peer-cost"),
    ),
    PoCEval(
        "Combo-B (Mesh×KV)", "speedup 2.40x→4.52x",
        quality_cost=0, hidden_cost=1, generalizability_risk=2, self_preference_risk=1,
        reproducibility=2,
        speed_cost_note="2 つの sim を合成 (誤差が乗る)。high-locality 前提。",
        flags=("composed-simulation", "assumes-high-locality"),
    ),
    PoCEval(
        "Combo-C (Antifragile×Gate)", "verifier run 全体 69% 削減",
        quality_cost=1, hidden_cost=0, generalizability_risk=2, self_preference_risk=2,
        reproducibility=2,
        speed_cost_note="panic 比率 (47.7/60) と invalid 90% 仮定に依存。誤却下も継承。",
        flags=("depends-on-panic-ratio-assumption", "false-reject"),
    ),
)


def scorecard_markdown(registry: tuple[PoCEval, ...] = REGISTRY) -> str:
    lines = [
        "| PoC | 主張 | 品質犠牲 | 隠れｺｽﾄ | 汎化ﾘｽｸ | self-pref | trust | verdict |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for p in registry:
        lines.append(
            f"| {p.name} | {p.headline} | {p.quality_cost} | {p.hidden_cost} | "
            f"{p.generalizability_risk} | {p.self_preference_risk} | {p.trust:.2f} | {p.verdict} |"
        )
    return "\n".join(lines)


def _ensure_utf8_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    except Exception:
        pass


def _self_check() -> None:
    # 眼鏡が機能している不変条件を assert で検証 (pytest 非依存)。
    assert all(0 <= p.trust <= 1 for p in REGISTRY)
    # 「単に高速というだけでは疑う」: 全 PoC が simulation/toy なので汎化ﾘｽｸ>=1。
    assert all(p.generalizability_risk >= 1 for p in REGISTRY)
    # self-preference が重い PoC は「採用保留」になる (速くても)。
    rigged = next(p for p in REGISTRY if p.name == "Antifragile")
    assert rigged.self_preference_risk == 2
    assert rigged.verdict == "実測で再検証 (採用保留)"
    # 「速いだけの罠」: 適応推論予算は品質犠牲が重い。
    ibpo = next(p for p in REGISTRY if "IBPO" in p.name)
    assert ibpo.quality_cost == 2
    # どの PoC も trust=1.0 (無条件採用) にはならない (全 sim なので)。
    assert max(p.trust for p in REGISTRY) < 1.0


@dataclass(frozen=True)
class Fragility:
    """各 PoC の verdict が依存する仮定パラメータと、崩れる地点 (感度分析)."""

    name: str
    parameter: str
    assumed: str
    breakeven: str
    fragile: bool
    note: str


# 全速度 PoC は「推定器精度 / 環境」を仮定値で置いている。verdict が仮定から
# どれだけ離れて flip するか = 脆弱性。眼鏡が最も flag した「estimator-accuracy-critical」。
FRAGILITY: tuple[Fragility, ...] = (
    Fragility(
        "Speculative Mesh", "hit_rate + fast-fallback", "hit~0.7 / 即時 fallback",
        "break-even hit 0.34 (slow-fallback 20ms)", True,
        "fast-fallback 必須。timeout が入ると break-even 上昇 → 低 hit で負ける。",
    ),
    Fragility(
        "Antifragile", "exploration_multiplier + landscape 形状", "mult=8 / panic 有利 toy",
        "mult>1 で脱出 (mult=1 は失敗)", True,
        "脱出は landscape 形状依存。rigged toy のため実 fitness で再評価必須。",
    ),
    Fragility(
        "適応推論予算 (IBPO)", "confidence 推定器ノイズ", "noise≈0 を仮定",
        "noise~0.025 で精度<95%", True,
        "推定器が少しノイズると品質が崩れる。最も脆い (要較正 calibration)。",
    ),
    Fragility(
        "予測検証ゲート (#1)", "gate recall / invalid_rate", "recall 0.9 / invalid 0.6",
        "recall が cheap/verify 比超で正 (≈常に成立)", False,
        "コスト削減は頑健。ただし lost_valid ~3-4% の floor は残る。",
    ),
    Fragility(
        "KV-cache 差分 (#2)", "locality(diff_ratio) / 帯域", "LAN / 差分小",
        "LAN break-even diff 1.0 (常勝) / WAN <0.01", False,
        "LAN なら locality に頑健。WAN は構造的に死亡。",
    ),
)


def fragility_markdown() -> str:
    lines = ["| PoC | 仮定 | break-even (flip 点) | 脆弱? |", "|---|---|---|---|"]
    for f in FRAGILITY:
        lines.append(
            f"| {f.name} | {f.parameter}={f.assumed} | {f.breakeven} | "
            f"{'⚠️ 脆い' if f.fragile else '頑健'} |"
        )
    return "\n".join(lines)


def main() -> None:
    _ensure_utf8_stdout()
    _self_check()
    print("# 眼鏡 — 高速化 PoC メタ評価 (単に高速 ≠ 採用)\n")
    print("採点: 0=無 / 1=中 / 2=重。trust 0..1 (高いほど信頼)。全 PoC simulation/toy。\n")
    print(scorecard_markdown())
    print("\n## 速さの裏 (各 PoC が速度のために払うもの)\n")
    for p in REGISTRY:
        print(f"- **{p.name}**: {p.speed_cost_note}")
    print("\n## 眼鏡の結論\n")
    print("- どの PoC も **trust=1.0 (無条件採用) にならない** — 全て simulation/toy。")
    print("- self-preference が重い (Antifragile / Combo-A,C) は **実測で再検証するまで採用保留**。")
    print("- 適応推論予算は『速いが間違える』罠 — 推定器精度の floor がないと品質が崩れる。")
    print("- **速い結果ほど内訳を疑い、実 transport/executor/fitness 配線後の実測で上書きする。**")


if __name__ == "__main__":
    main()
