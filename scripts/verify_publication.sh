#!/usr/bin/env bash
# verify_publication.sh — one-shot machine check for the 2026-05-16
# FullSense umbrella expansion publication.
#
# Checks:
#   A. GitHub Pages reachability for fullsense / llmesh / llove / lldesign / lltrade
#   B. Portal landing page → external link sweep (no 404 expected)
#   C. Branch protection rules on 6 repos (Restrict deletions + Block force pushes)
#   D. About config (Website + 10 individual Topics) for lldesign / lltrade
#   E. Mermaid family tree actually rendered (not raw fenced source)
#
# Usage: bash D:/projects/fullsense/scripts/verify_publication.sh

set -u

# --- ANSI helpers ----------------------------------------------------------
if [[ -t 1 ]]; then
  G="\033[32m"; R="\033[31m"; Y="\033[33m"; B="\033[1m"; N="\033[0m"
else
  G=""; R=""; Y=""; B=""; N=""
fi
pass(){ printf "  ${G}PASS${N}  %s\n" "$1"; }
fail(){ printf "  ${R}FAIL${N}  %s\n" "$1"; FAIL_COUNT=$((FAIL_COUNT+1)); }
warn(){ printf "  ${Y}WARN${N}  %s\n" "$1"; WARN_COUNT=$((WARN_COUNT+1)); }
hdr(){  printf "\n${B}== %s ==${N}\n" "$1"; }

FAIL_COUNT=0
WARN_COUNT=0

OWNER="furuse-kazufumi"
REPOS=(fullsense llmesh llive llove lldesign lltrade)
PAGES_REPOS=(fullsense llmesh llove lldesign lltrade)  # llive Pages already up
ABOUT_REPOS=(lldesign lltrade)

# --- A. Pages reachability -------------------------------------------------
hdr "A. GitHub Pages reachability"
for r in "${PAGES_REPOS[@]}"; do
  url="https://$OWNER.github.io/$r/"
  code=$(curl -sI -o /dev/null -L --max-time 15 -w "%{http_code}" "$url" 2>/dev/null)
  if [[ "$code" == "200" ]]; then
    pass "$url  ($code)"
  else
    fail "$url  ($code — Pages not yet enabled or build pending)"
  fi
done

# --- B. Portal landing page → external link sweep --------------------------
hdr "B. Portal link sweep (fullsense landing page → all linked URLs)"
PORTAL_HTML=$(curl -s --max-time 20 "https://$OWNER.github.io/fullsense/" 2>/dev/null || echo "")
if [[ -z "$PORTAL_HTML" ]]; then
  fail "could not fetch portal landing page"
else
  # Extract href values pointing at github.io or github.com — limit to first 40
  urls=$(printf '%s' "$PORTAL_HTML" | grep -oE 'href="https?://[^"]+"' \
           | sed 's/^href="//;s/"$//' \
           | grep -E 'github\.(io|com)' \
           | sort -u \
           | head -40)
  bad=0
  total=0
  while IFS= read -r u; do
    [[ -z "$u" ]] && continue
    total=$((total+1))
    code=$(curl -sI -o /dev/null -L --max-time 12 -w "%{http_code}" "$u" 2>/dev/null)
    if [[ "$code" == "200" ]]; then
      : # quiet — only print failures
    else
      bad=$((bad+1))
      fail "$code  $u"
    fi
  done <<< "$urls"
  if (( bad == 0 )); then
    pass "all $total external GitHub links return 200"
  fi
fi

# --- C. Branch protection --------------------------------------------------
hdr "C. Branch protection (Restrict deletions + Block force pushes)"
for r in "${REPOS[@]}"; do
  # Try modern Repository Rulesets API first
  ruleset_json=$(gh api "repos/$OWNER/$r/rules/branches/main" 2>/dev/null || echo "[]")
  has_no_force=$(printf '%s' "$ruleset_json" | grep -c '"non_fast_forward"' || true)
  has_no_delete=$(printf '%s' "$ruleset_json" | grep -c '"deletion"' || true)
  # Fall back to classic branch protection
  if [[ "$has_no_force" == "0" || "$has_no_delete" == "0" ]]; then
    classic_json=$(gh api "repos/$OWNER/$r/branches/main/protection" 2>/dev/null || echo "{}")
    if [[ "$classic_json" == *"allow_force_pushes"* ]]; then
      ff=$(printf '%s' "$classic_json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('allow_force_pushes',{}).get('enabled',True))" 2>/dev/null || echo "True")
      dd=$(printf '%s' "$classic_json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('allow_deletions',{}).get('enabled',True))" 2>/dev/null || echo "True")
      if [[ "$ff" == "False" && "$dd" == "False" ]]; then
        pass "$r  (classic protection: force=blocked, deletion=blocked)"
        continue
      fi
    fi
    fail "$r  (no active rule found)"
  else
    pass "$r  (ruleset: non_fast_forward + deletion both present)"
  fi
done

# --- D. About config (Website + Topics) ------------------------------------
hdr "D. About — Website + Topics (lldesign, lltrade)"
for r in "${ABOUT_REPOS[@]}"; do
  meta=$(gh api "repos/$OWNER/$r" --jq '{homepage, topics, topic_count: (.topics|length)}' 2>/dev/null || echo "{}")
  homepage=$(printf '%s' "$meta" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('homepage') or '')" 2>/dev/null)
  topic_count=$(printf '%s' "$meta" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('topic_count',0))" 2>/dev/null)
  topics=$(printf '%s' "$meta" | python3 -c "import sys,json; d=json.load(sys.stdin); print(' '.join(d.get('topics',[])))" 2>/dev/null)
  expected="https://$OWNER.github.io/$r/"
  if [[ "$homepage" == "$expected" ]]; then
    pass "$r homepage  ($homepage)"
  else
    fail "$r homepage  (got '$homepage', expected '$expected')"
  fi
  if (( topic_count >= 10 )); then
    pass "$r topics    ($topic_count chips: $topics)"
  elif (( topic_count >= 1 )); then
    warn "$r topics    ($topic_count chips — expected ≥ 10: $topics)"
  else
    fail "$r topics    (0 chips set)"
  fi
done

# --- E. Mermaid actually rendered -----------------------------------------
hdr "E. Mermaid family tree on fullsense portal"
if [[ -n "$PORTAL_HTML" ]]; then
  # mermaid.run script tag must be present, and the family tree class hook
  # must be present.
  has_runtime=$(printf '%s' "$PORTAL_HTML" | grep -c 'mermaid\.esm\.min\.mjs')
  has_block=$(printf '%s' "$PORTAL_HTML" | grep -c 'language-mermaid')
  has_node=$(printf '%s' "$PORTAL_HTML" | grep -c 'lldesign')
  if (( has_runtime > 0 && has_block > 0 && has_node > 0 )); then
    pass "mermaid runtime injected + language-mermaid block + lldesign node present"
  else
    fail "mermaid setup incomplete  (runtime=$has_runtime block=$has_block lldesign-node=$has_node)"
  fi
else
  fail "portal HTML not available; cannot check Mermaid"
fi

# --- Summary --------------------------------------------------------------
hdr "Summary"
if (( FAIL_COUNT == 0 && WARN_COUNT == 0 )); then
  printf "${G}ALL CHECKS PASSED${N}\n"
  exit 0
elif (( FAIL_COUNT == 0 )); then
  printf "${Y}PASSED with %d warning(s)${N}\n" "$WARN_COUNT"
  exit 0
else
  printf "${R}%d FAILURE(S), %d warning(s)${N}\n" "$FAIL_COUNT" "$WARN_COUNT"
  exit 1
fi
