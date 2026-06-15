$ErrorActionPreference = "Continue"
try { chcp 65001 > $null } catch {}
$OutputEncoding = [Console]::OutputEncoding = [Console]::InputEncoding = [System.Text.Encoding]::UTF8
Set-Location -Path $PSScriptRoot
$Model = "claude-opus-4-8"
$Worker = "Read RULES_V2.md and BACKLOG_V2.md in this folder. Do ONLY the single topmost unchecked '- [ ]' task, strictly following RULES_V2.md. KEY RULES: never delete or overwrite any existing file (additions use NEW filenames; do NOT overwrite existing pptx/template/photos_v15); never use rm/Remove-Item/del/move/taskkill; never kill Chrome; read OPENAI_API_KEY/GEMINI_API_KEY from .env and NEVER print key values. For a G-NXX task, run 'node gen_v16.mjs NXX' to make base/openai/google (3 images), self-check and regenerate only a clearly broken one (max 2 tries each), then update img_index_v16.csv. The final pptx is a NEW file hakuten_jirei_v2.pptx following template_spec.md (do not overwrite hakuten_jirei_cases.pptx). Titles are creative event-setup accident titles; do NOT show AI model-name labels; AI/fiction note only once on the cover; sources are shown small as 'reference material'. Each slide has supervisor '金田義太（登録第4840号）'. Video prompts go in a SEPARATE file video_prompts_v16.(md/pdf): 15 cases x Sora2 + Veo3.1 x JP&EN, 3 phases (before/moment/after), image-to-video. For QA convert via PowerPoint COM and visually inspect; record QA_V2_r{n}.md; stop at zero issues or max 4 rounds. When the task is complete, change its line to '- [x]' and git add/commit/push origin main (commit master, push, then fast-forward master:main; if rejected pull --rebase then push). If no unchecked task remains, create empty DONE_V2.flag and stop. If you hit a usage or rate limit, save and push work in progress, then stop."
New-Item -ItemType Directory -Force -Path ".\runner_logs" | Out-Null
$cycle = 0
while (-not (Test-Path ".\DONE_V2.flag")) {
    $cycle++; $ts = Get-Date -Format "yyyyMMdd_HHmmss"; $log = ".\runner_logs\v2_$ts.log"
    Write-Host "[$ts] cycle $cycle start"
    & claude -p --model $Model --dangerously-skip-permissions $Worker *>&1 | Tee-Object -FilePath $log
    if (Test-Path ".\DONE_V2.flag") { Write-Host "All done."; break }
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
