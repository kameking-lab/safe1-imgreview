# run_until_done.ps1 - $200プラン制限で止まっても自動復帰してBACKLOGを完走
$ErrorActionPreference = "Continue"
try { chcp 65001 > $null } catch {}
$OutputEncoding = [Console]::OutputEncoding = [Console]::InputEncoding = [System.Text.Encoding]::UTF8
$Model = "claude-opus-4-8"   # Fableが使えるなら "claude-fable-5"
$Worker = "Read RULES.md and BACKLOG.md in this folder. Do ONLY the single topmost unchecked '- [ ]' task in BACKLOG.md, strictly following RULES.md (never delete or overwrite, never use rm/Remove-Item/del/move, additions use new filenames, never kill Chrome, never print credentials; before starting, check existing outputs under refs/ and v14/ and only produce what is missing). When the task is complete, change its line to '- [x]' and run git add/commit/push to origin master. If no unchecked task remains, create an empty file named DONE.flag and stop. If you hit a usage or rate limit, save and push any work in progress, then stop."
New-Item -ItemType Directory -Force -Path ".\runner_logs" | Out-Null
$cycle = 0
while (-not (Test-Path ".\DONE.flag")) {
    $cycle++; $ts = Get-Date -Format "yyyyMMdd_HHmmss"; $log = ".\runner_logs\c_$ts.log"
    Write-Host "[$ts] cycle $cycle start (model=$Model)"
    & claude -p --model $Model --dangerously-skip-permissions $Worker *>&1 | Tee-Object -FilePath $log
    if (Test-Path ".\DONE.flag") { Write-Host "All tasks done. Exiting."; break }
    $out = Get-Content $log -Raw -ErrorAction SilentlyContinue
    if ($out -match "(?i)usage limit|rate.?limit|limit reached|reached your .*limit|try again|resets? (at|in)|too many requests|\b429\b|5-hour|weekly limit") {
        $sleepMin = 30
        if ($out -match "(?i)reset[s]? at (\d{1,2}):(\d{2})\s*(AM|PM)?") {
            try {
                $h=[int]$Matches[1]; $m=[int]$Matches[2]; $ap=$Matches[3]
                if ($ap){ if($ap.ToUpper() -eq 'PM' -and $h -lt 12){$h+=12}; if($ap.ToUpper() -eq 'AM' -and $h -eq 12){$h=0} }
                $r=(Get-Date).Date.AddHours($h).AddMinutes($m); if($r -le (Get-Date)){$r=$r.AddDays(1)}
                $sleepMin=[int][math]::Ceiling(($r-(Get-Date)).TotalMinutes)+3; if($sleepMin -gt 360){$sleepMin=360}
            } catch { $sleepMin = 30 }
        }
        Write-Host ("[{0}] limit detected. waiting {1} min then auto-retry." -f (Get-Date -Format HH:mm), $sleepMin)
        Start-Sleep -Seconds ($sleepMin*60)
    } else { Start-Sleep -Seconds 8 }
}
Write-Host "RUNNER finished."
