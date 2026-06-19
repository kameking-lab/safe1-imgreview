$ErrorActionPreference = "Continue"
try { chcp 65001 > $null } catch {}
$OutputEncoding = [Console]::OutputEncoding = [Console]::InputEncoding = [System.Text.Encoding]::UTF8
Set-Location -Path $PSScriptRoot
$Model = "claude-opus-4-8"
$Worker = "Read RULES_LAYER.md and BACKLOG_LAYER.md in this folder. Do ONLY the single topmost unchecked '- [ ]' task, strictly following RULES_LAYER.md. KEY RULES: never delete or overwrite any existing file (additions use NEW filenames); never use rm/Remove-Item/del/move/taskkill; never kill Chrome; read OPENAI_API_KEY/GEMINI_API_KEY from .env and NEVER print key values. Generate assets with 'node gen_img.mjs <openai|google> <out.png> \"<prompt>\" [transparent]' (OpenAI=gpt-image-2 can do native transparent; Google=Nano Banana Pro). Make backgrounds opaque (no people), object/worker parts on pure white background then cut to transparent via 'py cutout_white.py <in> <out>' (rembg is absent). Self-check thumbnails for white fringe/holes, regenerate a clearly bad one at most once. Build sample_layers_v18.pptx with python-pptx placing each part as a SEPARATE movable/rotatable picture object over a full-bleed background (do NOT flatten); make OpenAI-asset and Google-asset versions of each composite; add the 'layer draft, adjust in PowerPoint' note. Convert to PDF via PowerPoint COM. For DEPLOY, union ALL past review tokens so every existing URL stays 200 (root=404). When the task is complete, change its line to '- [x]' and git add/commit/push origin main (commit master, push, then fast-forward master:main; if rejected pull --rebase then push). If no unchecked task remains, create empty DONE_LAYER.flag and stop. If you hit a usage or rate limit, save and push work in progress, then stop."
New-Item -ItemType Directory -Force -Path ".\runner_logs" | Out-Null
$cycle = 0
while (-not (Test-Path ".\DONE_LAYER.flag")) {
    $cycle++; $ts = Get-Date -Format "yyyyMMdd_HHmmss"; $log = ".\runner_logs\layer_$ts.log"
    Write-Host "[$ts] cycle $cycle start"
    & claude -p --model $Model --dangerously-skip-permissions $Worker *>&1 | Tee-Object -FilePath $log
    if (Test-Path ".\DONE_LAYER.flag") { Write-Host "All done."; break }
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
