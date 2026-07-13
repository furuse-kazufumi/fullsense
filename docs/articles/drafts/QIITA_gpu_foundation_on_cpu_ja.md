# GPU付きPCが届く前に、CPUだけで「研究の土台」を作った話 —— スケールを「書き直し」ではなく「設定＋フラグ変更」にするために

> 対象: 世界モデル・進化計算・ロボティクスのシミュレーションを自宅PCで回している人 / 「そろそろGPUを足したい」が「コードを書き直したくない」人。
> 前提知識: Python が読めれば十分。torch / jax / MuJoCo 用語は都度かみくだきます。
> この記事は publish 前ドラフト（構成は CPU で検証済み、GPU 実測はまだ・公開は人間判断）。

---

## 0. 3行まとめ（先に結論）

- GPU付きPCが今週届く。**待つ代わりに**、CPUだけで回っている世界モデル＋ロボ進化のコードベース（`onocollo`）を、GPU箱に載せる瞬間が「書き直しではなく、セットアップ＋フラグ変更」で済むように整えた。
- まず**推測せず測った**: コード全体は 100% 直列・単一環境の MuJoCo で、律速は ①ロケット評価実験 ②ADR 把持 ③スイマー QD、世界モデル（Dreamer/RSSM）は既に CUDA クリーンだが V→M→C の画素経路に CPU 決め打ちの障害物があった。CPU 上で作れる**移植可能な勝ち**を3つ実装した（stdlib 並列 map / `device="auto"` 配線 / クロスプラットフォームの環境ブートストラップ）。
- ただし正直に言うと、**GPU の高速化も MJX のバッチ物理も、まだ一度も走らせていない**（GPU がまだ無い）。だから最大の勝ち候補（MJX）は「移植」ではなく「**先に走らせる go/no-go スループット計測**」として出荷した。「測る前に制御ループを移植するな」——このルールを守ったこと自体が、この記事の主題だ。

---

## 1. 用語（先に地図）

| 用語 | かみくだき |
|---|---|
| onocollo | 自作の CPU 完結な研究コードベース。世界モデル（画素から学ぶ）＋ ロボの進化・QD シミュを1つに束ねたもの |
| 世界モデル（world model） | 環境を頭の中で再現するモデル。画素→潜在→予測→制御の V→M→C 構成が古典 |
| V→M→C | Vision（画像を圧縮する VAE）→ Memory（時間を予測する RNN）→ Controller（行動を選ぶ）の3段パイプライン |
| VAE（variational autoencoder） | 画像を小さな潜在ベクトルに圧縮・復元するネット。64×64 画素の畳み込みが GPU で一番効く |
| Dreamer / RSSM | 世界モデルの現代版。潜在状態を回して「夢の中で」方策を学ぶ。RSSM=recurrent state space model |
| MuJoCo | 物理シミュレータ。C エンジンで剛体・接触を解く。ロケット・把持・歩行の土台 |
| MJX | MuJoCo を jax で書き直した GPU 版。**同じ形の**モデルを数千個まとめて GPU で並列に踏める（バッチ物理） |
| jax | GPU/TPU 上で自動微分＋ベクトル化する数値計算ライブラリ。`jax.vmap` で「関数を一括適用」 |
| 律速（ボトルネック） | 全体の実行時間を支配している最も重い箇所。ここを速くしないと他をいくら磨いても無駄 |
| embarrassingly parallel | 「恥ずかしいほど並列」。各仕事が互いに独立で、分けて配るだけで速くなる状態 |
| process-parallel | 独立した評価を複数の CPU コア（プロセス）に配って同時に回す。GPU 不要の素直な高速化 |
| ADR（adversarial / automatic domain randomization） | ロボ把持を「わざと荒れた条件」で頑健化する評価。ここでは把持ロールアウトの重いループ |
| QD（quality-diversity） | 「速い解」だけでなく「多様で良い解の地図」を育てる進化。スイマーの形態探索に使う |
| go/no-go gate | 本移植の前に「そもそも速くなるのか」を独立に測る関門。NO-GO なら移植しない、と先に決めておく |

