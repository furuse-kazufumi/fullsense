---
layout: default
title: "llcraft — Creative Material SOTA"
parent: "Research"
nav_order: 4
---

# llcraft — On-prem Creative Material Generation OSS SOTA (2026-05-20)

> AI agent (Claude Opus 4.7) が WebSearch + 既知 OSS 知識から 800 字以内で
> 生成した調査メモ. `spinoff_ideas_2026_05.md` の llcraft 候補を具体化する
> 前提資料.

## Stack matrix (2026 SOTA, on-prem)

| 領域 | Tier 1 (商用 OK) | Tier 2 (条件付) | Tier 3 (商用 NG) | 日本語 |
|---|---|---|---|---|
| **TTS** | Bark (MIT), StyleTTS2 (MIT, JVS 学習済), VoxCPM2 (Apache-2.0, 48kHz, 30 言語), Irodori-TTS (MIT, 日本語特化) | VOICEVOX (キャラ毎にライセンス分岐, 要クレジット) | XTTS-v2 (CPML, 商用要許諾), AIHUB StyleTTS2 派生 (CC-BY-NC) | VOICEVOX > Irodori > VoxCPM2 > XTTS |
| **画像** | Flux.1-schnell (Apache-2.0), SDXL (OpenRAIL++-M) | Flux.1-dev (Non-Commercial), SD3 (Stability Community, 売上<$1M) | Flux.1-pro (API only) | — |
| **動画** | Open-Sora 2.0 (Apache-2.0), AnimateDiff core (Apache-2.0, ただし WebUI 拡張は NC), Mochi-1, HunyuanVideo, Wan 2.1 | SVD (Stability Community, $1M 閾値) | — | — |
| **音楽** | Stable Audio Open 1.5 (Stability Community, <$1M), YuE 7B, ACE-Step 3.5B | — | MusicGen (CC-BY-NC, self-host でも商用 NG) | — |

## License-aware gap

**統合 OSS の空白**: ComfyUI / InvokeAI は画像中心, Vilva / Yolly / Magnific は
**cloud 依存** (ElevenLabs / Kling 等を内部呼出). **on-prem で TTS+画像+動画+音楽を
license tier 強制付きで束ねる OSS は不在**. SIGGRAPH'26 の Audio-Omni / AudioX
は音響 3 種統合のみで画像・動画は対象外.

**License runtime 強制**: 既存 OSS は **license metadata を出力に埋め込む機構を
持たない**. C2PA Content Credentials (royalty-free, Rust SDK + JS SDK あり) が
provenance manifest の唯一の業界標準で, IPTC 2025.1 が `AISystemUsed` /
`AIPromptInformation` 等 4 XMP フィールドを定義済. **ここに llcraft の
`license_tier` カスタム assertion を載せれば仕様準拠で差別化できる**.

**MCP 統合**: VOICEVOX MCP server (Yuki Kobayashi), VOICEPEAK MCP は単機能のみ.
**マルチモダリティ統合 MCP server は未踏**.

## Recommended composition

1. **コア**: Coqui XTTS は商用障壁 → **VoxCPM2 (Apache-2.0) + Irodori-TTS +
   VOICEVOX (キャラ毎契約管理)** に置換. SDXL or **Flux.1-schnell** (Apache-2.0),
   **Open-Sora 2.0** (Apache-2.0), **Stable Audio Open 1.5** (収益閾値で gate).
   MusicGen は商用 NG ゲートに固定.
2. **License Gate 層**: 各モデル呼出を `LicenseTier` enum で wrap し,
   tenant 収益 / 用途と突き合わせる Policy Engine (llmesh 既存 Approval Bus を
   流用). 違反時 fail-closed.
3. **Provenance**: 出力に **C2PA Manifest + IPTC 2025.1 + 独自
   `llcraft:license_tier` assertion** を埋込. `c2pa-rs` を Rust extra で同梱.
4. **MCP**: `llcraft.generate.{tts,image,video,music}` ツール群を MCP server 化,
   llmesh から llgrow が呼ぶ.
5. **差別化軸**: (a) on-prem 統合, (b) license runtime 強制 + C2PA,
   (c) 日本語第一 (VOICEVOX+Irodori), (d) MCP 経由 vertical 連携 — **4 軸全てを
   満たす OSS は現存せず**, 空白を全部抑えられる.

## Sources

- Stability AI License (Community License, $1M threshold): <https://stability.ai/license>
- Stable Audio Open LICENSE.md: <https://huggingface.co/stabilityai/stable-audio-open-1.0/blob/main/LICENSE.md>
- SDXL LICENSE (OpenRAIL++-M): <https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/LICENSE.md>
- Open-Sora (Apache-2.0): <https://github.com/hpcaitech/Open-Sora>
- StyleTTS2 LICENSE (MIT): <https://github.com/yl4579/StyleTTS2/blob/main/LICENSE>
- Coqui XTTS-v2 (CPML, non-commercial default): <https://huggingface.co/coqui/XTTS-v2>
- VOICEVOX 商用利用ガイド: <https://ondoku3.com/en/post/voicevox/>
- VoxCPM2 / Irodori-TTS 2026 まとめ: <https://lilting.ch/en/articles/voxcpm2-tokenizer-free-local-tts>
- C2PA Content Credentials Spec 2.4: <https://spec.c2pa.org/specifications/specifications/2.4/explainer/Explainer.html>
- IPTC 2025.1 + C2PA AI metadata fields: <https://www.numonic.ai/blog/iptc-2025-c2pa-ai-provenance-metadata>
- Open-source music model deployment guide 2026: <https://www.spheron.network/blog/deploy-open-source-ai-music-generation-gpu-cloud-2026/>
- ComfyUI alternative landscape 2026: <https://martini.art/en/vs/comfyui-alternative>
