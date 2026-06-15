$ErrorActionPreference = "Continue"
try { chcp 65001 > $null } catch {}
$OutputEncoding = [Console]::OutputEncoding = [Console]::InputEncoding = [System.Text.Encoding]::UTF8
Set-Location -Path $PSScriptRoot
$Model = "claude-opus-4-8"
$Worker = "Read RULES_PPT.md and BACKLOG_PPT.md in this folder. Do ONLY the single topmost unchecked '- [ ]' task, strictly following RULES_PPT.md. KEY RULES: never delete or overwrite any existing file (additions use NEW filenames; never overwrite the template or any existing pptx); never use rm/Remove-Item/del/move/taskkill; never kill Chrome; do NOT use API keys or print any credential values. SOURCE AUTHENTICITY IS CRITICAL: any MHLW url you attach MUST be fetched (web_fetch or curl) and confirmed HTTP 200 AND its body must match that accident mechanism before you use it; do NOT invent or guess urls/dates/sources; TGL cases must be genuine tail-gate-lifter accidents only (no refuse-truck / truck-crane / forklift / tank-truck / plain bed-or-dump fall); aerial cases must have agent=aerial work platform; if no matching public case exists, write 'public case none (verify)' and mark the narrative as 'AI-organized (no public source)' rather than fabricating. The 博展 template is the established format (reference hakuten_jirei_photo_v10.pptx + build_pptx.py + images/ref/footer_strip_raw.png + memory spec) — do NOT stop with 'template not found'; reproduce that format into a NEW file hakuten_jirei_cases.pptx. For QA, convert pptx via PowerPoint COM (render_pptx.ps1 style) since LibreOffice is absent, render to PNG/PDF and visually inspect. Each case: 2 slides (top=the 4 photos A/B/C/D in a labeled 2x2, bottom=item table), supervisor line '金田義太（労働安全コンサルタント 登録第4840号）'. When the task is complete, change its line to '- [x]' and git add/commit/push to origin main (commit to master, push, then fast-forward master:main; if rejected git pull --rebase then push). If no unchecked task remains, create an empty file named DONE_PPT.flag and stop. If you hit a usage or rate limit, save and push work in progress, then stop."
New-Item -ItemType Directory -Force -Path ".\runner_logs" | Out-Null
$cycle = 0
while (-not (Test-Path ".\DONE_PPT.flag")) {
    $cycle++; $ts = Get-Date -Format "yyyyMMdd_HHmmss"; $log = ".\runner_logs\ppt_$ts.log"
    Write-Host "[$ts] cycle $cycle start"
    & claude -p --model $Model --dangerously-skip-permissions $Worker *>&1 | Tee-Object -FilePath $log
    if (Test-Path ".\DONE_PPT.flag") { Write-Host "All done."; break }
    $out = Get-Content $log -Raw -ErrorAction SilentlyContinue
    if ($out -match "(?i)usage limit|rate.?limit|limit reached|reached your .*limit|try again|resets? (at|in)|too many requests|\b429\b|5-hour|weekly limit") {
        $sleepMin = 30
        if ($out -match "(?i)reset[s]? at (\d{1,2}):(\d{2})\s*(AM|PM)?") {
            try { $h=[int]$Matches[1]; $m=[int]$Matches[2]; $ap=$Matches[3]
                if ($ap){ if($ap.ToUpper() -eq 'PM' -and $h -lt 12){$h+=12}; if($ap.ToUpper() -eq 'AM' -and $h -eq 12){$h=0} }
                $r=(Get-Date).Date.AddHours($h).AddMinutes($m); if($r -le (Get-Date)){$r=$r.AddDays(1)}
                $sleepMin=[int][math]::Ceiling(($r-(Get-Date)).TotalMinutes)+3; if($sleepMin -gt 360){$sleepMin=360}
            } catch { $sleepMin = 30 } }
        Write-Host ("[{0}] limit detected. waiting {1} min." -f (Get-Date -Format HH:mm), $sleepMin)
        Start-Sleep -Seconds ($sleepMin*60)
    } else { Start-Sleep -Seconds 8 }
}
Write-Host "RUNNER finished."
