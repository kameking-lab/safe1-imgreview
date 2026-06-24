/** _smoke_a1.mjs : A1 疎通確認のみ。anzenプロファイルでBing画像検索を1クエリ開き、
 *  a.iusc の件数を数えるだけ。画像保存しない・生成しない・非破壊。Chromeはkillしない。*/
import fs from "node:fs";
const LIB = "C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);
const LOG = "C:/Users/kanet/20260522/safe1/collect_aerial2/_smoke_a1.log";
const lines = [];
const log = (s) => { console.log(s); lines.push(s); };

const q = "高所作業車 転倒 災害 イラスト";
const url = `https://www.bing.com/images/search?q=${encodeURIComponent(q)}&qft=+filterui:photo-clipart`;
let count = 0, sample = null;
const { ctx, page } = await launchBrowser("anzen", { viewport: { width: 1500, height: 1200 } });
try {
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForTimeout(2500);
  const items = await page.evaluate(() =>
    Array.from(document.querySelectorAll("a.iusc")).slice(0, 30)
      .map(a => { try { return JSON.parse(a.getAttribute("m")); } catch { return null; } })
      .filter(Boolean).map(m => ({ murl: m.murl, purl: m.purl })));
  count = items.length;
  if (items[0]) sample = { hasMurl: !!items[0].murl, hasPurl: !!items[0].purl };
} catch (e) {
  log(`ERR: ${e.message}`);
} finally { try { await ctx.close(); } catch {} }

log(`SMOKE q="${q}" -> a.iusc parsed=${count}`);
log(`sample firstItem keys present: ${JSON.stringify(sample)}`);
log(count > 0 ? "RESULT: OK (anzen profile reachable, a.iusc parseable)" : "RESULT: ZERO (check selector/profile)");
fs.writeFileSync(LOG, lines.join("\n") + "\n");
