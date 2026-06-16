/** stage1_search.mjs : TGL操作起因(昇降板からの墜落/はさまれ)の事例を検索→候補本文を取得 */
import fs from "node:fs";
const LIB = "C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);
const OUT = "C:/Users/kanet/20260522/safe1/anzen";
fs.mkdirSync(`${OUT}/details`, { recursive: true });
const KEYWORDS = ["昇降板","テールゲートリフター","リフト 荷台","荷台 昇降","あおり 墜落","荷台 はさまれ","テールゲート 昇降","パワーゲート"];

async function search(page, kw) {
  await page.goto("https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_FND.aspx", { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForTimeout(1200);
  await page.locator('input[name="keyword"]').first().fill(kw);
  await Promise.all([page.waitForLoadState("domcontentloaded").catch(()=>{}), page.locator('input[type="button"][value="検索開始"]').first().click().catch(()=>{})]);
  await page.waitForTimeout(2800);
  return await page.evaluate(() => {
    const out=[]; const seen=new Set();
    document.querySelectorAll("a").forEach(a=>{const h=a.getAttribute("href")||"";const m=h.match(/f_page_send\((\d+)\)/);if(m&&!seen.has(m[1])){seen.add(m[1]);out.push({joho_no:m[1],title:(a.textContent||"").trim()});}});
    const t=(document.body.innerText.match(/検索結果は([\d,]+)件/)||[])[1]||"?";
    return { total:t, cases:out };
  });
}
async function detail(page, id) {
  const url=`https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_DET.aspx?joho_no=${id}`;
  const resp=await page.goto(url,{waitUntil:"domcontentloaded",timeout:60000}); await page.waitForTimeout(1500);
  const d=await page.evaluate(()=>{const t=document.body.innerText.replace(/\r/g,"");return{ full:t.slice(0,2600), has:/発生状況|原因|対策/.test(t)};});
  return { id, url, status: resp?resp.status():0, ...d };
}

const { ctx, page } = await launchBrowser("anzen", { viewport:{width:1400,height:1000} });
const res={};
try {
  for (const kw of KEYWORDS) {
    try { const r=await search(page,kw); res[kw]=r; console.log(`\n== "${kw}" total=${r.total} p1=${r.cases.length} ==`); r.cases.forEach(c=>console.log(`  ${c.joho_no}: ${c.title.slice(0,70)}`)); }
    catch(e){ console.error(`"${kw}" ${e.message}`); }
  }
  fs.writeFileSync(`${OUT}/stage1_candidates.json`, JSON.stringify(res,null,2));
  // タイトルに 昇降板/テールゲート/リフト/あおり/パワーゲート を含み 墜落/転落/はさ を含むものを自動詳細取得
  const ids=new Set();
  Object.values(res).forEach(r=>(r.cases||[]).forEach(c=>{ if(/昇降板|テールゲート|リフト|あおり|パワーゲート|荷台/.test(c.title) && /墜落|転落|はさ|挟|落ち|踏み外/.test(c.title)) ids.add(c.joho_no); }));
  console.log("\n--- auto-detail candidates:", [...ids].join(","));
  for (const id of ids) {
    try { const d=await detail(page,id); fs.writeFileSync(`${OUT}/details/s1_${id}.txt`, `URL:${d.url}\nSTATUS:${d.status}\n\n${d.full}`); console.log(`#${id} status=${d.status} has=${d.has}`); }
    catch(e){ console.error(`#${id} ${e.message}`); }
  }
} finally { try{await ctx.close();}catch{} console.log("\nDONE"); }
