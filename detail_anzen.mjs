/** detail_anzen.mjs : 候補事例の詳細ページを開き、本文(発生状況/原因/対策)を抽出・保存 */
import fs from "node:fs";
const LIB = "C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);
const OUT = "C:/Users/kanet/20260522/safe1/anzen/details";
fs.mkdirSync(OUT, { recursive: true });

// 本命6 + 予備
const IDS = ["101398","101281","101534","101377","101270","101412","101240","100614","55","101397","101392"];

async function getDetail(page, id) {
  const url = `https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_DET.aspx?joho_no=${id}`;
  const resp = await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForTimeout(1800);
  const status = resp ? resp.status() : 0;
  const d = await page.evaluate(() => {
    const t = document.body.innerText.replace(/\r/g,"");
    const h = (document.querySelector("h1,h2,h3") || {}).innerText || "";
    // 見出しごとの抽出（発生状況/原因/対策 系のラベルを探す）
    const grab = (labels) => {
      for (const lab of labels) {
        const re = new RegExp(lab + "[\\s\\S]{0,600}");
        const m = t.match(re);
        if (m) return m[0].slice(0, 600);
      }
      return "";
    };
    return {
      title: document.title,
      headline: h.trim().slice(0,120),
      hasCase: /発生状況|災害発生状況|原因|対策|防止/.test(t),
      bodyLen: t.length,
      jokyo: grab(["発生状況","災害発生状況","災害の発生状況"]),
      genin: grab(["原因","発生原因"]),
      taisaku: grab(["対策","防止対策","再発防止","対策のポイント"]),
      full: t.slice(0, 2500),
    };
  });
  return { id, url, finalUrl: page.url(), status, ...d };
}

const { ctx, page } = await launchBrowser("anzen", { viewport: { width: 1400, height: 1100 } });
const all = [];
try {
  for (const id of IDS) {
    try {
      const r = await getDetail(page, id);
      all.push(r);
      fs.writeFileSync(`${OUT}/case_${id}.txt`, `URL: ${r.finalUrl}\nSTATUS: ${r.status}\nTITLE: ${r.title}\nHEADLINE: ${r.headline}\nhasCase: ${r.hasCase} bodyLen:${r.bodyLen}\n\n=== FULL ===\n${r.full}`);
      console.log(`\n#${id} status=${r.status} hasCase=${r.hasCase} len=${r.bodyLen}`);
      console.log(`  ${r.headline}`);
    } catch (e) { console.error(`#${id} err ${e.message}`); all.push({ id, error: e.message }); }
  }
  fs.writeFileSync(`${OUT}/_summary.json`, JSON.stringify(all.map(a=>({id:a.id,status:a.status,hasCase:a.hasCase,bodyLen:a.bodyLen,finalUrl:a.finalUrl,headline:a.headline})), null, 2));
} finally { try { await ctx.close(); } catch {} console.log("\nDONE"); }
