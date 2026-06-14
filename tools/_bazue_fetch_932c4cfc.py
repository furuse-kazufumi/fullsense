#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch the public Qiita article 932c4cfc6cfca636504a and dump body/title/tags/private."""
from __future__ import annotations

import json
import sys
import urllib.request

sys.path.insert(0, r"D:/projects/fullsense/tools")
from qiita_public_post import get_token  # noqa: E402

for s in ("stdout", "stderr"):
    try:
        getattr(sys, s).reconfigure(encoding="utf-8")
    except Exception:
        pass

ITEM_ID = "932c4cfc6cfca636504a"
tok = get_token()
if not tok:
    print("NO TOKEN")
    sys.exit(2)

req = urllib.request.Request(
    f"https://qiita.com/api/v2/items/{ITEM_ID}",
    headers={"Authorization": "Bearer " + tok},
)
with urllib.request.urlopen(req, timeout=30) as r:
    data = json.loads(r.read().decode("utf-8"))

print("===TITLE===")
print(data.get("title"))
print("===PRIVATE===")
print(data.get("private"))
print("===TAGS===")
print(json.dumps(data.get("tags"), ensure_ascii=False))
print("===BODYLEN===")
print(len(data.get("body", "")))
print("===BODY===")
print(data.get("body", ""))
