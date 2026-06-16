/** collect_anzen.mjs : キーワード検索→ f_page_send(joho_no) を抽出して候補一覧化 */
import fs from "node:fs";
const LIB = "C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);
const OUT = "C:/Users/kanet/20260522/safe1/anzen";
fs.mkdirSync(OUT, { recursive: true });
const KEYWORDS = ["テールゲートリフター","テールゲート","ロールボックスパレット","かご車","荷台","昇降","トラック 荷台","高所作業車"];

async function search(page, kw) {
  await page.goto("https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_FND.aspx", { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForTimeout(1200);
  await page.locator('input[name="keyword"]').first().fill(kw);
  await Promise.all([page.waitForLoadState("domcontentloaded").catch(()=>{}), page.locator('input[type="button"][value="検索開始"]').first().click().catch(()=>{})]);
  await page.waitForTimeout(3000);
  return await page.evaluate(() => {
    const out = []; const seen = new Set();
    document.querySelectorAll("a").forEach(a => {
      const h = a.getAttribute("href") || "";
      const m = h.match(/f_page_send\((\d+)\)/);
      if (m && !seen.has(m[1])) { seen.add(m[1]); out.push({ joho_no: m[1], title: (a.textContent||"").trim() }); }
    });
    const cntM = (document.body.innerText.match(/検索結果は([\d,]+)件/)||[])[1] || "?";
    return { total: cntM, cases: out };
  });
}

const { ctx, page } = await launchBrowser("anzen", { viewport: { width: 1400, height: 1000 } });
const res = {};
try {
  for (const kw of KEYWORDS) {
    try { const r = await search(page, kw); res[kw] = r; console.log(`\n== "${kw}"  total=${r.total}  page1=${r.cases.length} ==`); r.cases.forEach(c=>console.log(`  ${c.joho_no}: ${c.title.slice(0,70)}`)); }
    catch (e) { console.error(`"${kw}" err ${e.message}`); res[kw]={error:e.message}; }
  }
  fs.writeFileSync(`${OUT}/candidates.json`, JSON.stringify(res, null, 2));
} finally { try { await ctx.close(); } catch {} console.log("\nDONE"); }
