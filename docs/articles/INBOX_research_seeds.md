# 研究→記事 INBOX (research feedback) — 自動集約・再生成可

> `tools/collect_research_seeds.py` が各 FullSense 系 project の `docs/ARTICLE_SEEDS.md` を集約。
> ☐=未記事化 / ☑=記事化済(元エントリに「→ 記事化: #NN」を書くと ☑ になる)。
> 計 36 件 / 未記事化 **35** 件。


## ?

- ☐ **[llterm]** 背景 (かみくだき)
- ☐ **[llterm]** 何が起きたか (事実・production ログ由来)
- ☐ **[llterm]** 直し方 (技術設計)
- ☐ **[llterm]** honest disclosure (記事の核)
- ☐ **[llterm]** コード参照
- ☐ **[llterm]** 事実
- ☐ **[llterm]** 直し方
- ☐ **[llterm]** angle 候補
- ☐ **[llterm]** 設計
- ☐ **[llterm]** 落とし穴 (教訓・honest)
- ☐ **[llterm]** コード参照
- ☐ **[llterm]** 事実 / 設計
- ☐ **[llterm]** angle
- ☐ **[llterm]** コード参照
- ☐ **[llterm]** 事実
- ☐ **[llterm]** 教訓 (記事 angle)
- ☐ **[llterm]** 抽出した原則 (転用可能・各々が小見出しになる)
- ☐ **[llterm]** angle / 連載の割り方 (13 側面に対応)

## 2026-06-13

- ☐ **[llcore]** 17. API が全部死んでも corpus は「構造化 fallback」で前に進める
  - 側面: 実装報告 / 教訓 / AI 駆動研究ワークフロー。
  - 気付き: `corpus2skill` の要約器は ANTHROPIC org disabled で全滅、さらに今回は
- ☐ **[llcore]** 18. 広い topical query は recall を稼ぐが、leaf cluster にノイズとして返ってくる
  - 側面: 教訓 / 実装報告 / honest disclosure。
  - 気付き: `self-evolving` / `reflection` / `test-time training` 系で 16 クエリを広く張ると、

## 2026-06-12

- ☐ **[llcore]** 1. 「ANN 化 = 速い」は規模の前提を隠している
  - 側面: ベンチ / honest disclosure / 教訓。「最適化はボトルネックの所在を測ってから」
  - 気付き: faiss HNSW を 23k annotations に入れても速くならない (exact 19.6ms →
- ☐ **[llcore]** 2. 過去の null 結果が将来の設計判断を救う (honest disclosure の実利)
  - 側面: honest disclosure / 哲学 / 教訓 / TRIZ (リソースを使わない解決)。
  - 気付き: 全量取込で doc 内全ペア共起エッジは ~2,000 万エッジ (dict 数 GB +
- ☐ **[llcore]** 3. トップレベル ls の罠 — 規模見積もりが 2.5 倍ずれる
  - 側面: 教訓 / 実装報告。「数える方法そのものを検証する」— 計測の計測。
  - 気付き: RAD corpus の規模をトップレベル `ls | wc -l` で見積もると 17.8k docs、
- ☐ **[llcore]** 4. RAD 接地 30 分で研究の新規性マップが引ける (AI 駆動研究ワークフロー)
  - 側面: 戦略 / エコシステム / AI 駆動研究の方法論 / 実装報告。
  - 気付き: M2 (cert gate × 会話連結性教師) の設計前に、RAD 49 分野を Explore
- ☐ **[llcore]** 5. 研究の circularity 回避 — 教師信号は「自分の実装」でなく「外部事実」に接地する
  - 側面: 哲学 / 認知科学 / 教訓。
  - 気付き: M2 で連結性グラフ (自前実装) を教師にすると「グラフ実装が正しい」前提の
- ☐ **[llcore]** 6. dedup が corpus 取込の実質規模を 2 割減らす
  - 側面: 実装報告 / ベンチ。
  - 気付き: AnnotationStore の store 全体 dedup で、aerospace 71k instances →
- ☐ **[llcore]** 7. 15.7 GB 物理メモリで 100 万行 store を扱う見積もり術
  - 側面: 実装報告 / 教訓 / ユーザー体験 (家庭用 PC スペックでの研究)。
  - 気付き: RSS 実測 2 点 (53.7k 行 = 764 MB, 89.7k 行 = 910 MB) から増分
- ☐ **[llcore]** 16. 採用する「頂点」自体が発散境界上にいる (best_rho 1.000)
  - 側面: 哲学 / honest disclosure / ベンチ / 認知科学 (探索と安全の幾何学)。
  - 気付き: M2.1 seed 0 無 gate で、fitness 最良 gene (= 実運用なら採用する個体)
- ☐ **[llcore]** 15. fail-closed gate は「最初の admit」を設計しないと空転する
  - 側面: 技術設計 / 教訓 / TRIZ (事前対策原理)。
  - 気付き: cert_inf (µs 判定) に切替えても MAP-Elites が空転した。実測で
- ☐ **[llcore]** 13. sound gate のコストは「判定 1 回の速さ」でなく「reject 率 × resample 構造」で決まる
  - 側面: 技術設計 / 実装報告 / 教訓。
  - 気付き: cert_sdp (1 判定 ~数百 ms) を MAP-Elites の gate にしたら smoke が
- ☐ **[llcore]** 14. 「学習できる × 安全を選ばない」の同時観測 (M2 v2 seed 0)
  - 側面: honest disclosure / ベンチ / 哲学。
  - 気付き: readout v2 で T1 (turn 境界予測) は train CE 0.5186 < floor 0.6269、
- ☐ **[llcore]** 12. run_in_background はセッションと運命を共にする — 長時間ジョブは detached へ
  - 側面: 教訓 / 実装報告 / ユーザー体験 (AI 駆動開発の実務的罠)。
  - 気付き: エージェント環境の「バックグラウンド実行」はセッション終了 = プロセス死。
- ☑ **[llcore]** 11. 「floor を仮説族に包含させる」— 識別力設計の一般原理
  - 側面: 技術設計 / 教訓 / 認知科学 (測定の妥当性)。
  - 気付き: M2.0 readout v1 (X 空間 centroid + 分離スケール β) は「定数予測 (クラス
- ☐ **[llcore]** 10. 無 gate archive 69/69 全部 ρ≥1 — 会話教師の危険性の初観測 (要 v2 確定)
  - 側面: honest disclosure / ベンチ / 哲学 (capability と safety の直交性)。
  - 気付き: M2.0 smoke v1 seed 0 で、無 gate MAP-Elites archive の **69 gene 全部が
- ☐ **[llcore]** 9. checkpoint は「量」と「時間」の二軸で切る (実損から)
  - 側面: 教訓 / 実装報告。
  - 気付き: 全量取込の checkpoint を「200k 行ごと」のみにした結果、セッション死亡で
- ☐ **[llcore]** 8. 「会話 35 turns = 122 annotations」の小ささ自体が設計を駆動する
  - 側面: honest disclosure / 哲学 / 技術設計。
  - 気付き: M2 の会話教師はわずか 122 annotations (境界率 0.281)。この小ささゆえ
