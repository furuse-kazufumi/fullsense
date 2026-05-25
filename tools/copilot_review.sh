#!/usr/bin/env bash
# copilot_review.sh — read-only cross-AI REVIEW via GitHub Copilot CLI (backstage tool).
#
# FullSense policy (feedback_external_ai_verify): external AIs (Copilot / Codex / Gemini) are
# for INFO-GATHERING / REVIEW / SECOND-OPINION ONLY — never coding/refactor; findings must be
# verified against real code by Claude. So this wrapper is READ-ONLY by construction:
#   --allow-tool read  (no write, no bash) + --no-ask-user + -s (quiet) + -p (one-shot program mode).
#
# Prereq (one-time, user does the interactive parts):
#   npm install -g @github/copilot     # or: curl -fsSL https://gh.io/copilot-install | bash
#   copilot                            # first run: trust folder + browser GitHub login (Copilot Pro)
#
# Usage:
#   ./copilot_review.sh <target-path> "<review prompt>"
#   OUT_FILE=review.out MODEL=gpt-5.2 ./copilot_review.sh . "Review test quality; bullet-point fixes"
#
# Then Claude reads $OUT_FILE and verifies every claim against the real code.
set -euo pipefail

if ! command -v copilot >/dev/null 2>&1; then
  echo "ERROR: 'copilot' CLI not found. Install: npm install -g @github/copilot ; then run 'copilot' once to log in." >&2
  exit 127
fi
if [ $# -lt 2 ]; then
  echo "Usage: $0 <target-path> <review prompt...>" >&2
  exit 1
fi

TARGET_PATH="$1"; shift
PROMPT="$*"
OUT_FILE="${OUT_FILE:-copilot_review.out}"
MODEL="${MODEL:-}"            # optional: e.g. gpt-5.2 / claude-opus-4.6 ; empty = Copilot default

# Frame as review-only so the model returns text, not edits.
FULL_PROMPT="You are a READ-ONLY reviewer. Do NOT modify files. Review the code under '${TARGET_PATH}'.
${PROMPT}
Return concise, actionable findings as a prioritized bullet list. Cite file:line where possible."

set -x
copilot \
  --add-dir "$TARGET_PATH" \
  --allow-tool read \
  ${MODEL:+--model "$MODEL"} \
  -p "$FULL_PROMPT" \
  -s \
  --no-ask-user \
  > "$OUT_FILE" 2> "${OUT_FILE}.err" || { set +x; echo "copilot failed (see ${OUT_FILE}.err)" >&2; exit 1; }
set +x
echo "Copilot review saved to: $OUT_FILE  (verify findings against real code — feedback_external_ai_verify)"
