$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

function Require-Command($Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Missing required command: $Name"
    }
}

function Require-Version($Label, $Actual, $Expected) {
    if ($Actual -ne $Expected) {
        throw "$Label version mismatch: expected $Expected, got $Actual"
    }
}

Require-Command python
Require-Command uv
Require-Command node
Require-Command pnpm
Require-Command docker

Require-Version "Python" ((python --version).Split()[1]) "3.13.14"
Require-Version "uv" ((uv --version).Split()[1]) "0.11.32"
Require-Version "Node.js" (node --version) "v24.18.0"
Require-Version "pnpm" (pnpm --version) "11.14.0"

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example"
} else {
    Write-Host ".env already exists; leaving unchanged"
}

uv sync --frozen
pnpm install --frozen-lockfile
docker compose -f infra/compose.yaml up -d

for ($i = 0; $i -lt 30; $i++) {
    $status = docker compose -f infra/compose.yaml ps --format json
    if ($status -match "healthy") { break }
    Start-Sleep -Seconds 2
}

$env:KRDT_DATABASE_URL = "postgresql+psycopg://krdt:change-me@127.0.0.1:5432/krdt"
Push-Location apps/api
uv run alembic upgrade head
Pop-Location

Write-Host @"
Bootstrap complete.

Next commands:
  uv run --project apps/api uvicorn krdt_api.main:app --reload --host 0.0.0.0 --port 8000
  pnpm --filter @krdt/web dev
  uv run --frozen python scripts/validate.py
"@
