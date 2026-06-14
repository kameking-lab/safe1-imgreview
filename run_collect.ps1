$ErrorActionPreference = "Continue"
try { chcp 65001 > $null } catch {}
$OutputEncoding = [Console]::OutputEncoding = [Console]::InputEncoding = [System.Text.Encoding]::UTF8
Set-Location -Path $PSScriptRoot
$Model = "claude-opus-4-8"
$Worker = "Read RULES_C.md and BACKLOG_C.md in this folder. Do ONLY the single topmost unchecked '- [ ]' task, strictly following RULES_C.md (never delete or overwrite; never use rm/Remove-Item/del/move/taskkill; additions use new filenames; never kill Chrome; never print credential or API key values; do NOT generate images in this phase, collection only; before starting check existing files under collect2/, data_xlsx/, data/jniosh/ and only add what is missing so re-runs never duplicate or break prior output). When the task is complete, change its line to '- [x]' and git add/commit/push to origin main (if push is rejected, git pull --rebase then push again). If no unchecked task remains, create an empty file named DONE_C.flag and stop. If you hit a usage or rate limit, save and push work in progress, then stop."
New-Item -ItemType Directory -Force -Path ".\runner_logs" | Out-Null
$cycle = 0
while (-not (Test-Path ".\DONE_C.flag")) {
    $cycle++; $ts = Get-Date -Format "yyyyMMdd_HHmmss"; $log = ".\runner_logs\col_$ts.log"
    Write-Host "[$ts] cycle $cycle start"
    & claude -p --model $Model --dangerously-skip-permissions $Worker *>&1 | Tee-Object -FilePath $log
    if (Test-Path ".\DONE_C.flag") { Write-Host "All done."; break }
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
