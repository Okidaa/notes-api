#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

PORT=18765
export PORT

python3 app.py > /tmp/notes-api-test.log 2>&1 &
SERVER_PID=$!

cleanup() {
    kill "$SERVER_PID" 2>/dev/null || true
}
trap cleanup EXIT

for i in {1..30}; do
    if curl -fsS "http://127.0.0.1:$PORT/healthz" >/dev/null; then
        break
    fi
    sleep 0.2
done

PASS=0
TOTAL=3

if curl -fsS "http://127.0.0.1:$PORT/healthz" | grep -q '"status": "ok"'; then
    PASS=$((PASS + 1))
fi

if curl -fsS "http://127.0.0.1:$PORT/" | grep -q 'Notes API is running'; then
    PASS=$((PASS + 1))
fi

if curl -fsS "http://127.0.0.1:$PORT/notes" | grep -q '"notes": \[\]'; then
    PASS=$((PASS + 1))
fi

echo "TESTS: $PASS/$TOTAL"

if [ "$PASS" -ne "$TOTAL" ]; then
    exit 1
fi
