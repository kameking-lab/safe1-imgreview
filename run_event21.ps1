$ErrorActionPreference = "Continue"
try { chcp 65001 > $null } catch {}
$OutputEncoding = [Console]::OutputEncoding = [Console]::InputEncoding = [System.Text.Encoding]::UTF8
Set-Location -Path $PSScriptRoot
$Model = "claude-opus-4-8"

New-Item -ItemType Directory -Force -Path ".\runner_logs" | Out-Null
$bootTs = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path ".\runner_logs\event21_boot.txt" -Value "BOOT $bootTs PID=$PID" -Encoding UTF8

$Worker = @'
Read RULES_EVENT21.md and BACKLOG_EVENT21.md in this folder. Do ONLY the single topmost unchecked - [ ] task, strictly following RULES_EVENT21.md: never delete or overwrite (additions use new filenames); never use rm/Remove-Item/del/move/taskkill; never kill Chrome; do NOT use OpenAI (Google gemini-3-pro-image-preview only); read the API key from .env and never print its value (mask to last 4 chars if needed); before starting check existing files under gen_event_v21/ and only generate what is missing so re-runs never duplicate or break prior output. The single most important requirement: each illustration must show the CAUSE of the accident (the unsafe act or unsafe condition) inside the frame together with the moment of the fall/tip-over, so a viewer can tell what went wrong. Do not draw a person merely falling with no visible cause. For each base number, look up its filename and accident type in collect_aerial2/aerial2_index.csv, keep that accident type, set ONE plausible cause scenario for it, and draw an exhibition-booth setup scene where that cause is visible. Generate 2 images per base with Google gemini-3-pro-image-preview (generateContent inlineData, passing the base image as reference), in the unified style and rules from RULES_EVENT21.md (scissor-lift only, exhibition-booth setup, accident moment PLUS visible cause, no text/arrows/captions, no blood, no real logos, proper PPE). Model the new generation script on the existing gen_event_v20.mjs but use a new filename like gen_event_v21.mjs and the Google path only. Self-check each image; if the cause is not visible (just a falling person), regenerate once with a stronger cause instruction (max 2 tries each). Record the cause scenario per number in gen_event_v21/event_index_v21.csv. When the task is complete, change its line to - [x] and git add/commit/push to origin master; if push is rejected, git pull --rebase then push again. If no unchecked task remains, create an empty file named DONE_EVENT21.flag and stop. If you hit a usage or rate limit, save and push work in progress, then stop.
'@

$ok = $false
try { [void][System.Management.Automation.Language.Parser]::ParseInput($Worker, [ref]$null, [ref]$null); $ok = $true } catch {}
Write-Host ("WORKER PARSE_OK={0}" -f $ok)

$cycle = 0
while (-not (Test-Path ".\DONE_EVENT21.flag")) {
    $cycle++; $ts = Get-Date -Format "yyyyMMdd_HHmmss"; $log = ".\runner_logs\event21_$ts.log"
    Write-Host "[$ts] cycle $cycle start"
    & claude -p --model $Model --dangerously-skip-permissions $Worker *>&1 | Tee-Object -FilePath $log
    if (Test-Path ".\DONE_EVENT21.flag") { Write-Host "All done."; break }
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
