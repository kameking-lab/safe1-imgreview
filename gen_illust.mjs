/**
 * gen_illust.mjs
 * instagram-automation の Gemini ブラウザ方式を流用し、技術安全イラストを生成する。
 * - APIキーは使わない。.cache/browser-profile-gemini のログイン済みセッションを再利用。
 * - chrome は kill しない（Playwright が別プロファイルの自前 chromium を起動）。
 * - 文字は焼き込まない（ラベル/矢印/三角は pptx 側で重ねる）。
 * 出力: safe1/images/gen/genNN.png + manifest.json
 */
import path from "node:path";
import fs from "node:fs";

const LIB = "C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const {
  launchBrowser, saveScreenshot, dismissOverlays, ensureGeminiLoggedIn,
} = await import(`file:///${LIB}/browser-helpers.mjs`);
const {
  startNewChat, selectImageCreationTool, isImageToolActive, submitPrompt,
} = await import(`file:///${LIB}/gemini-helpers.mjs`);

const OUT_DIR = "C:/Users/kanet/20260522/safe1/images/gen";
fs.mkdirSync(OUT_DIR, { recursive: true });

const STYLE =
  "Black and white technical line drawing, clean thin vector outlines on a pure white background, " +
  "industrial occupational-safety manual illustration style, simple schematic, side view. " +
  "The human worker is drawn as a solid black silhouette. " +
  "Absolutely NO text, no letters, no numbers, no labels, no watermark, no logo, no caption. " +
  "Minimal, generous white space, single scene centered, consistent simple style.";

const SCENES = [
  // 1 TGL 端部・後退時の墜落
  "The rear of a flatbed delivery truck. A tail-lift platform (tailgate lifter) is lowered horizontally at the back. " +
  "A worker silhouette is stepping backward and losing his balance off the rear outer edge of the platform, beginning to fall to the ground. A heavy cylindrical steel drum stands on the platform near him.",
  // 2 TGL 昇降中のはさまれ
  "The rear of a truck with a tail-lift platform raised to about half height, partway between the ground and the truck bed. " +
  "A worker silhouette stands at the side and his foot is caught and pinched in the narrow gap between the rising platform and the edge of the truck bed.",
  // 3 カゴ車が昇降板上で転倒・下敷き
  "A tail-lift platform at the rear of a truck, slightly inclined. A tall wheeled roll-cage cart (a metal mesh cage on casters, a roll box pallet) is tipping over and toppling off the platform. " +
  "A worker silhouette beside the platform is being knocked down by the falling cage.",
  // 4 バケット身を乗り出し・墜落
  "A self-propelled boom-type aerial work platform (cherry picker / boom lift) with its basket bucket raised high in the air on a long articulated arm. " +
  "A worker silhouette inside the basket is leaning far out over the guardrail and falling head-first toward the ground, with a safety-harness lanyard dangling loose and unhooked.",
  // 5 走行・旋回中の車両転倒
  "A boom-type aerial work platform on sloped uneven ground, tipping over toward one side, its outrigger support legs NOT deployed (folded up). " +
  "A worker silhouette is inside the elevated basket as the whole machine topples over.",
  // 6 バケットと上方構造物のはさまれ
  "A boom-type aerial work platform with its basket raised up close beneath a long horizontal overhead steel beam / ceiling truss. " +
  "A worker silhouette inside the basket is pinched and squeezed between the top guardrail of the basket and the overhead beam above him.",
];

async function waitForNewImage(page, prevCount, maxSec = 240) {
  await page.waitForTimeout(6000);
  for (let w = 0; w < maxSec / 5; w++) {
    const cnt = await page.evaluate(() => Array.from(document.querySelectorAll("img")).filter((img) => {
      const src = img.src || ""; const ww = img.naturalWidth || img.width;
      return ww > 200 && (src.includes("googleusercontent") || src.startsWith("blob:") || src.startsWith("data:image"));
    }).length);
    if (cnt > prevCount) return true;
    const stop = await page.locator('button[aria-label="回答を停止"], button[aria-label*="停止"], button[aria-label*="Stop"]').first().isVisible({ timeout: 500 }).catch(() => false);
    if (!stop && w > 2) {
      const txt = await page.evaluate(() => document.body.innerText);
      if (/制限に達しました|利用上限|quota|rate.?limit|Try again later/i.test(txt)) throw new Error("QUOTA");
      return false;
    }
    await page.waitForTimeout(5000);
  }
  return false;
}