---

## 2. 状況: GPU箱が今週来る。待つか、備えるか

`onocollo` は「CPU-first, then 1 GPU」という約束のもとに作ってきた。自宅の非力なノート CPU（torch は `2.12.0+cpu`）で、**世界モデルとロボの進化を1つのコードベースに束ねた**研究基盤だ。世界モデルは画素から着陸や把持を学ぶ V→M→C / Dreamer 系、ロボ側はロケット着陸・ADR 把持・スイマー形態進化を MuJoCo で回す。

そこに GPU付きPCが今週届くことになった。ここで普通なら「箱が来てから GPU 対応を考える」のだが、それだと**届いた日に「あれ、このコード GPU で動かすには結構書き直しが要るな」と気づいて数日溶かす**——という筋書きが見える。過去に何度もやった。

だから決めた。**箱が来る前に、CPU の上で「GPU 対応」を済ませておく**。ゴールは1つ:

> GPU箱に載せる瞬間を、**書き直し（rewrite）ではなく、セットアップ＋フラグ変更（setup + flag change）**にする。

この記事は、その「備え」を CPU だけでどこまで正直に作れたか、そして**どこは正直に"まだ走らせていない"と認めたか**の記録だ。

---

## 3. まず測る: コンピュートマップ（推測でGPU対応しない）

FullSense 全体で守っている規律に「異常に良い結果は内訳を疑う」「測る前に手を動かすな」がある。GPU 対応も同じで、**"たぶんここが遅い"で移植先を決めない**。最初にやったのは監査——コード全体の**コンピュートマップ（compute map）**、つまり「どのループが、どこで、どれだけ計算を食い、どのアクセラレータが一番効くか」の地図作りだ。

分かったことは身も蓋もなくシンプルだった:

> コードベースは現状 **100% 直列・単一環境の MuJoCo**。`Simulation` が1つの `MjModel`+`MjData` を Python ループで踏むだけ。どのコード経路にも `multiprocessing` も `jax` も `mjx` も無い。

一方で、進化・QD・評価の各ループは**候補×エピソード×seed で互いに独立**——つまり embarrassingly parallel なのに、その並列性を1ミリも使っていない。これが伸びしろ（headroom）だ。地図にするとこうなる:

| ワークロード | どこ | コスト | 最良のアクセラレータ |
|---|---|---|---|
| **ロケット評価実験** | `rocket_eval_experiment.py`, `landing.py` 内側ループ | **#1** — 1600ステップ×数千/seed×10 seed＋PIDグリッド再調整 ≈ 1000万 `mj_step`/seed | **MJX**（単一固定 `RocketSpec` → 均質バッチ、理想的）or 10 seed の process-parallel（最安・移植可能） |
| **ADR 頑健/神経把持** | `adr/capture.py` | #2 — `飛来数×(1+アクチュエータ数)` ロールアウト×集団×seed | **process-parallel**（ほぼ線形）。ループ内 IK/接触が Python なので MJX は部分的に不向き |
| **スイマー/形態 QD** | `evolve/evolution.py`, `qd.py` | #3 — 短い(~430ステップ)ロールアウト、**genome ごとにモデルが違う** | **集団の process-parallel**（MJX は形態ごとのバッチが必要） |
| **世界モデル V→M→C** | `train.py` の VAE/MDN-RNN 訓練 | GPU 有利な畳み込み＋系列訓練 | **torch CUDA**（`device="auto"`） |
| **Dreamer / RSSM** | `dreamer.py`, `rssm.py` | 小さい MLP/GRU、次元を上げて初めて GPU が効く | **torch CUDA**、既に device クリーン |
| コントローラ ES | `train.py` | 直列・単一サンプル | なし — CPU 据え置き（GPU はむしろ損） |

この地図が、以降の**「何を、どの順で」**を全部決めた。推測ではなく、監査に基づいて。

ここで大事な非対称性が2つ見えた:

1. **世界モデル側は既にほぼ GPU 対応だった**。Dreamer/RSSM のスタックは最初から device クリーン。ただし古典 V→M→C の画素経路（VAE の画素訓練・MDN-RNN・VAE エンコードのブリッジ）に **CPU 決め打ちの障害物**が残っていた。
2. **ロボ側は 1 コアも並列化していない**。だが各ループは独立候補の集まりなので、**GPU すら要らずに**多コアで速くできる。

つまり「GPU 対応」と一括りにしていたものは、実は**性質の違う3種類の勝ち**だった。順に作る。

---

## 4. 移植可能な勝ち A: 進化ループを多コアで回す（GPU不要・jax不要）

一番効いて、一番安いのがこれ。進化・QD・評価ループに `--workers` / `parallel_map` の経路を足した。実装は `onocollo.parallel` の 1 関数だけ、**依存は標準ライブラリの `concurrent.futures` のみ**（jax も ray も joblib も要らない）。

設計の肝は「直列と**バイト単位で同一**を保つ」こと。`--workers 1`（既定）は今までと 1 ビットも変わらない。多コア箱では同じ実験がただ速く回る。

```python
def parallel_map(fn, items, *, workers=1, backend="auto"):
    # backend="auto": workers<=1 なら直列、そうでなければ process
    if backend == "auto":
        backend = "serial" if workers <= 1 else "process"
    if backend == "serial":
        return [fn(x) for x in items]
    if backend == "process":
        seq = list(items)
        with ProcessPoolExecutor(max_workers=workers) as pool:
            # 入力順に submit し、index で回収（as_completed ではない）
            # → 出力順 = 入力順が構造的に保証される
            futures = [pool.submit(fn, x) for x in seq]
            return [f.result() for f in futures]
```

`[fn(x) for x in items]` の**プラグ互換な置き換え**になっている点がポイントだ。`fn` が引数の純関数（onocollo の seed 付き評価はそうなっている）なら、並列出力＝直列出力。しかも `as_completed`（完了順）ではなく **index で回収**しているので、ワーカーの完了順に関わらず**返る順序は必ず入力順**——決定性が壊れない。

使い方はこう。ロケット評価の 10 個の独立 seed をコア数ぶん並列にするだけ:

```bash
# ロケット評価 — 10個の独立 seed をコアに分散
PYTHONPATH=src py -3.11 scripts/rocket_eval_experiment.py \
    --condition P --seeds 0-9 --workers 8 --out out/rocket/eval_exp
```

正直な但し書きも埋め込んだ。Windows は `spawn` なので `fn` と各 item は picklable でなければならず（lambda/closure 不可、module-level 関数を使う）、呼び出しスクリプトは `if __name__ == "__main__":` で守る必要がある——さもないと spawn 下で各ワーカーが親モジュールを再 import して**無限にフォーク**する。決定性については、各 seed が自己完結の paired-common-random-numbers run で自分の JSON を書くので並列出力＝直列出力（`--quick` スモークで検証済み）。frozen-PID キャッシュは fan-out 前に一度だけ温めて書き込み競合を避ける。

**これは GPU がまだ無い今でも効く勝ち**だ。手元のノートでもコア数ぶん速くなり、多コアの新箱ではそのまま線形にスケールする。GPU を1枚も使わずに。

---

## 5. 移植可能な勝ち B: 世界モデル訓練を CUDA へ（フラグ1つ）

世界モデル側の障害物を潰す。`WMConfig.device` を `"auto" | "cpu" | "cuda"` の3値にし、`"auto"` は GPU があれば `cuda`、無ければ `cpu` に解決する。中身は `utils.resolve_device` のこれだけ:

```python
def resolve_device(device: str) -> str:
    """config の device 文字列を具体的な torch device へ解決する。"""
    if device == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    return device  # "cpu"/"cuda"/"cuda:0" 等はそのまま通す
```

