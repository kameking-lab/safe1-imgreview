/** explore_anzen.mjs : 職場のあんぜんサイト 労働災害事例検索ページの構造を把握 */
import fs from "node:fs";
const LIB = "C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser, saveScreenshot } = await import(`file:///${LIB}/browser-helpers.mjs`);
const OUT = "C:/Users/kanet/20260522/safe1/anzen";
fs.mkdirSync(OUT, { recursive: true });

const { ctx, page } = await launchBrowser("anzen", { viewport: { width: 1400, height: 1000 } });
try {
  const url = "https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_FND.aspx";
  const resp = await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForTimeout(2500);
  console.log("STATUS", resp && resp.status(), url);
  // フォーム要素ダンプ
  const form = await page.evaluate(() => {
    const inputs = Array.from(document.querySelectorAll("input")).map(e => ({tag:"input", type:e.type, name:e.name, id:e.id, value:(e.value||"").slice(0,30)}));
    const selects = Array.from(document.querySelectorAll("select")).map(e => ({tag:"select", name:e.name, id:e.id, opts:Array.from(e.options).slice(0,8).map(o=>o.text)}));
    const btns = Array.from(document.querySelectorAll("button, input[type=submit], input[type=button], a.btn")).map(e=>({tag:e.tagName, name:e.name, id:e.id, value:e.value, text:(e.textContent||"").trim().slice(0,20)}));
    return { title: document.title, inputs, selects, btns, bodyLen: document.body.innerText.length };
  });
  fs.writeFileSync(`${OUT}/search_form.json`, JSON.stringify(form, null, 2));
  console.log("TITLE", form.title, "inputs", form.inputs.length, "selects", form.selects.length);
  console.log(JSON.stringify(form.inputs.filter(i=>i.type!=="hidden"), null, 1));
  console.log("SELECTS", JSON.stringify(form.selects, null, 1));
  console.log("BTNS", JSON.stringify(form.btns, null, 1));
  await saveScreenshot(page, "anzen", "search").catch(()=>{});
} finally { try { await ctx.close(); } catch {} console.log("DONE"); }
