$ErrorActionPreference = "Continue"
try { chcp 65001 > $null } catch {}
$OutputEncoding = [Console]::OutputEncoding = [Console]::InputEncoding = [System.Text.Encoding]::UTF8
Set-Location -Path $PSScriptRoot
$Model = "claude-opus-4-8"

New-Item -ItemType Directory -Force -Path ".\runner_logs" | Out-Null
$bootTs = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path ".\runner_logs\event22_boot.txt" -Value "BOOT $bootTs PID=$PID" -Encoding UTF8

$Worker = @'
Read RULES_EVENT22.md and BACKLOG_EVENT22.md in this folder. Do ONLY the single topmost unchecked - [ ] task, strictly following RULES_EVENT22.md: never delete or overwrite (additions use new filenames); never use rm/Remove-Item/del/move/taskkill; never kill Chrome; do NOT use OpenAI (Google gemini-3-pro-image-preview only); read the API key from .env and never print its value (mask to last 4 chars if needed); before starting check existing files under gen_event_v22/ and only generate what is missing so re-runs never duplicate or break prior output. The single most important requirement: each illustration is a KYT hazard-prediction diagram that shows, in ONE frame, (1) a worker in an unsafe posture or situation AND (2) curved red/orange ARROWS showing how the worker moves / the center of gravity shifts / the direction of the resulting fall, tip-over or crush. Do not draw a person already fully fallen; show the about-to-happen flow via arrows. For each base number, read its accident type and the cause scenario from gen_event_v21/event_index_v21.csv, and recompose it as an unsafe-posture-then-arrow-to-accident diagram in an exhibition-booth setup scene. Look up the base filename in collect_aerial2/aerial2_index.csv and pass that image as the reference. Generate 2 images per base with Google gemini-3-pro-image-preview (generateContent inlineData), unified style from RULES_EVENT22.md (scissor-lift only, exhibition-booth setup, unsafe posture plus prediction arrows, arrows allowed but NO other text/captions/speech-bubbles, no blood, no real logos, proper PPE). Model the new generation script on gen_event_v21.mjs but use a new filename like gen_event_v22.mjs and the Google path only. Self-check each image; if the prediction arrow is missing or unclear, regenerate once with a stronger arrow instruction (max 2 tries each). Record per number in gen_event_v22/event_index_v22.csv the unsafe-posture content and what the arrow indicates. When the task is complete, change its line to - [x] and git add/commit/push to origin master; if push is rejected, git pull --rebase then push again. If no unchecked task remains, create an empty file named DONE_EVENT22.flag and stop. If you hit a usage or rate limit, save and push work in progress, then stop.
'@

$ok = $false
try { [void][System.Management.Automation.Language.Parser]::ParseInput($Worker, [ref]$null, [ref]$null); $ok = $true } catch {}
Write-Host ("WORKER PARSE_OK={0}" -f $ok)

$cycle = 0
while (-not (Test-Path ".\DONE_EVENT22.flag")) {
    $cycle++; $ts = Get-Date -Format "yyyyMMdd_HHmmss"; $log = ".\runner_logs\event22_$ts.log"
    Write-Host "[$ts] cycle $cycle start"
    & claude -p --model $Model --dangerously-skip-permissions $Worker *>&1 | Tee-Object -FilePath $log
    if (Test-Path ".\DONE_EVENT22.flag") { Write-Host "All done."; break }
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
