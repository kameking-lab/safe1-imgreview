/** dump_result.mjs : 高所作業車で検索し、結果リストの全アンカーhrefをダンプ */
import fs from "node:fs";
const LIB = "C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);
const { ctx, page } = await launchBrowser("anzen", { viewport: { width: 1400, height: 1000 } });
try {
  await page.goto("https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_FND.aspx", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(1500);
  await page.locator('input[name="keyword"]').first().fill("高所作業車");
  await Promise.all([page.waitForLoadState("domcontentloaded").catch(()=>{}), page.locator('input[type="button"][value="検索開始"]').first().click()]);
  await page.waitForTimeout(3500);
  const data = await page.evaluate(() => {
    const anchors = Array.from(document.querySelectorAll("a"))
      .map(a => ({ href: a.getAttribute("href"), full: a.href, text: (a.textContent||"").trim().slice(0,50), onclick: a.getAttribute("onclick") }))
      .filter(a => a.text && a.text.length > 8);
    return { url: location.href, anchors: anchors.slice(0, 40) };
  });
  fs.writeFileSync("C:/Users/kanet/20260522/safe1/anzen/dump_anchors.json", JSON.stringify(data, null, 2));
  console.log("URL", data.url);
  data.anchors.forEach(a => console.log(`[${a.href}] | onclick=${a.onclick} | ${a.text}`));
} finally { try { await ctx.close(); } catch {} console.log("DONE"); }
