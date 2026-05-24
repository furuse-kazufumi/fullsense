---
layout: default
title: "Speculative Mesh 本格配線 (SPEC-MESH-02/03/04) + セキュリティ修正"
parent: "Research"
nav_order: 96
---

# Speculative Mesh 本格配線 (SPEC-MESH-02/03/04) + セキュリティ修正 (2026-05-25)

> FullSense 高速化プログラム Tier 1「Speculative Mesh」([`acceleration_poc_matrix_2026_05_24`]({{ '/research/acceleration_poc_matrix_2026_05_24' | relative_url }}))
> の本格導入。PoC の record-only / 手動駆動だった 2 つの seam を、実機構へ配線した。
> 規約: 要件→PoC→フィジビリティ→詳細設計 / fail-closed / honest disclosure。

## 配線した 3 要件 (llmesh `llmesh/speculative/`)

- **SPEC-MESH-02 実 mesh transport**: 派遣先 peer の endpoint を node registry で解決し、
  非ブロッキングの背景送信で署名 manifest を idle peer へ low-priority 投入。送信失敗は
  計上のみで origin の本筋推論を止めない (fail-soft)。
- **SPEC-MESH-03 peer executor**: 受信 manifest を Ed25519 検証 (fail-closed・未検証は実行しない)
  → 低優先で実行 → 結果を**署名して返す** (provenance + 改ざん検知)。
- **SPEC-MESH-04 fast-fallback**: origin は投機完了を待たず、hit が無ければ**即ローカル計算**。
  timeout 待ち・inflight join を一切しない (break-even を 0 付近に保つ唯一の条件・後付け不可)。

in-process ループバック mesh で origin→peer→origin の往復 (hit / miss+fast-fallback) を
実署名・実検証で通す round-trip テスト含め全テスト green。

## セキュリティレビューと修正 (cross-AI → 実コード検証)

独立レビューで判明した本物の脆弱性を実コードで検証し修正:

- **キャッシュ汚染の遮断 (high)**: 結果取込時の peer 束縛を**既定で fail-closed** 化。
  返ってきた結果の署名鍵から peer 識別子を復元し、**実際に派遣した peer** と一致しなければ拒否。
  公開される manifest ハッシュに第三者が署名結果を被せてキャッシュを汚す経路を塞いだ
  (registry 非依存)。open-relay は明示 opt-out のみ。
- **信頼境界の明確化 (high)**: 結果値を認証しない低レベル sink と、署名検証する取込関数を
  ドキュメント上も分離。未信頼な peer 返答は必ず取込関数を通す契約に。
- 送信路の no-raise 契約遵守・ループバックの best-effort 化 (low) も対応。
- 暗号プリミティブ / 正準 JSON 決定性 / fail-closed デコード / メトリクスのスレッド安全性 /
  非ブロッキング fast-fallback は**正しい**と確認。

> honest disclosure (SPEC-MESH-11): 署名は **authenticity + 派遣先 provenance** を保証するが
> **結果の正しさ**は保証しない。投機結果を確定タスクへ昇格する前に cross-check / 予測検証ゲートを
> 通すこと。

## 残作業 (honest)

- **実測 (SPEC-MESH-07)**: simulation 値を実 transport/executor 配線後の実測で上書き (LAN/WAN 分離)。
- **分岐予測器の実データ化 (#2)**: 唯一 LLM 不要の候補生成器は決定論テンプレ表のため、それで作る
  hit_rate は構造的に過大 (= 「変に良い結果」)。意味ある実測には on-prem 実 LLM を生成器へ配線するのが前提。
  それまでは honest ガード (実測データ不足表示) が合成上限を正しく守る。

## 関連

- 要件: llmesh `docs/requirements_speculative_mesh.md`
- 上流: [予測符号化スパイン (発見A)]({{ '/research/ideation_marathon_expression_realtime_2026_05_23' | relative_url }}) /
  [Gemini ブレスト実装着地]({{ '/research/gemini_brainstorm_impl_2026_05_24' | relative_url }})
