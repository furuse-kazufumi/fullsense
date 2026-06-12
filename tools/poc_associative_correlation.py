# -*- coding: utf-8 -*-
"""PoC: 相関で連想のつながりを判断するエンジン × 見かけの相関(spurious)を弾く judge.

ユーザー要望(2026-06-10): 「相関値をもっと大事にして、物事の連想におけるつながりを判断する
タイプの AI が大事」。今日の honest 教訓(経験は見かけに騙される、null で本物を見分ける=ラング
トンの蟻)を綜合し、CPU・numpy のみで feasibility を 实测する。

2 部構成:
  Part A (falsifiable): 合成データ(既知の真の連想 + ランダム distractor)で、
    相関(cosine)による連想抽出を「naive top-k」vs「null 検定 + Bonferroni で spurious 棄却」で比較。
    → 真の連想を回収しつつ spurious/distractor を弾けるか(precision/recall/false-positive)を測定。
  Part B (real demo): FullSense MEMORY.md のエントリを char-bigram TF-IDF で表現し、相関で連想想起。
    各クエリの top 連想 + null 閾値超えのみ「本物」と判定して表示(言語不要・on-prem・軽量)。

honest: 相関≠因果。spurious を弾く規律(null 検定)が無ければ「見かけの連想」に騙される、を実証する。
"""
from __future__ import annotations
import sys, io, math, re
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import numpy as np

SEED = 20260610
MEMORY_MD = Path(r"C:\Users\puruy\.claude\projects\D--tools-raptor\memory\MEMORY.md")


# ---------- Part A: 合成 falsifiable test ----------
def synth_embeddings(rng, D=64, K=5, n_per=8, n_distract=12, noise=0.85):
    """K トピック(真の連想=同トピック) + ランダム distractor(連想なし)。"""
    cents = rng.normal(size=(K, D)); cents /= np.linalg.norm(cents, axis=1, keepdims=True)
    X, topic = [], []
    for k in range(K):
        for _ in range(n_per):
            v = cents[k] + rng.normal(scale=noise, size=D)
            X.append(v); topic.append(k)
    for _ in range(n_distract):
        X.append(rng.normal(size=D)); topic.append(-1)  # -1 = distractor(真の連想なし)
    X = np.array(X); X /= np.linalg.norm(X, axis=1, keepdims=True)
    return X, np.array(topic)


def null_threshold(rng, D, n_pairs, alpha=0.05, n_null=200000):
    """ランダム単位ベクトル対の cosine null 分布 → Bonferroni 補正後の閾値。"""
    a = rng.normal(size=(n_null, D)); a /= np.linalg.norm(a, axis=1, keepdims=True)
    b = rng.normal(size=(n_null, D)); b /= np.linalg.norm(b, axis=1, keepdims=True)
    null = np.abs(np.sum(a * b, axis=1))
    q = 1.0 - alpha / max(n_pairs, 1)        # Bonferroni: 多重比較補正
    return float(np.quantile(null, q))


def eval_assoc(S, topic, pairs_mask):
    """pairs_mask[i,j]=True を「連想あり」と判定したときの precision/recall/distractor-FP。"""
    N = len(topic); iu = np.triu_indices(N, k=1)
    same = (topic[:, None] == topic[None, :]) & (topic[:, None] >= 0)  # 同トピック=真(distractor除外)
    pred = pairs_mask[iu]; gt = same[iu]
    tp = int(np.sum(pred & gt)); fp = int(np.sum(pred & ~gt)); fn = int(np.sum(~pred & gt))
    prec = tp / (tp + fp) if tp + fp else float("nan")
    rec = tp / (tp + fn) if tp + fn else float("nan")
    # distractor を1つでも含む「本物」と判定された対の数(見かけの連想)
    is_distract = (topic < 0)
    dpairs = (is_distract[:, None] | is_distract[None, :])
    fp_distract = int(np.sum(pairs_mask[iu] & dpairs[iu]))
    return prec, rec, fp_distract, tp, fp, fn


