---
title: 'Semantic Governance は「AI の権限管理」ではなく「AI の意味管理」'
tags:
  - AI
  - LLM
  - Security
  - Agent
  - ClaudeCode
private: true
slide: false
ignorePublish: true
---
# Semantic Governance は「AI の権限管理」ではなく「AI の意味管理」

> **この草稿の位置づけ**
> #43 の `loop engineering にもセキュリティの顔がある` から切り出した Team stock 用の source-only draft です。限定共有・公開とも未実施で、まずは論点を stock することを優先しています。

> **前提**
> headless AI agent / harness / loop を自分で回し、安全層も自作する側の文脈を前提にします。
>
> **流れ**
> `権限管理` と `意味管理` の差を先に切り出し、その後で `llterm` の fail-closed 安全層や `RAPTOR` の evidence ladder へ橋を架けます。
>
> **ゴール**
> `Semantic Governance` を単なる流行語としてではなく、「何を監視し、どこを fail-closed にすべきか」という設計判断へ落として持ち帰れるようにします。

> **この記事で話さないこと**
> ここでは ACL 実装の網羅や、個別ベンダー製品の比較表までは扱いません。論点はあくまで「意味管理」を loop/harness 設計へどう接続するかに絞ります。

AI agent の安全性を語るとき、つい ACL や権限管理の話に寄りがちです。もちろんそれは必要です。ですが、loop が速く回る世界では、それだけでは足りません。  
本当に怖いのは、**許可された権限の中で、意味的に危ない挙動を量産すること**です。

この記事で切り出したいのは、その差です。

- 「正規表現で止める」「このコマンドは禁止」といった静的ガード
- 実行文脈の意味を読んで「今のループが何をしようとしているか」を判定する動的ガード

この後者を、#43 では Filip Verloy の問題提起に沿って `Semantic Governance` と呼びました。  
ここではその語を流行語としてではなく、**自作 loop/harness にどう落ちるか**という目線で整理します。

## この記事で扱う論点

1. なぜ ACL や denylist だけでは loop 時代の安全性を担保できないのか
2. `scaling risk at machine speed` は何を意味するのか
3. `llterm` の fail-closed 安全層は Semantic Governance のどこまでを担い、どこから先は未実装なのか
4. 「AI に権限を渡す」のではなく「AI の行為の意味を監督する」とはどういうことか

## source

- 完全版: `qiita43_harness_loop_stack.md` 第2章前半 `security face`
- 橋渡し先:
  - `MAPE-K` と fail-closed 安全層
  - `/goal` と人間の介入点
  - `RAPTOR` 側の evidence ladder

## honest disclosure

この草稿はまだ Team stock の段階で、具体ログや実装コード片までは展開していません。  
公開版へ育てるときは、引用元 URL、`Semantic Governance` をどこまで Verloy の問題提起として扱い、どこから自分の設計解釈として書くかを、本文中で明示的に切り分けます。
