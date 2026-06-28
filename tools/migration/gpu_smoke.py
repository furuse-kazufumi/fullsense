#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gpu_smoke.py -- RTX 5090 (Blackwell sm_120) Day-1 GPU smoke test.

新 GPU マシン(RTX 5090 Founders / Blackwell sm_120 / 32GB)移行後の最小
GPU 健全性チェック(スタンドアロン)。`verify_new_machine.ps1` のチェック 2
から呼ばれるが、単体でも実行できる。

正本: D:/projects/fullsense/docs/research/gpu_pc_migration_plan_2026-06-28.md
      (§4-4 torch cu128 検証 / §5 検証チェックリスト)

使い方 (PYTHONUTF8=1 を前置推奨。stdout は UTF-8 で固定する):
    set PYTHONUTF8=1
    py -3.11 gpu_smoke.py

チェック内容 (順に / 途中失敗でも可能な範囲で続行):
    1. torch import
    2. torch.cuda.is_available()
    3. torch.cuda.get_device_capability(0) == (12, 0)   # Blackwell sm_120
    4. 小 GEMM: torch.randn(512,512,cuda) @ ... が "no kernel image" を出さず走る
    5. nn.Linear を .to('cuda') して forward が通る

出力: 結果を 1 行 JSON で stdout に出す (status は snake_case)。
終了コード (verify 側がこれで PASS/SKIP/FAIL を判定):
    0  = 全 GPU チェック PASS
    2  = cuda 利用不可 / torch import 不可 = 環境差 (verify 側は SKIP 判定)
    1  = cuda は使えるが capability / GEMM / Linear のいずれかで FAIL (実不具合)

exit 2 を 1 (FAIL) と分けるのが要点: 現機(GPU 無し)では「環境が違うだけ」
であって不具合ではないため、verify 側がクリーンに SKIP できるようにする。
"""
from __future__ import annotations

import json
import sys

# cp932 環境でも JSON / 記号が化けないよう stdout/stderr を UTF-8 に固定。
for _stream in ("stdout", "stderr"):
    try:
        getattr(sys, _stream).reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

# 終了コードの意味 (verify_new_machine.ps1 と契約)
EXIT_PASS = 0       # 全チェック PASS
EXIT_FAIL = 1       # cuda 利用可だが途中で FAIL = 実不具合
EXIT_ENV_SKIP = 2   # cuda/torch が無い = 環境差 -> verify は SKIP

EXPECTED_CAPABILITY = (12, 0)  # Blackwell sm_120 (RTX 5090)


def _emit(result: dict, exit_code: int) -> int:
    """結果 JSON を 1 行で stdout に出して終了コードを返す。"""
    result["exit_code"] = exit_code
    try:
        sys.stdout.write(json.dumps(result, ensure_ascii=False) + "\n")
        sys.stdout.flush()
    except Exception:
        # stdout が壊れていても終了コードだけは返す
        pass
    return exit_code


def main() -> int:
    result: dict = {
        "tool": "gpu_smoke",
        "torch_importable": False,
        "torch_version": None,
        "cuda_available": False,
        "device_name": None,
        "capability": None,
        "capability_ok": False,
        "gemm_ok": False,
        "linear_ok": False,
        "checks": [],
        "overall": "skip",
        "error": None,
    }

    def add(name: str, status: str, detail: str) -> None:
        result["checks"].append({"name": name, "status": status, "detail": detail})

    # --- 1. torch import -------------------------------------------------
    try:
        import torch
    except Exception as exc:  # torch 未導入 = 環境差
        result["error"] = f"torch import failed: {exc!r}"
        result["overall"] = "skip"
        add("torch_import", "skip", f"torch import failed: {exc}")
        return _emit(result, EXIT_ENV_SKIP)

    result["torch_importable"] = True
    result["torch_version"] = getattr(torch, "__version__", "unknown")
    add("torch_import", "pass", f"torch {result['torch_version']}")

    # --- 2. cuda available ----------------------------------------------
    try:
        cuda_ok = bool(torch.cuda.is_available())
    except Exception as exc:
        cuda_ok = False
        add("cuda_available", "skip", f"is_available() raised: {exc}")
    result["cuda_available"] = cuda_ok

    if not cuda_ok:
        # GPU が無い / driver 未導入 = 環境差。FAIL ではなく SKIP。
        add("cuda_available", "skip", "torch.cuda.is_available() == False (GPU 無し環境)")
        result["overall"] = "skip"
        return _emit(result, EXIT_ENV_SKIP)

    add("cuda_available", "pass", "torch.cuda.is_available() == True")

    # device 名 (情報用 / 失敗しても致命的でない)
    try:
        result["device_name"] = torch.cuda.get_device_name(0)
    except Exception as exc:
        result["device_name"] = None
        add("device_name", "fail", f"get_device_name(0) raised: {exc}")

    # ここから先は cuda 利用可。失敗は実不具合 (EXIT_FAIL)。
    failed = False

    # --- 3. compute capability == (12, 0) (Blackwell sm_120) -------------
    try:
        cap = torch.cuda.get_device_capability(0)
        cap = (int(cap[0]), int(cap[1]))
        result["capability"] = list(cap)
        if cap == EXPECTED_CAPABILITY:
            result["capability_ok"] = True
            add("capability", "pass", f"get_device_capability(0) == {cap} (Blackwell sm_120)")
        else:
            result["capability_ok"] = False
            failed = True
            add(
                "capability",
                "fail",
                f"get_device_capability(0) == {cap}, expected {EXPECTED_CAPABILITY} "
                f"(sm_120 でない GPU か torch wheel の不整合)",
            )
    except Exception as exc:
        failed = True
        add("capability", "fail", f"get_device_capability(0) raised: {exc}")

    # --- 4. 小 GEMM が "no kernel image" を出さず走るか ------------------
    # CUDA は非同期なので synchronize + 値読み出しで実カーネル実行を強制する。
    try:
        a = torch.randn(512, 512, device="cuda")
        b = torch.randn(512, 512, device="cuda")
        c = a @ b
        torch.cuda.synchronize()
        s = float(c.sum().item())
        result["gemm_ok"] = True
        add("gemm", "pass", f"512x512 GEMM 成功 (sum={s:.3e}, no kernel image エラー無し)")
    except Exception as exc:
        failed = True
        msg = str(exc)
        hint = ""
        if "no kernel image" in msg.lower():
            hint = " <- torch wheel が sm_120 未対応 (cu128/nightly へ更新)"
        add("gemm", "fail", f"GEMM 失敗: {exc}{hint}")

    # --- 5. nn.Linear を .to('cuda') して forward ----------------------
    try:
        lin = torch.nn.Linear(256, 256).to("cuda")
        x = torch.randn(8, 256, device="cuda")
        y = lin(x)
        torch.cuda.synchronize()
        ys = float(y.sum().item())
        result["linear_ok"] = True
        add("linear_forward", "pass", f"nn.Linear(256,256).to('cuda') forward 成功 (sum={ys:.3e})")
    except Exception as exc:
        failed = True
        msg = str(exc)
        hint = ""
        if "no kernel image" in msg.lower():
            hint = " <- torch wheel が sm_120 未対応 (cu128/nightly へ更新)"
        add("linear_forward", "fail", f"Linear forward 失敗: {exc}{hint}")

    if failed:
        result["overall"] = "fail"
        return _emit(result, EXIT_FAIL)

    result["overall"] = "pass"
    return _emit(result, EXIT_PASS)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(EXIT_FAIL)
