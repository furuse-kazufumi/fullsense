---
title: '`ctx 2549%` は AI の暴走ではなく人間の計測破綻だった — llterm 障害対応の切り分け記録'
tags:
  - AI
  - LLM
  - ClaudeCode
  - Codex
  - Agent
private: false
public_private: false
group_url_name: general
slide: false
ignorePublish: true
id: 6fe79ab04443f7654eca
---
# `ctx 2549%` は AI の暴走ではなく人間の計測破綻だった — llterm 障害対応の切り分け記録

> **この草稿の位置づけ**
> #46 の `2. ターン境界と緊急割り込みは、最初から別物として設計する` / `3. ctx 2549% は「AI が太った」のではなく、計測が壊れていた` / `6. テストも「たまたま緑」を疑う` を、後で個別公開できるよう Team stock に退避した source draft です。2026-06-18 に Qiita Team `fullsense` へ POST 済みで、item id は `6fe79ab04443f7654eca`、2026-06-19 12:41:22 +09:00 の再確認では Team API GET が `private:false` と `group.url_name: general` / `group.private: false` を返し、未認証 HTML GET は `302 /login?redirect_to=...` でした。poster payload では `group_url_name` を明示していなかったため、現在の local source では観測済み share target として `group_url_name: general` を固定しています。ただし Team サブドメイン全体の auth gate でも説明できるため、team-only と positively 確認できるまでは **過剰露出の疑いを優先**します。`private:false` の意味づけ自体は一次情報待ちで、ここで言う `visibility semantics` はプロジェクト内用語です。local source では accidental な `qiita publish` を避けるため `ignorePublish: true` を残しています。

> **前提**
> `claude -p --resume` や `codex exec` のような headless CLI を turn 境界で回し続ける自走 AI harness の文脈を前提にします。
>
> **流れ**
> `ctx 2549%` を入口に、rotate 因果、`sticky cancel`、`block point` の順で incident を切り分けます。
>
> **ゴール**
> 「異常値を AI の賢さと誤認せず、まず計測破綻として疑う」という監督側の態度を、具体 incident として持ち帰れるようにします。

> **この記事で話さないこと**
> ここでは `llterm` 全体の 9 原則を再説明しません。対象は `ctx 2549%` を入口にした障害切り分けと、そこから見えた監督境界の話に限ります。

最初の異常は、AI が止まったことではありませんでした。  
目に入ったのは `ctx 2549%` という、物理的にありえない占有率表示です。

この数字を見た瞬間、つい「モデルが太った」「context が爆発した」と言いたくなります。  
でも実際に追うべきだったのは AI の賢さではなく、**人間が置いた計測の壊れ方**でした。

## この記事で切り出す軸

1. `ctx 2549%` は何が確認済みで、何が未解決なのか
2. `rotate` を誘発した因果と、表示数値の膨張機序を分けて書く
3. `turn boundary` と `interrupt` を同じレールで扱うと、なぜ `sticky cancel` になるのか
4. `block point` が無いと、なぜ flaky test は「たまたま緑」に見えるのか

## この草稿の狙い

#46 本編は「自走 AI をどう監督するか」という 9 原則の線でまとめています。  
そのぶん、`ctx 2549%` 自体の postmortem はどうしても圧縮されています。

そこでこの別稿では、

- 計測破綻
- rotate 条件
- cancel / interrupt の切り分け
- suspiciously green なテスト

を、監督原則の一般論ではなく **障害対応の切り分け記録** として掘り直します。

## source

- 完全版: `qiita46_llterm_supervision_first.md` 第2章 `ターン境界と緊急割り込みは、最初から別物として設計する` / 第3章 `ctx 2549% は「AI が太った」のではなく、計測が壊れていた` / 第6章 `テストも「たまたま緑」を疑う`
- 切り出しの核:
  - `turn boundary` と `interrupt` を分ける incident
  - `ctx 2549%` の rotate 因果と算定未解決の二段構え
  - `block point` が無いテストは `たまたま緑` に見えるという incident
- 根拠スナップショット: `docs/articles/2026-06-18/llterm_seed6_evidence.md`

## honest disclosure

`ctx 2549%` について、現時点で確認済みなのは「この異常表示が rotate を誘発していた」ことまでです。  
一方で、**その表示値をどう算定した結果 2549% まで膨れたのか** はまだ完全分解していません。公開時も、この二段の確信度は崩さず書きます。
