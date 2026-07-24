$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
uv run --frozen python "$Root/scripts/validate.py" @args
