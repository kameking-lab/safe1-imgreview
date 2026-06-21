$ErrorActionPreference = "Continue"
try { chcp 65001 > $null } catch {}
$OutputEncoding = [Console]::OutputEncoding = [Console]::InputEncoding = [System.Text.Encoding]::UTF8
Set-Location -Path $PSScriptRoot
New-Item -ItemType Directory -Force -Path ".\runner_logs" | Out-Null
("BOOT " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss") + " pid=" + $PID + " dir=" + $PSScriptRoot) | Out-File -FilePath ".\runner_logs\prop_boot.txt" -Append -Encoding utf8
$Model = "claude-opus-4-8"
$Worker = @'
Read RULES_PROP.md and BACKLOG_PROP.md in this folder. Do ONLY the single topmost unchecked task line, strictly following RULES_PROP.md. KEY RULES: never delete or overwrite any existing file (additions use NEW filenames; existing files may be REUSED but not destroyed); never use rm/Remove-Item/del/move/taskkill; never kill Chrome; never stop a running runner. DO NOT generate any new images this time (use only existing local data, existing generated images, and existing figures). Do NOT call image-generation APIs. Read GEMINI_API_KEY/keys only from .env if ever needed and NEVER print key values. NEVER fabricate numbers, laws, dates or sources: use ONLY the confirmed data in RULES_PROP.md; if a value cannot be confirmed, omit it. GOAL: build proposal_hakuten.pptx for tomorrow business meeting, visual-first per Mehrabian (visuals 70 percent, minimal text: max 3 lines per slide, big numbers + short captions + figures + icons, safety colors red danger / yellow caution / green countermeasure, Japanese font to avoid mojibake, 16:9). Use existing figs/ (fig_tgl_type_rank, fig_aerial_type_rank, fig_death_vs_injury, fig_tgl_timeline, fig_qual_table, fig_danger_points); create any missing concept figures with matplotlib using a Japanese font under NEW names figs/prop_*.png (no fabricated numbers). For the mandated accident-case format slide use template_spec.md layout with photos_v16 images and cases_v2 body text, small source note, supervisor credit (金田 義太, 労働安全コンサルタント 登録第4840号), and a small "AI再現イメージ" note. Build with python-pptx (py 3.12), convert to proposal_hakuten.pdf via PowerPoint COM. For QA rounds actually render PDF to PNG into qa_prop/ and visually inspect (do not self-grade only); cut text, fix overflow/distortion. For DEPLOY put pptx+PDF+index.html into review_prop/<random 32 chars>/, redeploy Vercel hakuten-review with vercel deploy --prod using the existing review_layer_v19/.vercel project, union ALL past review tokens (every existing review_*/<32-char> token directory plus the new one) so every existing URL stays 200 and root is 404, verify HTTP 200 and root 404 with curl, then git push the artifacts. When the task is complete, change its line to checked and git add/commit/push origin main (commit master, push, then fast-forward master:main; if rejected pull --rebase then push). If no unchecked task remains, create an empty file named DONE_PROP.flag and stop. If you hit a usage or rate limit, save and push work in progress, then stop.
'@
if (-not [System.Management.Automation.Language.Parser]::ParseInput($Worker, [ref]$null, [ref]$null)) {} else { ("PARSE_OK " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss")) | Out-File -FilePath ".\runner_logs\prop_boot.txt" -Append -Encoding utf8 }
$cycle = 0
while (-not (Test-Path ".\DONE_PROP.flag")) {
    $cycle++; $ts = Get-Date -Format "yyyyMMdd_HHmmss"; $log = ".\runner_logs\prop_$ts.log"
    Write-Host "[$ts] cycle $cycle start"
    & claude -p --model $Model --dangerously-skip-permissions $Worker *>&1 | Tee-Object -FilePath $log
    if (Test-Path ".\DONE_PROP.flag") { Write-Host "All done."; break }
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
("DONE " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss")) | Out-File -FilePath ".\runner_logs\prop_boot.txt" -Append -Encoding utf8
Write-Host "RUNNER finished."
