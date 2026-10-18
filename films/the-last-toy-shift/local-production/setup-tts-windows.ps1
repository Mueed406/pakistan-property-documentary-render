param(
  [string]$FilmPath = ".",
  [ValidateSet("kokoro","chatterbox","directml")][string]$Engine = "kokoro",
  [switch]$InstallNoizSkill
)
$ErrorActionPreference="Stop"
$film=(Resolve-Path $FilmPath).Path
$script=Join-Path $film "local-production\voice_gpu.py"
if (-not (Test-Path $script)) {throw "Choose film directory containing local-production\voice_gpu.py"}
if (-not (Get-Command py -ErrorAction SilentlyContinue)) {throw "Python 3.11 + Windows Python Launcher are required."}
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {throw "FFmpeg is required on PATH."}
$venv=Join-Path $film ".venv-tts"
$python=Join-Path $venv "Scripts\python.exe"
if (-not (Test-Path $python)) {
  & py -3.11 -m venv $venv
  if ($LASTEXITCODE -ne 0) {throw "Unable to create Python 3.11 venv"}
}
& $python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {throw "Unable to upgrade pip"}
& $python -m pip install "numpy>=1.26,<3" soundfile "kokoro>=0.9.4,<1.1" torch torchaudio
if ($LASTEXITCODE -ne 0) {throw "Unable to install local Kokoro backend"}
if ($Engine -eq "directml") {
  & $python -m pip uninstall -y onnxruntime onnxruntime-gpu
  & $python -m pip install --upgrade kokoro-onnx onnxruntime-directml
  if ($LASTEXITCODE -ne 0) {throw "Unable to install ONNX Runtime DirectML provider"}
}
if ($Engine -eq "chatterbox") {
  & $python -m pip install chatterbox-tts
  if ($LASTEXITCODE -ne 0) {throw "Unable to install Chatterbox; use clean separate venv when dependencies conflict"}
}
if ($InstallNoizSkill) {
  & (Join-Path $film "local-production\install-noiz-skill.ps1") -ProjectPath $film
  if ($LASTEXITCODE -ne 0) {throw "Noiz skill install failed"}
}
Write-Host "Actual local device probe:"
& $python $script probe
if ($LASTEXITCODE -ne 0) {throw "PyTorch probe failed"}
Write-Host "For an NVIDIA GPU reporting CPU, install a compatible CUDA-enabled PyTorch wheel within $venv using the official instructions at https://pytorch.org/get-started/locally/ ."
Write-Host "A CPU-only wheel does NOT mean your GPU is being used."
Write-Host "Generate: & '$python' '$script' generate --backend kokoro --output '$film\output\local-voice'"

if ($Engine -eq "directml") {
  Write-Host "DirectML selected: run 'generate --backend kokoro-directml --require-gpu' after installation."
  Write-Host "Models will download from the fixed official Kokoro ONNX release with verified SHA256."
}
