# Puts figcraft-review (the CLI) and figcraft-agent (the chat) on PATH as .cmd shims into this folder,
# so keep the folder where it is. The shims go to %LOCALAPPDATA%\figcraft-review\bin, added to the user PATH.
$ErrorActionPreference = "Stop"
$here = $PSScriptRoot
$bin = Join-Path $env:LOCALAPPDATA "figcraft-review\bin"
New-Item -ItemType Directory -Force $bin | Out-Null
$py = if (Get-Command py -ErrorAction SilentlyContinue) { "py -3" } else { "python" }
Set-Content -Encoding ASCII (Join-Path $bin "figcraft-review.cmd") "@$py `"$here\agent\review.py`" %*"
Set-Content -Encoding ASCII (Join-Path $bin "figcraft-agent.cmd") "@$py `"$here\sidecar\launch.py`" %*"
$path = [Environment]::GetEnvironmentVariable("Path", "User")
if (($path -split ";") -notcontains $bin) {
  [Environment]::SetEnvironmentVariable("Path", "$path;$bin", "User")
  Write-Host "Added $bin to your PATH (open a new terminal)."
}
Write-Host "Installed figcraft-review and figcraft-agent in $bin"
if (-not (Get-Command figcraft-cli -ErrorAction SilentlyContinue)) {
  $cli = Join-Path ${env:ProgramFiles} "ArtCraft\FigCraft\figcraft-cli.exe"
  if (-not (Test-Path $cli)) { Write-Host "figcraft-cli not found: install FigCraft or set FIGCRAFT_CLI." }
}
Write-Host ""
Write-Host "Plugin: in FigCraft, Plugins > Development > Import plugin from manifest... and pick"
Write-Host "  $here\plugin\figcraft-plugin.json"
Write-Host "Start FigCraft with its control channel: figcraft.exe --control 7979"
