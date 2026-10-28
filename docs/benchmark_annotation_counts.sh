#!/usr/bin/env bash
# Measure MO-1: median latency for annotation counts API (5 runs).
set -euo pipefail

TASK_ID="${1:?Usage: $0 <task_id> [sessionid_cookie_value]}"
SESSION="${2:-}"

if [[ -z "$SESSION" ]]; then
  echo "Pass sessionid as second argument (from browser cookies after login)." >&2
  exit 1
fi

URL="http://localhost:8080/api/test/tasks/${TASK_ID}/annotation-counts"
echo "URL=$URL"
echo "runs_ms:"

times=()
for i in 1 2 3 4 5; do
  ms=$(curl -s -o /dev/null -w '%{time_total}' \
    -H "Cookie: sessionid=${SESSION}" \
    "$URL" | awk '{printf "%.0f", $1 * 1000}')
  echo "  run${i}=${ms}"
  times+=("$ms")
done

python3 - <<'PY' "${times[@]}"
import statistics, sys
vals = [int(x) for x in sys.argv[1:]]
print(f"median_ms={statistics.median(vals):.0f}")
print(f"min_ms={min(vals)} max_ms={max(vals)}")
PY
