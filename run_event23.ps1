$ErrorActionPreference = "Continue"
try { chcp 65001 > $null } catch {}
$OutputEncoding = [Console]::OutputEncoding = [Console]::InputEncoding = [System.Text.Encoding]::UTF8
Set-Location -Path $PSScriptRoot
$Model = "claude-opus-4-8"

New-Item -ItemType Directory -Force -Path ".\runner_logs" | Out-Null
$bootTs = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path ".\runner_logs\event23_boot.txt" -Value "BOOT $bootTs PID=$PID" -Encoding UTF8

$Worker = @'
Read RULES_EVENT23.md and BACKLOG_EVENT23.md in this folder. Do ONLY the single topmost unchecked - [ ] task, strictly following RULES_EVENT23.md: never delete or overwrite (additions use new filenames); never use rm/Remove-Item/del/move/taskkill; never kill Chrome; do NOT use OpenAI (Google gemini-3-pro-image-preview only); read the API key from .env and never print its value (mask to last 4 chars if needed); before starting check existing files under gen_event_v23/ and only generate what is missing so re-runs never duplicate or break prior output. The single most important requirement: do NOT use a generic shared template. For the base number of this task, look up its filename in collect_aerial2/aerial2_index.csv and actually READ the source image collect_aerial2/img/(file) with the Read tool, analyze it carefully (machine type, worker posture/action/count, accident situation, and WHY it happens = the cause), then write a bespoke generation prompt for THAT specific image (Japanese plus English) that faithfully preserves its cause, posture, situation and physics, shows the exact moment the accident begins, relocates the scene to a Japanese exhibition-hall booth-setup indoor environment (steel/H-beams to exhibition truss, curbs/steps to cable protectors, outdoor to indoor), makes the aerial platform a scissor lift, unified high-quality safety-education illustration style, and contains NO arrows, NO text/captions/speech-bubbles, no blood, no real logos. Save the bespoke prompt full text to prompts_v23/(number).txt. Then generate 2 images with Google gemini-3-pro-image-preview (generateContent inlineData, passing the source image as reference) USING that bespoke prompt read from prompts_v23/(number).txt (do not bake a generic string into the script). Model the generation script on gen_event_v22.mjs but use a new filename like gen_event_v23.mjs, Google path only, reading the prompt from the txt file. Self-check each image for fidelity to the source cause/posture/situation, the accident moment, physical correctness, indoor-exhibition/scissor-lift/truss/cable-protector substitution, and no-arrow/no-text; if 1 to 3 are weak, adjust the bespoke prompt and regenerate once (max 2 tries each). Record per number in gen_event_v23/event_index_v23.csv the cause/posture/situation read from the source and a summary of the bespoke prompt. When the task is complete, change its line to - [x] and git add/commit/push to origin master; if push is rejected, git pull --rebase then push again. If no unchecked task remains, create an empty file named DONE_EVENT23.flag and stop. If you hit a usage or rate limit, save and push work in progress, then stop.
'@

$ok = $false
try { [void][System.Management.Automation.Language.Parser]::ParseInput($Worker, [ref]$null, [ref]$null); $ok = $true } catch {}
Write-Host ("WORKER PARSE_OK={0}" -f $ok)

$cycle = 0
while (-not (Test-Path ".\DONE_EVENT23.flag")) {
    $cycle++; $ts = Get-Date -Format "yyyyMMdd_HHmmss"; $log = ".\runner_logs\event23_$ts.log"
    Write-Host "[$ts] cycle $cycle start"
    & claude -p --model $Model --dangerously-skip-permissions $Worker *>&1 | Tee-Object -FilePath $log
    if (Test-Path ".\DONE_EVENT23.flag") { Write-Host "All done."; break }
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
