param(
  [Parameter(Mandatory=$true)][string]$Pptx,
  [Parameter(Mandatory=$true)][string]$OutDir
)
$ErrorActionPreference = "Stop"
if (Test-Path $OutDir) { } else { New-Item -ItemType Directory -Force -Path $OutDir | Out-Null }
$Pptx = (Resolve-Path $Pptx).Path
$OutDir = (Resolve-Path $OutDir).Path
$pp = New-Object -ComObject PowerPoint.Application
try {
  $pres = $pp.Presentations.Open($Pptx, $true, $false, $false)  # ReadOnly, Untitled, WithWindow=false
  # 16:9 1280x720 で各スライドをPNG出力
  $i = 0
  foreach ($slide in $pres.Slides) {
    $i++
    $fn = Join-Path $OutDir ("slide{0:D2}.png" -f $i)
    $slide.Export($fn, "PNG", 1600, 900)
  }
  $pres.Close()
  Write-Output "EXPORTED $i slides to $OutDir"
} finally {
  $pp.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($pp) | Out-Null
}
