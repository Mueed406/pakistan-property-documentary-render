param(
    [string]$ProjectPath = ".",
    [string]$Hosts = "codex,claude,antigravity,gemini",
    [string]$BlenderExecutable = "",
    [switch]$InstallSketchfabAddon
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$installer = Join-Path $here "install.py"
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git for Windows is required; install Git before running this script."
}
$python = Get-Command py -ErrorAction SilentlyContinue
if ($python) {
    & py -3 $installer install --project $ProjectPath --hosts $Hosts
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python $installer install --project $ProjectPath --hosts $Hosts
} else {
    throw "Python 3 is required for pinned Git skill installation."
}
if ($LASTEXITCODE -ne 0) {
    throw "Agent skill installer failed. Existing skills were not overwritten."
}

$projectAbs = (Resolve-Path $ProjectPath).Path
$downloads = Join-Path $projectAbs "_verified_tools"
New-Item -Path $downloads -ItemType Directory -Force | Out-Null
$zipPath = Join-Path $downloads "sketchfab-plugin-1-8-0.zip"
$url = "https://github.com/sketchfab/blender-plugin/releases/download/1.8.0/sketchfab-plugin-1-8-0.zip"
$expected = "a6be9e8348a67b66faa236c7aba4c4980db0bda76ab5db17eddd077f66ca71d7"
if (-not (Test-Path $zipPath)) {
    Invoke-WebRequest -UseBasicParsing -Uri $url -OutFile $zipPath
}
$actual = (Get-FileHash -Algorithm SHA256 -Path $zipPath).Hash.ToLowerInvariant()
if ($actual -ne $expected) {
    Remove-Item -Path $zipPath -Force
    throw "The official Sketchfab 1.8.0 ZIP failed published SHA256 verification."
}
Write-Host "PASS: 71 skill folders copied to the selected project."
Write-Host "PASS: official Sketchfab 1.8.0 ZIP verified at $zipPath"

if ($InstallSketchfabAddon) {
    if ([string]::IsNullOrWhiteSpace($BlenderExecutable) -or -not (Test-Path $BlenderExecutable)) {
        throw "For unattended Blender addon installation supply -BlenderExecutable pointing to your installed blender.exe."
    }
    $script = Join-Path $here "install_sketchfab_blender.py"
    & $BlenderExecutable --background --python $script -- --zip $zipPath
    if ($LASTEXITCODE -ne 0) {
        throw "Blender add-on installation failed. Check console output and use Blender GUI installation if needed."
    }
    Write-Host "PASS: Blender reported a successful Sketchfab add-on install/enable."
} else {
    Write-Host "To install Sketchfab: Blender > Edit > Preferences > Add-ons > Install from Disk > $zipPath"
    Write-Host "Sketchfab login, Blender MCP, Blender 3D tools and Meshy remain separate."
}
