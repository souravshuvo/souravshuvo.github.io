# 1-Click Runner to automatically generate ASO Assets for all games in parallel
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ToolPath = Join-Path $ScriptDir "batch_asset_builder.py"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  ANTIGRAVITY AUTOMATED GAME ASO ASSET BATCH BUILDER" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

python $ToolPath --all --parallel 4

Write-Host "`nAll game assets generated successfully!" -ForegroundColor Green
Write-Host "Location: D:\souravshuvo.github.io\game_store_assets" -ForegroundColor White