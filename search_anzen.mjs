/** search_anzen.mjs : キーワードで労働災害事例を検索し、結果の事例詳細リンク(joho_no)を収集 */
import fs from "node:fs";
const LIB = "C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser, saveScreenshot } = await import(`file:///${LIB}/browser-helpers.mjs`);
const OUT = "C:/Users/kanet/20260522/safe1/anzen";
fs.mkdirSync(OUT, { recursive: true });

const KEYWORDS = ["テールゲートリフター","テールゲート","ロールボックスパレット","かご車","昇降装置","荷台 あおり","高所作業車"];

async function collect(page) {
  // 結果ページ内の sai_det.aspx?joho_no= へのリンクを収集
  return await page.evaluate(() => {
    const out = [];
    document.querySelectorAll("a").forEach(a => {
      const href = a.href || "";
      const m = href.match(/sai_det\.aspx\?joho_no=(\d+)/i);
      if (m) out.push({ joho_no: m[1], text: (a.textContent||"").trim().slice(0,80), href });
    });
    return out;
  });
}

const { ctx, page } = await launchBrowser("anzen", { viewport: { width: 1400, height: 1000 } });
const result = {};
try {
  for (const kw of KEYWORDS) {
    try {
      await page.goto("https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_FND.aspx", { waitUntil: "domcontentloaded", timeout: 60000 });
      await page.waitForTimeout(1500);
      const kwInput = page.locator('input[name="keyword"]').first();
      await kwInput.fill(kw);
      await page.waitForTimeout(300);
      // 「検索開始」ボタン
      const btn = page.locator('input[type="button"][value="検索開始"]').first();
      await Promise.all([
        page.waitForLoadState("domcontentloaded").catch(()=>{}),
        btn.click().catch(()=>{}),
      ]);
      await page.waitForTimeout(3000);
      let links = await collect(page);
      // 件数表示や次ページがある場合に備え、本文も少し記録
      const info = await page.evaluate(() => ({ url: location.href, title: document.title, snippet: document.body.innerText.replace(/\s+/g," ").slice(0,300) }));
      // 重複除去
      const seen = new Set(); links = links.filter(l => !seen.has(l.joho_no) && seen.add(l.joho_no));
      result[kw] = { info, count: links.length, links };
      console.log(`KW "${kw}" -> ${links.length} cases  [${info.url}]`);
      console.log("  " + links.slice(0,12).map(l=>l.joho_no+":"+l.text.slice(0,24)).join(" | "));
      await saveScreenshot(page, "anzen", `res_${kw.slice(0,6)}`).catch(()=>{});
    } catch (e) { console.error(`KW "${kw}" err: ${e.message}`); result[kw] = { error: e.message }; }
  }
  fs.writeFileSync(`${OUT}/search_results.json`, JSON.stringify(result, null, 2));
} finally { try { await ctx.close(); } catch {} console.log("DONE"); }
