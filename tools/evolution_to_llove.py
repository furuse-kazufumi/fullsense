# SPDX-License-Identifier: Apache-2.0
"""進化ラン metrics.jsonl → llove Event JSONL 変換ブリッジ (スキーマ不一致解消).

llive の進化ラン出力 (``metrics.jsonl``: 各行 generation/best_score/mean_score/
std_score/median_score/diversity_l2) を **llove が読める Event 形式** (各行 ``kind``
付き, :class:`llove.events.EventKind`) に変換する。

背景
----
``llove tail <file>`` は :class:`llove.sources.jsonl.JSONLSource` を使い、各行に
``kind`` (EventKind enum 値) が無いと**全行を読み飛ばす**。進化ランの metrics.jsonl は
``kind`` を持たないため、そのままでは llove で「何も流れない」。本ブリッジが両者を
**疎結合**でつなぐ (llive / llove 本体は一切改変しない = 独立性原則
feedback_independence_principle)。

変換ルール
----------
各世代を 3〜4 本の SENSOR イベントに展開する:
  - ``best_score`` / ``mean_score`` / ``diversity_l2`` (時系列メトリクス)
  - ``monoculture_ratio`` (founder_lineage.jsonl から算出した最大系統占有率)
さらに **系統が 2 以下 or 占有率 ≥ 0.8 になった世代に SPC_ALARM** を発火し
(FullSense らしく「多様性崩壊」を異常検知として可視化)、冒頭/末尾に NARRATION で
honest disclosure ラベルと見極め所見を焼き込む (feedback_benchmark_honest_disclosure)。

使い方
------
    py -3.11 tools/evolution_to_llove.py <run_dir> [--out events.jsonl]
    # 例:
    py -3.11 tools/evolution_to_llove.py D:/projects/llive/out/evo_seekvalue_2026_05_25
    llove tail D:/projects/llive/out/evo_seekvalue_2026_05_25/llove_events.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

# UTF-8 stdout (Windows cp932 対策, feedback_cli_utf8_stdout_pattern)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 擬似タイムスタンプ基点 (進化ランは wallclock を記録しないので世代→秒で合成)。
_BASE_TS = datetime(2026, 1, 1, tzinfo=UTC)
_TICK = timedelta(seconds=1)

# monoculture 警報の閾値 (要件 OE-3: 単一系統 >80% 占有 / 系統 2 以下)。
_MONOCULTURE_SHARE = 0.8
_MONOCULTURE_LINEAGES = 2

_SENSORS = ("best_score", "mean_score", "diversity_l2")


def _load_jsonl(path: Path) -> list[dict]:
    """JSONL を dict のリストに (ファイル無し/壊れ行は握り潰し、空リストを返す)."""
    rows: list[dict] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            rows.append(obj)
    return rows


def _emit(kind: str, ts: datetime, **payload: object) -> str:
    """1 行の llove Event JSONL を組み立てる (kind + ts + source_id + payload フィールド).

    JSONLSource は ``payload`` キーが無ければ残りのフィールド全てを payload とみなすので、
    payload フィールドはトップレベルにフラットに置く。
    """
    rec: dict[str, object] = {"kind": kind, "ts": ts.isoformat(), "source_id": "evolution"}
    rec.update(payload)
    return json.dumps(rec, ensure_ascii=False)


def convert(run_dir: Path) -> list[str]:
    """run_dir の進化出力を llove Event JSONL 行のリストに変換する."""
    metrics = _load_jsonl(run_dir / "metrics.jsonl")
    if not metrics:  # checkpoint 刻みだが generations.jsonl でも代替可
        metrics = _load_jsonl(run_dir / "generations.jsonl")
    if not metrics:
        raise FileNotFoundError(
            f"no metrics.jsonl / generations.jsonl in {run_dir}"
        )

    lineage = {
        r["generation"]: r.get("founder_counts", {})
        for r in _load_jsonl(run_dir / "founder_lineage.jsonl")
        if "generation" in r
    }

    manifest: dict = {}
    mp = run_dir / "run_manifest.json"
    if mp.exists():
        try:
            manifest = json.loads(mp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            manifest = {}
    is_proxy = str(manifest.get("fitness", "proxy")) != "llm"
    label = "PROXY fitness — NOT real LLM eval" if is_proxy else "real on-prem LLM fitness"

    lines: list[str] = []
    lines.append(
        _emit(
            "narration",
            _BASE_TS,
            text=f"llive persona evolution — {label}  ·  gens={len(metrics)}",
        )
    )

    alarmed = False
    for i, r in enumerate(metrics):
        g = int(r.get("generation", i))
        ts = _BASE_TS + _TICK * (i + 1)

        for sid in _SENSORS:
            if sid in r:
                lines.append(_emit("sensor", ts, sensor_id=sid, value=round(float(r[sid]), 4)))

        counts = lineage.get(g)
        if counts:
            total = sum(counts.values()) or 1
            share = max(counts.values()) / total
            n_lineages = len(counts)
            lines.append(_emit("sensor", ts, sensor_id="monoculture_ratio", value=round(share, 4)))
            if (share >= _MONOCULTURE_SHARE or n_lineages <= _MONOCULTURE_LINEAGES) and not alarmed:
                # 最初に崩壊した世代でのみ 1 度 SPC_ALARM (連続発火で埋もれさせない)。
                lines.append(
                    _emit(
                        "spc_alarm",
                        ts,
                        sensor_id="monoculture_ratio",
                        cusum=round(share, 4),
                        note=f"gen{g}: 系統 {n_lineages} に収束 (top share {share:.0%}) — 多様性崩壊",
                    )
                )
                alarmed = True

    last = metrics[-1]
    final_counts = lineage.get(int(last.get("generation", 0)), {})
    div = float(last.get("diversity_l2", 0.0))
    lines.append(
        _emit(
            "narration",
            _BASE_TS + _TICK * (len(metrics) + 1),
            text=(
                f"結論: best={last.get('best_score')} (飽和), diversity_l2={div:.2f}, "
                f"最終系統数={len(final_counts)}. open-endedness 未達 — "
                f"novelty/QD/per-dim 標準化の配線が前提."
            ),
        )
    )
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description="進化ラン → llove Event JSONL 変換ブリッジ")
    ap.add_argument("run_dir", type=Path, help="進化ラン出力ディレクトリ (metrics.jsonl 等)")
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="出力 JSONL パス (既定: <run_dir>/llove_events.jsonl)",
    )
    args = ap.parse_args()

    out = args.out or (args.run_dir / "llove_events.jsonl")
    lines = convert(args.run_dir)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}  ({len(lines)} events)")
    print(f"  llove tail {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
