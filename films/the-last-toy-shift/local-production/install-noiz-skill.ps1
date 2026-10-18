param([string]$ProjectPath=".")
$ErrorActionPreference="Stop"
$dest=(Resolve-Path $ProjectPath).Path
$sha="779f30af588ebf4dd17fc0acaa590ae147a0d3f5"
$temp=Join-Path $env:TEMP ("NoizAI-skills-"+[guid]::NewGuid().ToString("N"))
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {throw "Git for Windows required"}
try {
  & git init -q $temp
  & git -C $temp remote add origin https://github.com/NoizAI/skills.git
  & git -C $temp fetch --depth 1 --quiet origin $sha
  & git -C $temp checkout --quiet --detach FETCH_HEAD
  $actual=(& git -C $temp rev-parse HEAD).Trim()
  if ($actual -ne $sha) {throw "NoizAI SHA verification failed"}
  $src=Join-Path $temp "skills\tts"
  if (-not (Test-Path (Join-Path $src "SKILL.md"))) {throw "Missing upstream TTS skill"}
  foreach($hostDir in @(".agents\skills",".claude\skills",".agent\skills",".gemini\skills")) {
    $target=Join-Path $dest (Join-Path $hostDir "noiz-tts")
    if (Test-Path $target) {Write-Host "SKIP preexisting $target"; continue}
    New-Item -Force -ItemType Directory -Path (Split-Path -Parent $target)|Out-Null
    Copy-Item $src $target -Recurse
    $doc=Join-Path $target "SKILL.md"
    $t=(Get-Content -Raw $doc) -replace '(?m)^name:\s*tts\s*$',"name: noiz-tts"
    Set-Content $doc -Value $t -Encoding utf8
    Write-Host "INSTALLED private upstream NoizAI/skills TTS $target"
  }
} finally {
  if (Test-Path $temp) {Remove-Item $temp -Force -Recurse}
}
Write-Host "Use an explicit local Kokoro backend; Noiz default can use cloud guest service. No cloud API key included."