Dreamer/RSSM は元々 device クリーンだったので、仕事は**古典 V→M→C 経路に device を通す配線**だった。VAE の画素訓練・MDN-RNN・VAE エンコードのブリッジに `device` を貫通させ、**パイプライン全体がフラグ1つで GPU に載る**ようにした。しかも CPU 上ではバイト単位で同一を維持——つまり「GPU 対応にしたら CPU の結果が変わった」が起きない。

呼び出し側はこうなる:

```python
import dataclasses
import onocollo as oc
from onocollo import default_config

# 世界モデル V/M/C を GPU で（tiny プリセットから拡大して）:
cfg = dataclasses.replace(default_config(), device="auto")
oc.run_pipeline(cfg)
```

### GPU が本当に効く場所（正直に）

ここは誇張しないのが大事なところ。**GPU がはっきり効くのは ConvVAE（64×64×3、strided 畳み込み4層）の画素訓練だけ**だ。RSSM/Dreamer は既定の tiny 次元（deter ≤ 64）では計算が軽く、**GPU の起動オーバーヘッドがむしろ支配的**になり得る——`z_dim` / `deter` / `batch` / `train_iters` を上げて初めて GPU が勝つ。

だから GPU 箱の意義は「micro プリセットを速くする」ことではなく、**CPU では回せない non-tiny な設定を回す**ことにある。プリセットを拡大（大きい `z_dim`、多い `train_steps`、長い系列）するのが正しい使い方で、tiny のまま速くなるのを期待するのは筋違いだ。この非対称性を doc に書いておかないと、GPU 箱で「あれ、速くならない」と誤解する。

---

## 6. Linux 限定の勝ち C: MJX バッチロケット —— ただし「先に測る」

さて、コンピュートマップの #1 律速はロケット評価だった。そしてこれは MJX の**唯一のきれいな適合**でもある。単一固定形状の `RocketSpec` モデルなので、数千のロールアウトが**均質なバッチ**を成し、`jax.vmap` + MJX が GPU 上でベクトル化できる。理屈の上では最大の勝ちだ。

ここで**正直さの分岐点**が来る。

MJX は jax の GPU 物理で、**公式 CUDA wheel は Linux 限定**（Windows は WSL2 が要る）。そして——**手元の CPU ワークステーションには入っておらず、一度も検証していない**。理屈では最大の勝ちだが、実測はゼロだ。

| Tier | Windows | Linux |
|---|---|---|
| **torch CUDA**（世界モデル訓練） | ✅ ネイティブ | ✅ ネイティブ |
| **多コア process 並列**（進化ループ） | ✅ ネイティブ | ✅ ネイティブ |
| **MJX**（jax GPU 物理バッチ） | ❌ WSL2 必須 | ✅ ネイティブ |

ここで一番やってはいけないのは、**未検証の GPU コードを「動く」と偽って移植を書き上げること**だ。MJX ロールアウトを丸ごと書いて「GPU で数千倍！」と記事に書くのは簡単だが、それは嘘になる。

だから移植する代わりに、**go/no-go スループット計測（throughput probe）を先に走らせる関門**を出荷した。ルールは1行:

> **測る前に制御ループを移植するな**（Don't port the control loop before the gate passes）。

関門はこう回す。まず必要条件だけを測る:

```bash
# go/no-go スループット関門（open-loop の生の物理だけを計測）
PYTHONPATH=src py -3.11 scripts/mjx_spike.py --batch 2048 --steps 200
```

これは**コントローラ抜きの open-loop バッチ踏み**（物理だけを切り出すため意図的に制御を外す）を、同じ `batch*steps` 仕事量に外挿した直列 C エンジンと比べ、5× 閾値で `GO` / `MARGINAL` / `NO-GO` を印字する。

- **`NO-GO`** → 止める。この モデル+GPU で GPU ベクトル化した踏みが本質的に速くないなら、制御ループを移植しても救えない。process-parallel の `--workers` 経路に留まる。
- **`MARGINAL`** → `--batch` を増やして（4096, 8192）再試行。固定の jit/起動オーバーヘッドは規模で償却される。再判定。
- **`GO`** → 初めて本移植へ進む。

