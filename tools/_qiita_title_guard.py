#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared title/baseline guard helpers for Qiita posting tools."""
from __future__ import annotations

from collections.abc import Callable, Mapping
from functools import lru_cache
from pathlib import Path
import subprocess

from _frontmatter import resolve_body_title, split_frontmatter

EMPTY_TREE_HASH = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def normalize_nullish_scalar(value) -> str | None:
    if isinstance(value, list):
        value = value[0] if value else None
    if value is None:
        return None
    cleaned = str(value).strip()
    return cleaned if cleaned and cleaned.lower() not in ("null", "none") else None


def meta_has_identity(meta: Mapping[str, object], *keys: str) -> bool:
    return any(normalize_nullish_scalar(meta.get(key)) for key in keys)


def resolve_frontmatter_title(meta: Mapping[str, object]) -> str:
    return normalize_nullish_scalar(meta.get("title")) or ""


def resolve_body_publish_title(body: str) -> str:
    return (resolve_body_title(body) or "").strip()


def infer_publish_title(meta: Mapping[str, object], body: str) -> str:
    frontmatter_title = resolve_frontmatter_title(meta)
    if frontmatter_title:
        return frontmatter_title
    return resolve_body_publish_title(body)


def has_title_mismatch(meta: Mapping[str, object], body: str) -> bool:
    frontmatter_title = resolve_frontmatter_title(meta)
    body_title = resolve_body_publish_title(body)
    return bool(frontmatter_title and body_title and frontmatter_title != body_title)


def title_findings(meta: Mapping[str, object], body: str) -> list[str]:
    return ["[TITLE-MISMATCH]"] if has_title_mismatch(meta, body) else []


def resolve_repo_relative_path(repo_root: Path, path_str: str | Path) -> Path:
    path = Path(path_str)
    if not path.is_absolute():
        path = repo_root / path
    return path


def git_ref_exists(repo_root: Path, ref: str) -> bool:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", ref],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=repo_root,
        )
    except OSError:
        return False
    return result.returncode == 0


@lru_cache(maxsize=1)
def resolve_upstream_ref(repo_root_str: str) -> str | None:
    repo_root = Path(repo_root_str)
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=repo_root,
        )
    except OSError:
        return None
    upstream = result.stdout.strip()
    return upstream or None


@lru_cache(maxsize=1)
def resolve_title_baseline_commit(repo_root_str: str) -> str | None:
    repo_root = Path(repo_root_str)
    refs: list[str] = []
    upstream = resolve_upstream_ref(repo_root_str)
    if upstream:
        refs.append(upstream)
    for fallback in ("origin/main", "origin/master", "main", "master"):
        if fallback not in refs and git_ref_exists(repo_root, fallback):
            refs.append(fallback)
    for ref in refs:
        try:
            result = subprocess.run(
                ["git", "merge-base", "HEAD", ref],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                cwd=repo_root,
            )
        except OSError:
            return None
        commit = result.stdout.strip()
        if commit:
            return commit
    if git_ref_exists(repo_root, "HEAD^"):
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD^"],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                cwd=repo_root,
            )
        except OSError:
            return None
        commit = result.stdout.strip()
        if commit:
            return commit
    if git_ref_exists(repo_root, "HEAD"):
        return EMPTY_TREE_HASH
    return None


@lru_cache(maxsize=None)
def load_git_text_at_rev(repo_root_str: str, rev: str, path_str: str) -> str | None:
    repo_root = Path(repo_root_str)
    path = resolve_repo_relative_path(repo_root, path_str)
    try:
        rel = path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return None
    try:
        result = subprocess.run(
            ["git", "show", f"{rev}:{rel}"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=repo_root,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout


def load_title_baseline_text(repo_root: Path, path: str | Path) -> str | None:
    baseline = resolve_title_baseline_commit(str(repo_root))
    if not baseline:
        return None
    return load_git_text_at_rev(str(repo_root), baseline, str(path))


def legacy_title_mismatch_is_compatible(
    baseline_text: str,
    meta: Mapping[str, object],
    body: str,
    infer_title: Callable[[Mapping[str, object], str], str],
) -> bool:
    baseline_meta, baseline_body = split_frontmatter(baseline_text)
    baseline_fm_title = normalize_nullish_scalar(baseline_meta.get("title")) or ""
    baseline_body_title = (resolve_body_title(baseline_body) or "").strip()
    baseline_mismatch = bool(
        baseline_fm_title and baseline_body_title and baseline_fm_title != baseline_body_title
    )
    baseline_publish_title = infer_title(baseline_meta, baseline_body)
    current_publish_title = infer_title(meta, body)
    return baseline_mismatch and baseline_publish_title == current_publish_title


def title_change_requires_human_gate(
    meta: Mapping[str, object],
    body: str,
    *,
    baseline_text: str | None,
    live_identity_keys: tuple[str, ...],
) -> bool:
    current_publish_title = infer_publish_title(meta, body)
    if baseline_text is None:
        return meta_has_identity(meta, *live_identity_keys) and bool(current_publish_title)

    baseline_meta, baseline_body = split_frontmatter(baseline_text)
    baseline_publish_title = infer_publish_title(baseline_meta, baseline_body)
    if current_publish_title == baseline_publish_title:
        return False
    return meta_has_identity(meta, *live_identity_keys) or meta_has_identity(
        baseline_meta, *live_identity_keys
    )


def should_report_title_mismatch(
    meta: Mapping[str, object],
    body: str,
    *,
    baseline_text: str | None,
    live_identity_keys: tuple[str, ...],
) -> bool:
    if not has_title_mismatch(meta, body):
        return False
    if baseline_text is None:
        return True
    baseline_meta, baseline_body = split_frontmatter(baseline_text)
    baseline_mismatch = has_title_mismatch(baseline_meta, baseline_body)
    if baseline_mismatch and not title_change_requires_human_gate(
        meta,
        body,
        baseline_text=baseline_text,
        live_identity_keys=live_identity_keys,
    ):
        return False
    return True


def should_block_title_mismatch(
    meta: Mapping[str, object],
    body: str,
    *,
    baseline_text: str | None,
    live_identity_keys: tuple[str, ...],
) -> bool:
    if not has_title_mismatch(meta, body):
        return False
    if not meta_has_identity(meta, *live_identity_keys):
        return True
    if baseline_text is None:
        return True
    if legacy_title_mismatch_is_compatible(baseline_text, meta, body, infer_publish_title):
        return False
    return True