async function downloadLatest(page, outPath) {
  const b64 = await page.evaluate(async () => {
    const imgs = Array.from(document.querySelectorAll("img")).filter((img) => {
      const src = img.src || ""; const w = img.naturalWidth || img.width;
      return w > 200 && (src.includes("googleusercontent") || src.startsWith("blob:") || src.startsWith("data:image"));
    });
    if (!imgs.length) return null;
    const img = imgs[imgs.length - 1];
    if (img.src.startsWith("data:image")) return img.src.split(",")[1];
    try {
      const resp = await fetch(img.src, { credentials: "include" });
      const blob = await resp.blob();
      return await new Promise((res) => { const r = new FileReader(); r.onload = () => res(r.result.split(",")[1]); r.onerror = () => res(null); r.readAsDataURL(blob); });
    } catch {
      try { const c = document.createElement("canvas"); c.width = img.naturalWidth; c.height = img.naturalHeight; c.getContext("2d").drawImage(img, 0, 0); return c.toDataURL("image/png").split(",")[1]; } catch { return null; }
    }
  });
  if (!b64) return false;
  fs.writeFileSync(outPath, Buffer.from(b64, "base64"));
  return fs.existsSync(outPath) && fs.statSync(outPath).size > 1000;
}

const manifest = { ok: [], fail: [] };
const { ctx, page } = await launchBrowser("gemini", { viewport: { width: 1400, height: 900 }, acceptDownloads: true });
try {
  await ensureGeminiLoggedIn(page);
  await page.waitForTimeout(2000);
  await dismissOverlays(page);
  await startNewChat(page);
  await page.waitForTimeout(1500);
  await dismissOverlays(page);
  await selectImageCreationTool(page, { allowProFallback: true });
  await page.waitForTimeout(1500);

  let prev = 0;
  for (let i = 0; i < SCENES.length; i++) {
    const outPath = path.join(OUT_DIR, `gen${String(i + 1).padStart(2, "0")}.png`);
    const prompt = `${SCENES[i]}\n\n${STYLE}`;
    let done = false;
    for (let attempt = 1; attempt <= 3 && !done; attempt++) {
      console.log(`\n[gen] scene ${i + 1}/${SCENES.length} attempt ${attempt}`);
      try {
        if (i > 0 && !(await isImageToolActive(page))) { await selectImageCreationTool(page, { allowProFallback: true }); await page.waitForTimeout(500); }
        await submitPrompt(page, prompt);
        const found = await waitForNewImage(page, prev, 240);
        await page.waitForTimeout(2500);
        await saveScreenshot(page, "gen", `scene${i + 1}-a${attempt}`).catch(() => {});
        if (found && await downloadLatest(page, outPath)) {
          prev++; done = true;
          console.log(`[gen] saved ${outPath} (${fs.statSync(outPath).size} bytes)`);
        } else {
          console.warn(`[gen] no image scene ${i + 1} attempt ${attempt}`);
          await page.waitForTimeout(3000);
        }
      } catch (e) {
        console.error(`[gen] error scene ${i + 1}: ${e.message}`);
        if (e.message === "QUOTA") { manifest.fail.push({ scene: i + 1, reason: "quota" }); break; }
        await page.waitForTimeout(3000);
      }
    }
    if (done) manifest.ok.push({ scene: i + 1, file: path.basename(outPath) });
    else if (!manifest.fail.find((f) => f.scene === i + 1)) manifest.fail.push({ scene: i + 1, reason: "no-image" });
  }
} finally {
  fs.writeFileSync(path.join(OUT_DIR, "manifest.json"), JSON.stringify(manifest, null, 2));
  try { await ctx.close(); } catch {}
  console.log(`\n[gen] DONE ok=${manifest.ok.length} fail=${manifest.fail.length}`);
}
