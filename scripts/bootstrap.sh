#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

require_version() {
  local label="$1"
  local actual="$2"
  local expected="$3"
  if [[ "$actual" != "$expected" ]]; then
    echo "$label version mismatch: expected $expected, got $actual" >&2
    exit 1
  fi
}

require_cmd python3
require_cmd uv
require_cmd node
require_cmd pnpm
require_cmd docker

require_version "Python" "$(python3 --version | awk '{print $2}')" "3.13.14"
require_version "uv" "$(uv --version | awk '{print $2}')" "0.11.32"
require_version "Node.js" "$(node --version)" "v24.18.0"
require_version "pnpm" "$(pnpm --version)" "11.14.0"

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example"
else
  echo ".env already exists; leaving unchanged"
fi

uv sync --frozen
pnpm install --frozen-lockfile

docker compose -f infra/compose.yaml up -d

for _ in $(seq 1 30); do
  if docker compose -f infra/compose.yaml ps --format json | grep -qi healthy; then
    break
  fi
  sleep 2
done

KRDT_DATABASE_URL="postgresql+psycopg://krdt:change-me@127.0.0.1:5432/krdt" \
  uv run --project apps/api alembic -c apps/api/alembic.ini upgrade head

cat <<'EOF'
Bootstrap complete.

Next commands:
  uv run --project apps/api uvicorn krdt_api.main:app --reload --host 0.0.0.0 --port 8000
  pnpm --filter @krdt/web dev
  uv run --frozen python scripts/validate.py
EOF
