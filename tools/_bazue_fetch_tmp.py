import sys, json, urllib.request
sys.path.insert(0, r'D:/projects/fullsense/tools')
from qiita_public_post import get_token

tok = get_token()
ITEM = "ab3839f8b5b3ea91311e"
req = urllib.request.Request(
    f"https://qiita.com/api/v2/items/{ITEM}",
    headers={"Authorization": "Bearer " + tok},
)
with urllib.request.urlopen(req) as r:
    data = json.load(r)

print("TITLE:", data["title"])
print("PRIVATE:", data["private"])
print("TAGS:", json.dumps([{"name": t["name"], "versions": t.get("versions", [])} for t in data["tags"]], ensure_ascii=False))
print("BODYLEN:", len(data["body"]))
print("=== HEADINGS ===")
for i, line in enumerate(data["body"].splitlines()):
    if line.startswith("#") or "Honest" in line or "まとめ" in line or "おわりに" in line or "おまけ" in line:
        print(i, repr(line))
print("=== FIRST 60 LINES ===")
for i, line in enumerate(data["body"].splitlines()[:60]):
    print(i, line)
# detect existing bazue images
print("=== EXISTING bazue refs ===")
for line in data["body"].splitlines():
    if "bazue_all" in line:
        print(line)