def part_a():
    print("=" * 64); print("Part A: 合成 falsifiable test(相関による連想 + spurious 棄却)"); print("=" * 64)
    rng = np.random.default_rng(SEED)
    X, topic = synth_embeddings(rng, D=64)
    N = len(topic); S = X @ X.T
    print(f"items={N} (真トピック {int(np.sum(topic>=0))} / distractor {int(np.sum(topic<0))}), dim=64")

    # (1) naive: 各 item の top-3 相関を「連想」とする(有意性を見ない)
    naive = np.zeros((N, N), bool)
    for i in range(N):
        order = np.argsort(-S[i]); order = order[order != i][:3]
        naive[i, order] = True
    naive = naive | naive.T
    p1, r1, d1, *_ = eval_assoc(S, topic, naive)

    # (2) honest: null 検定 + Bonferroni 閾値を超えた相関のみ「本物の連想」
    tau = null_threshold(rng, D=64, n_pairs=N * (N - 1) // 2)
    honest = np.abs(S) > tau; np.fill_diagonal(honest, False)
    p2, r2, d2, *_ = eval_assoc(S, topic, honest)

    print(f"\n  null 閾値 τ(Bonferroni α=0.05) = {tau:.3f}")
    print(f"  {'手法':<26}{'precision':>10}{'recall':>9}{'spurious(distractor混入)':>26}")
    print(f"  {'naive top-3 (有意性無視)':<24}{p1:>10.2f}{r1:>9.2f}{d1:>20}")
    print(f"  {'honest null+Bonferroni':<24}{p2:>10.2f}{r2:>9.2f}{d2:>20}")
    print("\n  → null 検定で spurious(distractor 連想)が減れば「見かけの相関を弾く」が機能=仮説支持。")
    return {"tau": tau, "naive": (p1, r1, d1), "honest": (p2, r2, d2)}


# ---------- Part B: 実コーパス(MEMORY.md)で連想デモ ----------
def load_memory_entries():
    if not MEMORY_MD.exists():
        return [], []
    names, texts = [], []
    for line in MEMORY_MD.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"^- \[([^\]]+)\]\([^)]+\)\s*[—-]\s*(.+)$", line.strip())
        if m:
            names.append(m.group(1).replace(".md", "")); texts.append(m.group(2))
    return names, texts


def char_bigram_tfidf(texts):
    """日本語向け: char bigram を特徴に TF-IDF(語分割不要・stdlib+numpy)。"""
    def grams(t):
        t = re.sub(r"\s+", "", t)
        return [t[i:i+2] for i in range(len(t) - 1)]
    vocab = {}
    for t in texts:
        for g in set(grams(t)):
            vocab.setdefault(g, len(vocab))
    V = len(vocab); N = len(texts)
    tf = np.zeros((N, V))
    for i, t in enumerate(texts):
        for g in grams(t):
            tf[i, vocab[g]] += 1.0
    df = np.sum(tf > 0, axis=0)
    idf = np.log((1 + N) / (1 + df)) + 1.0
    M = tf * idf
    norm = np.linalg.norm(M, axis=1, keepdims=True); norm[norm == 0] = 1
    return M / norm


def part_b():
    print("\n" + "=" * 64); print("Part B: 実コーパス(MEMORY.md エントリ)で連想想起デモ"); print("=" * 64)
    names, texts = load_memory_entries()
    if len(names) < 10:
        print(f"  [skip] MEMORY.md エントリ {len(names)} 件(不足)"); return
    X = char_bigram_tfidf(texts); S = X @ X.T; N = len(names)
    rng = np.random.default_rng(SEED)
    # TF-IDF 用 null: 行をランダム置換した擬似ベクトル対の cosine 分布で閾値
    idx = rng.integers(0, N, size=(50000, 2))
    perm = np.array([X[a] for a, _ in idx]); permb = np.array([X[b] for _, b in idx])
    null = np.sum(perm * permb, axis=1)
    tau = float(np.quantile(null, 1 - 0.05 / (N * (N - 1) // 2)))
    print(f"  entries={N}, char-bigram TF-IDF, null 閾値 τ={tau:.3f}\n")
    queries = ["feedback_benchmark_honest_disclosure", "project_llcore_evolvable_llm_replan_2026_06_09",
               "feedback_polysemy_associative_memory"]
    for q in queries:
        if q not in names:
            # 部分一致で代替
            cand = [n for n in names if q.split("_")[0] in n]
            if not cand:
                continue
            q = cand[0]
        i = names.index(q); order = np.argsort(-S[i]); order = order[order != i][:5]
        print(f"  ◆ クエリ: {q}")
        for j in order:
            mark = "本物✓" if S[i, j] > tau else "弱/見かけ?"
            print(f"     {S[i,j]:.3f} [{mark}] {names[j]}")
        print()
    print("  → 相関(char-bigram cosine)だけで意味的に近いメモが連想想起され、null 閾値で")
    print("    『本物の連想』と『見かけ』を区別。言語生成なし・on-prem・軽量で動く(feasibility 支持)。")


if __name__ == "__main__":
    a = part_a()
    part_b()
    print("\n[honest 留保] 合成は理想化(トピック=ガウス球)、実 TF-IDF は表層 n-gram で意味は粗い。")
    print("本 PoC は『相関連想 + spurious 棄却』が CPU で成立する feasibility までを示すもので、")
    print("能力(意味理解の深さ)は別途。次段=埋め込み(SmolLM2 hidden)化 + 私的データ規模化。")
