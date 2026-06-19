$ErrorActionPreference = "Continue"
try { chcp 65001 > $null } catch {}
$OutputEncoding = [Console]::OutputEncoding = [Console]::InputEncoding = [System.Text.Encoding]::UTF8
Set-Location -Path $PSScriptRoot
New-Item -ItemType Directory -Force -Path ".\runner_logs" | Out-Null
("BOOT " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss") + " pid=" + $PID + " dir=" + $PSScriptRoot) | Out-File -FilePath ".\runner_logs\layv19_boot.txt" -Append -Encoding utf8
$Model = "claude-opus-4-8"
$Worker = @'
Read RULES_LAYV19.md and BACKLOG_LAYV19.md in this folder. Do ONLY the single topmost unchecked task line, strictly following RULES_LAYV19.md. KEY RULES: never delete or overwrite any existing file (additions use NEW filenames; existing files may be REUSED but not destroyed); never use rm/Remove-Item/del/move/taskkill; never kill Chrome; do NOT use OpenAI (Google only = gemini-3-pro-image-preview); read GEMINI_API_KEY from .env and NEVER print key values. CORE METHOD: fix ONE camera viewpoint per situation and generate the background AND all parts with the SAME viewpoint/eye-height/perspective/lighting (use the shared viewpoint phrase from RULES at the end of every prompt) so angles already match at generation time. Generate with: node gen_img.mjs google OUTPATH.png "PROMPT" . Make parts on a pure white background then cut to transparent (rembg if available, else py cutout_white.py IN OUT). Self-check thumbnails for white fringe or holes, regenerate a clearly bad one at most once. Build sample_layers_v19.pptx with python-pptx: a catalog slide (label each part with its viewpoint A or B) and ONE composite slide (TGL is fine) overlaying the same-viewpoint collapsing rollcage and pinned worker with minimal or no rotation, each part a SEPARATE movable picture object (do NOT flatten); add a note that this verifies the fixed-viewpoint method; convert to PDF via PowerPoint COM. For DEPLOY, union ALL past review tokens so every existing URL stays 200 and root is 404. When the task is complete, change its line to checked and git add/commit/push origin main (commit master, push, then fast-forward master:main; if rejected pull --rebase then push). If no unchecked task remains, create an empty file named DONE_LAYV19.flag and stop. If you hit a usage or rate limit, save and push work in progress, then stop.
'@
$cycle = 0
while (-not (Test-Path ".\DONE_LAYV19.flag")) {
    $cycle++; $ts = Get-Date -Format "yyyyMMdd_HHmmss"; $log = ".\runner_logs\layv19_$ts.log"
    Write-Host "[$ts] cycle $cycle start"
    & claude -p --model $Model --dangerously-skip-permissions $Worker *>&1 | Tee-Object -FilePath $log
    if (Test-Path ".\DONE_LAYV19.flag") { Write-Host "All done."; break }
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
("DONE " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss")) | Out-File -FilePath ".\runner_logs\layv19_boot.txt" -Append -Encoding utf8
Write-Host "RUNNER finished."
