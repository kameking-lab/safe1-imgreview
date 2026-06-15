param(
  [Parameter(Mandatory=$true)][string]$Pptx,
  [Parameter(Mandatory=$true)][string]$OutPdf
)
$ErrorActionPreference = "Stop"
$Pptx = (Resolve-Path $Pptx).Path
$pp = New-Object -ComObject PowerPoint.Application
try {
  $pres = $pp.Presentations.Open($Pptx, $true, $false, $false)  # ReadOnly, Untitled, WithWindow=false
  # 32 = ppSaveAsPDF
  $pres.SaveAs($OutPdf, 32)
  $pres.Close()
  Write-Output ("EXPORTED PDF -> {0}" -f $OutPdf)
} finally {
  $pp.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($pp) | Out-Null
}
