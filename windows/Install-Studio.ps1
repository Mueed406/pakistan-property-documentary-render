#Requires -Version 5.1
<#
.SYNOPSIS
Installs and verifies an AI-controllable documentary production suite on Windows.
.EXAMPLE
powershell -ExecutionPolicy Bypass -File windows\Install-Studio.ps1 -Install
.NOTES
Runs only when user launches on their Windows machine. Does NOT create accounts or spend API credits.
Installs official WinGet packages and project-local Python/Node dependencies.
Remotion free-license eligibility must be confirmed by the user before commercial use.
#>
[CmdletBinding()]
param(
  [switch]$Install,
  [switch]$WithShotcut,
  [switch]$WithAudacity,
  [switch]$SkipRemotion,
  [string]$BlenderVersion = "4.5.14"
)
$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$root=(Get-Location).Path
Write-Host "AI Documentary Studio for Windows / version 1" -ForegroundColor Cyan
Write-Host "Project: $root"
Write-Host "Install requested: $Install"
if(-not $Install) {
  Write-Host "AUDIT ONLY: Add -Install to authorize WinGet/package installation." -ForegroundColor Yellow
  & (Join-Path $PSScriptRoot 'Verify-Studio.ps1')
  exit $LASTEXITCODE
}
if(-not (Get-Command winget -ErrorAction SilentlyContinue)){
  throw "WinGet is required. Install Microsoft's App Installer first: https://aka.ms/getwinget"
}
function Install-Package([string]$Id, [string]$Version="") {
  Write-Host "Reviewing WinGet: $Id" -ForegroundColor Cyan
  $args=@('install','--id',$Id,'--exact','--source','winget','--accept-source-agreements','--accept-package-agreements','--disable-interactivity')
  if($Version){$args+=@('--version',$Version)}
  & winget @args
  if($LASTEXITCODE -ne 0) {
    throw "WinGet failed for $Id (version '$Version'). Run: winget show --id $Id --versions. Nothing will be silently substituted."
  }
}
# Install only essentials; preserve already-installed user software where detected.
$required=@(
  @{Exe='py.exe';Id='Python.Python.3.11'},
  @{Exe='node.exe';Id='OpenJS.NodeJS.LTS'},
  @{Exe='ffmpeg.exe';Id='Gyan.FFmpeg'},
  @{Exe='git.exe';Id='Git.Git'}
)
foreach($pkg in $required) {
  if(Get-Command $pkg.Exe -ErrorAction SilentlyContinue){
    Write-Host "Already installed: $($pkg.Exe)"
  } else { Install-Package $pkg.Id }
}
$blenderPaths=@(
 (Get-Command blender.exe -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Source -ErrorAction SilentlyContinue),
 (Get-ChildItem "$env:ProgramFiles\Blender Foundation\Blender *\blender.exe" -ErrorAction SilentlyContinue | Sort-Object FullName -Descending | Select-Object -First 1 -ExpandProperty FullName)
) | Where-Object {$_ -and (Test-Path $_)}
if(-not $blenderPaths){Install-Package 'BlenderFoundation.Blender' $BlenderVersion}
else{Write-Host "Blender is already installed; keeping it: $($blenderPaths[0])"}
if(-not (Get-Command inkscape.exe -ErrorAction SilentlyContinue)) {
  Install-Package 'Inkscape.Inkscape'
}
if($WithShotcut){Install-Package 'Meltytech.Shotcut'}
if($WithAudacity){Install-Package 'Audacity.Audacity'}
# Update process PATH after WinGet; restart shell if newly installed executables remain unavailable.
$env:Path=[Environment]::GetEnvironmentVariable('Path','Machine')+';'+[Environment]::GetEnvironmentVariable('Path','User')
$py=Get-Command py.exe -ErrorAction SilentlyContinue
if(-not $py){throw "Python launcher missing after WinGet. Open a new PowerShell window and run this script again."}
& py -3.11 -m venv (Join-Path $root '.venv')
if($LASTEXITCODE -ne 0){throw 'Python venv creation failed'}
$venv=Join-Path $root '.venv\Scripts\python.exe'
& $venv -m pip install --upgrade pip
if($LASTEXITCODE -ne 0){throw 'pip upgrade failed'}
& $venv -m pip install -r (Join-Path $root 'windows\requirements-studio.txt')
if($LASTEXITCODE -ne 0){throw 'Python dependencies did not install'}
if(-not $SkipRemotion) {
  if(-not (Get-Command npm.cmd -ErrorAction SilentlyContinue)) {
    Write-Warning 'Node/npm not on PATH yet. Reopen PowerShell and rerun installation.'
  } else {
    Write-Host "Installing project-local Remotion dependencies. Check free-license eligibility before commercial production."
    & npm.cmd install --prefix (Join-Path $root 'motion') --no-audit --no-fund
    if($LASTEXITCODE -ne 0){throw 'Remotion project install failed'}
  }
}
& (Join-Path $PSScriptRoot 'Verify-Studio.ps1')
if($LASTEXITCODE -ne 0) {
  Write-Warning 'Some tools might require opening a new terminal for updated PATH. Run windows\Verify-Studio.ps1.'
}
Write-Host 'No Gemini API key was used. Set GitHub secrets on the server, never in this installer.' -ForegroundColor Green
