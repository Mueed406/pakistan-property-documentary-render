#Requires -Version 5.1
<#
AI motion skill installer for Windows/Claude Code/Codex.
Does not install anything unless -Install is passed.
Skills are installed from their upstream repositories (not vendored/republished here).
No paid API, no billing.
#>
[CmdletBinding()]
param(
 [switch]$Install,
 [switch]$IncludeCommunityMotion,
 [switch]$Advanced,
 [switch]$Global
)
$ErrorActionPreference='Stop'
$root=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
Write-Host 'Required tools: Node >=18, ffmpeg, Chrome/Edge. Optional: Blender for 3D.' -ForegroundColor Cyan
foreach($exe in @('node.exe','npx.cmd','ffmpeg.exe')){
 if(-not (Get-Command $exe -ErrorAction SilentlyContinue)){
   throw "Missing $exe. Install the Windows Studio prerequisites first."
 }
}
$version=(& node.exe -p "process.versions.node.split('.')[0]")
if([int]$version -lt 18){throw 'Node 18+ required'}
$edge1='C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$chrome1='C:\Program Files\Google\Chrome\Application\chrome.exe'
if(-not (Test-Path $edge1) -and -not (Test-Path $chrome1) -and -not $env:CHROME_PATH) {
 Write-Warning 'No Chrome/Edge detected at a standard location; set CHROME_PATH to a browser binary.'
}
if(-not $Install) {
 Write-Host 'Audit only: run with -Install to actually install external skills.'
 Write-Host 'MIT: JakeB-5/motion-graphic-skill'
 Write-Host 'MIT: haidrrrry/claude-remotion-skill'
 Write-Host 'Advanced pack: motion art direction, shot composition, beat-sync, premium color-motion, graph/chart-animation, animated-infographic, map-animation, cinematic-camera, HyperFrames'
 Write-Host 'Optional unlicensed upstream: abhimahamkali/claude-motion-skill (install separately at your own discretion)'
 exit 0
}
$scope=@()
if($Global){$scope+=@('-g')}
function AddSkill([string]$source,[string]$skill,[string[]]$agents) {
 $args=@('-y','skills','add',$source,'--skill',$skill)
 foreach($a in $agents){$args+=@('-a',$a)}
 $args+=$scope;$args+=@('-y')
 Write-Host "Installing authorized external skill: $source / $skill" -ForegroundColor Cyan
 & npx.cmd @args
 if($LASTEXITCODE -ne 0){throw "Skill install failed for $source ($LASTEXITCODE). Check upstream CLI."}
}
AddSkill 'JakeB-5/motion-graphic-skill' 'motion-graphic' @('claude-code','codex')
AddSkill 'haidrrrry/claude-remotion-skill' 'remotion-motion-graphics' @('claude-code','codex')
if($Advanced) {
  AddSkill 'iart-ai/motion-design-skills' 'motion-art-direction' @('claude-code','codex')
  AddSkill 'iart-ai/motion-design-skills' 'shot-composition' @('claude-code','codex')
  AddSkill 'iart-ai/motion-design-skills' 'beat-sync-editing' @('claude-code','codex')
  AddSkill 'heygen-com/hyperframes' 'hyperframes-animation' @('claude-code','codex')
  AddSkill 'heygen-com/hyperframes' 'hyperframes-cli' @('claude-code','codex')
  AddSkill 'heygen-com/hyperframes' 'faceless-explainer' @('claude-code','codex')
  AddSkill 'iart-ai/motion-design-skills' 'color-motion' @('claude-code','codex')
  AddSkill 'iart-ai/motion-design-skills' 'animation-principles' @('claude-code','codex')
  AddSkill 'iart-ai/data-animation-skills' 'chart-animation' @('claude-code','codex')
  AddSkill 'iart-ai/data-animation-skills' 'animated-infographic' @('claude-code','codex')
  AddSkill 'iart-ai/map-animation-skills' 'map-animation' @('claude-code','codex')
  AddSkill 'Liamrjohnston/remotion-motion-graphics-skill' 'cinematic-camera' @('claude-code','codex')
}
if($IncludeCommunityMotion) {
 Write-Warning 'The /motion repository did not contain a visible explicit LICENSE file when reviewed. Do NOT redistribute as our own skill; installing upstream only.'
 AddSkill 'abhimahamkali/claude-motion-skill' 'motion' @('claude-code')
}
Write-Host 'External skills installed into selected agent(s). Restart your agent session to load them.' -ForegroundColor Green
Write-Host 'This does NOT install a ChatGPT plugin or grant tool execution inside ChatGPT.' -ForegroundColor Yellow
