#Requires -Version 5.1
[CmdletBinding()]
param([switch]$RequireAll)
$ErrorActionPreference='Stop'
$root=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$items=[ordered]@{}
function Check([string]$Label,[string]$Command,[string[]]$Args){
 try {
  $c=Get-Command $Command -ErrorAction Stop
  $message=(& $c.Source @Args 2>&1 | Select-Object -First 2 | Out-String).Trim()
  $items[$Label]=@{ok=$true;path=$c.Source;version=$message}
 } catch {
  $items[$Label]=@{ok=$false;reason=$_.Exception.Message}
 }
}
Check 'ffmpeg' 'ffmpeg.exe' @('-version')
Check 'ffprobe' 'ffprobe.exe' @('-version')
Check 'node' 'node.exe' @('--version')
Check 'npm' 'npm.cmd' @('--version')
Check 'python launcher' 'py.exe' @('--version')
Check 'git' 'git.exe' @('--version')
Check 'Inkscape CLI' 'inkscape.exe' @('--version')
$blender=@(
 (Get-Command blender.exe -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Source -ErrorAction SilentlyContinue),
 (Get-ChildItem "$env:ProgramFiles\Blender Foundation\Blender *\blender.exe" -ErrorAction SilentlyContinue | Sort-Object FullName -Descending | Select-Object -First 1 -ExpandProperty FullName)
)|Where-Object {$_ -and (Test-Path $_)}
if($blender){
 $b=(& $blender[0] --version 2>&1 | Select-Object -First 2 | Out-String).Trim()
 $items['Blender background CLI']=@{ok=$true;path=$blender[0];version=$b}
}else{$items['Blender background CLI']=@{ok=$false;reason='Not found on PATH or standard Blender installation folder'}}
$python=Join-Path $root '.venv\Scripts\python.exe'
if(Test-Path $python){
 $code="import pedalboard, opentimelineio, numpy; print('Pedalboard, OTIO and NumPy import OK')"
 & $python -c $code 2>&1 | Out-Host
 $items['Audio+timeline Python environment']=@{ok=($LASTEXITCODE -eq 0);path=$python}
}else {$items['Audio+timeline Python environment']=@{ok=$false;reason='Create with windows/Install-Studio.ps1 -Install'}}
$rem=Join-Path $root 'motion\node_modules\remotion\package.json'
$items['Remotion project']=@{ok=(Test-Path $rem);path=$rem}
$report=Join-Path $root 'windows\STUDIO_DIAGNOSTICS.json'
$items | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 $report
Write-Host "Verification saved to: $report"
$items.GetEnumerator() | ForEach-Object{
 Write-Host "$(if($_.Value.ok){'[OK]'}else{'[MISSING]'}) $($_.Key)"
}
if($RequireAll -and @($items.Values|Where-Object {-not $_.ok}).Count -gt 0){exit 2}
exit 0
