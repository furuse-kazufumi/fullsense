# QIITA #24 series — Cross-link URL mapping (投稿後に埋める)

> ⚠ 連載 #24 シリーズ 9 本 (#24-00 〜 #24-08) は draft 段階. 投稿後に各記事の
> Qiita URL (`https://qiita.com/furuse-kazufumi/items/<hash>`) が確定するため,
> 全 draft 内の cross-link を本表に従って実 URL に **一括置換** する.
>
> 本 mapping は **投稿時に更新**.  draft 内の cross-link は以下の **仮表記**:
>
> - 本文中の参照: `#24-XX` (例: 「詳細は #24-05 で」)
> - memory 風参照: `[[QIITA_24_XX_*]]`
> - repo internal: `docs/perf_comparison/<日付>_*.md` (GitHub URL に展開)

## URL mapping table

| ID | 仮表記 | Title | Qiita URL (投稿後に埋める) | 投稿日 |
|---|---|---|---|---|
| 24-00 | `#24-00` / index | llive 完全解説 series — index | _未投稿_ | — |
| 24-01 | `#24-01` | 4 層メモリ | _未投稿_ | — |
| 24-02 | `#24-02` | 10 軸で考える AI: 思考因子 × COG-MESH × 三重縞 | _未投稿_ | — |
| 24-03 | `#24-03` | 矛盾は計算できる: 構造進化 × TRIZ × Z3 | _未投稿_ | — |
| 24-04 | `#24-04` | 収束する脳 B-series: SynapticSelector / UCB1 / Hebbian | _未投稿_ | — |
| 24-05 | `#24-05` | 集団が学ぶ AI: v0.B/C/D/E 派生集団進化総括 (連載中核) | _未投稿_ | — |
| 24-06 | `#24-06` | Transformer の外: Mamba / Jamba / RWKV / Diffusion | _未投稿_ | — |
| 24-07 | `#24-07` | 審査つき AI: runtime_metadata × Approval Bus × Ed25519 audit chain | _未投稿_ | — |
| 24-08 | `#24-08` | 眼鏡を作る: lleval — honest disclosure 5+1 因子分解 | _未投稿_ | — |

## 投稿後の置換手順

1. 1 本投稿 → Qiita 個別記事 URL を取得
2. 本表の「Qiita URL」列に追記
3. **全 draft (#24-00 〜 #24-08) を grep** で当該 ID への参照を検索:
   - `grep -rn "#24-${ID}\|QIITA_24_${ID}" docs/articles/2026-05-21/`
4. 仮表記を Qiita URL に **一括置換** (sed or Edit tool):
   - `#24-XX` → `[#24-XX](https://qiita.com/.../items/<hash>)`
   - `[[QIITA_24_XX_*]]` → 同上
5. 投稿済記事も追々更新 (Qiita 側で記事編集 → 再公開)

## Repo internal link の扱い

`docs/perf_comparison/<日付>_*.md` や `crates/llive_rust_ext/src/lib.rs` のような
**repo 内 path** は Qiita 投稿時に GitHub URL に展開:

```
docs/perf_comparison/2026-05-22_kernel_implementation_comparison.md
↓
https://github.com/furuse-kazufumi/llive/blob/optimize/core-2026-05-20/docs/perf_comparison/2026-05-22_kernel_implementation_comparison.md
```

main にマージ済なら branch 部分を `main` に. PR 進行中は当該 branch.

## memory cross-link の扱い

`[[feedback_rust_usage_matters]]` のような memory 参照は Qiita 公開記事には
**そのまま出さない** (memory は private). 代わりに:

- 関連知見を本文に展開 (memory の Why / How を要約してインライン化)
- もしくは GitHub repo 内 docs に同等内容を作って link

## 関連 memory

- [[feedback_no_local_path_in_public]] — 公開資料に D ドライブやローカルパスを書かない
- [[feedback_qiita_github_links.md]] — Qiita 記事に GitHub link を積極配置
- [[feedback_no_image_placeholders]] — image placeholder 不可

---

> 投稿開始時に本表を **唯一の source of truth** として運用. draft 直書き
> はしないこと.