そして `GO` が出ても、移植後に**数値検証**が待っている。MJX は C エンジンとビット単位一致しない（接触ソルバの内部が違う）ので、CPU の数 seed でロケットの着陸統計が `landing.py` と許容誤差内で一致することを確認するまで、**事前登録した実験のスコア用ロールアウトを勝手に別の物理エンジンに差し替えてはいけない**。ロケットは脚で着地する——接触リッチな力学こそ MJX ソルバが C エンジンから最も逸れやすい場所だ。

CPU 上で「今出荷したもの」は正直にこれだけ:

- `onocollo/mujoco/mjx_batch.py` — `has_mjx()`, `require_mjx()`（明快なインストールエラー）, `mjx_throughput_probe(...)`（標準 mjx API、CPU 上では未実行）。
- `scripts/mjx_spike.py` — 走る関門。MJX 非対応の箱では「not available」と印字して非ゼロ終了する（**結果を捏造しない**）。
- `tests/test_mjx_batch.py` — CPU 上でガード経路を検証（ここでは `has_mjx()` は False、`require_mjx()` は実行可能なエラーを投げ、probe は走行を拒否する）。

**未検証のものを「動く」と言わない。関門を出荷して、移植は関門の後にする**——これが誠実さの実装だ。

---

## 7. セットアップと検証を「1コマンド」にする

3つの勝ちを、箱が来た日に**1コマンドで**立ち上げられるようにブートストラップした。設計は「dry-run 既定」——コミットして読めるまで、何も機械に触らせない。

```bash
# まず dry-run（この機械向けの正確な pip 計画を印字、インストールはしない）:
py -3.11 scripts/setup_gpu_env.py
# 実行:
py -3.11 scripts/setup_gpu_env.py --run
# 実際に立ち上がったものを検証（torch CUDA / MuJoCo レンダ / jax・MJX）:
py -3.11 scripts/verify_gpu_env.py
```

`setup_gpu_env.py` は `nvidia-smi` で NVIDIA GPU を検出し、`+cpu` の代わりに **CUDA torch wheel** を入れる。`onocollo[dev,mujoco]`・`cma`・メディアエンコーダを足し、**Linux でのみ** `jax[cuda12]` + `mujoco-mjx` を入れる。`MUJOCO_GL` は `onocollo.viz.backend` が自動選択（Windows/macOS は glfw、ヘッドレス Linux GPU 箱は egl）。Windows で MJX を要求されたら、捏造せず**WSL2 の注意書きを印字してスキップ**する。

`verify_gpu_env.py` は非破壊のプローブで、コア経路（numpy + torch + onocollo import）が通れば exit 0、GPU/MJX 行は**報告するが判定を落とさない**（任意 tier だから）。torch の CUDA 可否、実際の MuJoCo オフスクリーンレンダ、jax デバイスを表で出す。

新箱での初日チェックリストはこれだけ:

1. `setup_gpu_env.py --run` → `verify_gpu_env.py`（`torch CUDA: ok`、Linux なら `jax devices: ok` を期待）。
2. sanity: `pytest -q`（5 件の既知 hygiene fail 以外は緑。後述）。
3. 無料の多コア勝ち: ロケット評価を `--workers <cores>` で再走、直列 seed と一致を確認。
4. torch CUDA 勝ち: `run_pipeline(replace(default_config(), device="auto"))` が GPU に載るのを見て、設定を拡大。
5. Linux のみ: MJX go/no-go 関門。通れば ロールアウトをバッチ化、駄目なら process-parallel に留まり**理由を記録**。

### 正直な余談: 5件の落ちるテストは「矛盾したテスト」であって実装バグではない

現状 pytest は **620 pass / 5 fail**。この 5 件（`test_import_hygiene.py`）は正直に言うと**テストスイート同士が矛盾している**ケースだ。facade 設計で `onocollo.train` を callable として公開しつつ実サブモジュールも到達可能にしている——あるコミットが「明示 import でモジュールが勝つ」を要求する 5 テストを書いた一方、古いテストは同じトリガで「facade が勝つ」を要求している。両者は相互排他で、**どんな `__init__.py` 実装でも両立不能**（`__setattr__` から train 分岐を外すと、どの 3 件が落ちるかが入れ替わるだけでゼロにならない、と経験的に確認済み）。研究コア（`rocket/`, `adr/`, `evolve/`, `vae/mdnrnn/rssm/dreamer`）は ruff+mypy クリーン。GPU 作業のブロッカーではないので、契約をどちらに寄せるかは製品判断として保留した。**落ちているものを"通っている"ことにしない**——これも同じ規律だ。

---

## 8. 教訓（gift-to-reader）

- **スケールは「書き直し」ではなく「設定＋フラグ変更」であるべき。** そう設計しておけば、GPU 箱が届いた日を「移植で溶かす日」ではなく「実験を回す日」にできる。`device="auto"` の 3 行、`parallel_map` の 1 関数、dry-run 既定の bootstrap——大げさな仕掛けは要らない。要るのは「載せ替え点を1点に絞る」意志だ。
- **移植する前に律速を測れ。** "たぶんここが遅い"で移植先を選ばない。コンピュートマップを取ると、勝ちは1種類ではなく性質の違う3種類（多コア / torch CUDA / MJX）で、しかも一番効くのが一番リスキー（Linux 限定・未検証）だと分かる。地図が順序を決める。
- **未検証の GPU コードを「動く」と偽らない。** 最大の勝ち候補（MJX）ほど、書き上げて「速い」と言いたくなる。だが手元で検証できないなら、出荷するのは**移植ではなく go/no-go 関門**だ。「NO-GO なら移植しない」を先に決めておくことが、数日を溶かさない保険になる。
- **CPU 上で GPU 対応の 8 割は終わる。** device 配線・並列化・環境ブートストラップ・数値一致の検証——GPU が無くてもできる誠実な準備は多い。GPU を待つ時間は、待つのではなく備える時間にできる。

---

## 9. 次回に続く

備えは終わった。次は**箱が来て、初日手順を実際に回す**回だ:

- 進化ループ全部を `--workers` で多コア化し、直列とバイト一致を確認 → **実測の高速化倍率**（これは今はまだ無い。GPU 箱の実データで正直に出す）。
- 世界モデルを `device="auto"` で GPU に載せ、tiny プリセットを CPU では回せなかった non-tiny へ拡大 → ConvVAE 画素訓練がどこから GPU 有利に転じるか。
- Linux なら MJX go/no-go を走らせる。**`GO` か `NO-GO` か——それ自体がまだ分からない**。5× 閾値を超えるのか、接触リッチなロケットで C エンジンと数値一致するのか。通れば数千ロールアウトのバッチ物理、駄目なら潔く process-parallel に留まって理由を記録する。

正直に繰り返すと、**この記事の GPU 高速化も MJX バッチも、まだ一度も走っていない**。今あるのは「CPU で検証した土台」と「関門」だけだ。だからこそ次回は、**予想が当たったか外れたか**を——ロケットの引き分けを正直に出したときと同じ流儀で——内訳つきで報告する。

（コードは `onocollo`＝世界モデル core + MuJoCo ロボ進化 env + 移植可能な `parallel_map` + `device="auto"` 配線 + go/no-go 関門 + セットアップ/検証スクリプト + 正直な doc、の再利用テンプレ。GPU 箱の実験は同じ形で載る。）

---

> 補足: 計画の正本は `docs/GPU_PLAYBOOK.md`（day-1 手順とコンピュートマップ）、MJX 関門は `docs/MJX_SCAFFOLD.md`、健康診断は `docs/DEV_BASELINE.md`。実装は `scripts/setup_gpu_env.py` / `verify_gpu_env.py`、`src/onocollo/parallel.py`、`utils.resolve_device`。この記事はドラフト（公開は人間判断）。
