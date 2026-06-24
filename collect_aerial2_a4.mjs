/** collect_aerial2_a4.mjs : A4「転倒・横転」高所作業車の事故/危険イメージ画像 収集。
 *  機体ごとの転倒・横転、軟弱地盤/傾斜/アウトリガー未設置による転倒等。
 *  instagram-automation方式・別プロファイル(anzen)・Chromeはkillしない・画像生成はしない・追記専用・非破壊。
 *  保存: collect_aerial2/img/NNNN.ext (4桁通し連番) / 重複排除: md5 / 索引: collect_aerial2/aerial2_index.csv
 *  実行済みクエリ: collect_aerial2/queries_done.txt に追記し再実行しない。
 *  雛形 safe1/search_ra1.mjs / collect_aerial2_a3.mjs 準拠（a.iusc解析・Referer fetch・拡張子中身判定）。*/
import fs from "node:fs"; import path from "node:path"; import crypto from "node:crypto";
const LIB = "C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);

const ROOT = "C:/Users/kanet/20260522/safe1/collect_aerial2";
const IMG  = path.join(ROOT, "img");
const CSV  = path.join(ROOT, "aerial2_index.csv");
const QDONE = path.join(ROOT, "queries_done.txt");
fs.mkdirSync(IMG, { recursive: true });

const CATEGORY = "転倒・横転";

// --- 既存状態の読込（再開時に重複/破壊しない）---
const md5set = new Set();   // 既存画像のmd5
const murlset = new Set();  // 既存indexのmurl(=出所URL)で再DL抑制（補助）
let maxNum = 0;

if (fs.existsSync(IMG)) {
  for (const f of fs.readdirSync(IMG)) {
    const m = /^(\d{4})\./.exec(f);
    if (m) maxNum = Math.max(maxNum, +m[1]);
    try {
      const buf = fs.readFileSync(path.join(IMG, f));
      md5set.add(crypto.createHash("md5").update(buf).digest("hex"));
    } catch {}
  }
}
let csvRows = [];
if (fs.existsSync(CSV)) {
  csvRows = fs.readFileSync(CSV, "utf8").split(/\r?\n/).filter(Boolean);
  for (let i = 1; i < csvRows.length; i++) {
    const cols = csvRows[i].split(",");
    if (cols[7]) md5set.add(cols[7].replace(/"/g, ""));
    if (cols[4]) murlset.add(cols[4].replace(/"/g, ""));
  }
}
const doneQ = fs.existsSync(QDONE)
  ? new Set(fs.readFileSync(QDONE, "utf8").split(/\r?\n/).filter(Boolean))
  : new Set();

const CSV_HEADER = "通し番号,ファイル名,カテゴリ,種別,出所URL,出所ドメイン,状況メモ,md5";
if (!fs.existsSync(CSV)) fs.writeFileSync(CSV, CSV_HEADER + "\r\n");

// --- A4 転倒・横転 クエリ（[query, clipart寄りか, 種別ラベル]）---
const QUERIES = [
  ["高所作業車 転倒 災害 イラスト", true,  "教育イラスト"],
  ["高所作業車 横転 事故 イラスト", true, "教育イラスト"],
  ["高所作業車 軟弱地盤 沈下 転倒 イラスト", true, "教育イラスト"],
  ["高所作業車 アウトリガー 未設置 転倒 災害 イラスト", true, "教育イラスト"],
  ["高所作業車 傾斜地 転倒 搭乗者 投げ出され イラスト", true, "教育イラスト"],
  ["高所作業車 横転 KYT ヒヤリハット 教材 イラスト", true, "KYT教材"],
  ["高所作業車 転倒 注意喚起 ポスター", true, "注意喚起ポスター"],
  ["高所作業車 段差 転倒 危険 イラスト", true, "ヒヤリハット挿絵"],
  ["ブーム式 高所作業車 横転 転倒 災害 イラスト", true, "教育イラスト"],
  ["シザース 高所作業車 横転 転倒 危険 イラスト", true, "教育イラスト"],
  ["高所作業車 転倒 死亡災害 事例 厚生労働省", false, "実事例図/写真"],
  ["職場のあんぜんサイト 高所作業車 転倒 災害事例", false, "実事例図/写真"],
  ["高所作業車 転倒 横転 災害事例 建災防", false, "実事例図/写真"],
  ["高所作業車 横転 災害事例 図", false, "実事例図/写真"],
  ["高所作業車 軟弱地盤 転倒 死亡災害 事例", false, "実事例図/写真"],
  ["aerial work platform boom lift tip over accident illustration", true, "教育イラスト"],
  ["scissor lift tip over overturn accident illustration", true, "教育イラスト"],
  ["MEWP overturn tipping hazard soft ground outrigger illustration", true, "教育イラスト"],
  ["aerial lift overturn slope worker thrown accident illustration", true, "教育イラスト"],
  ["boom lift tip over uneven ground fatality case photo", false, "実事例図/写真"],
];

const { ctx, page } = await launchBrowser("anzen", { viewport: { width: 1500, height: 1200 } });
let n = maxNum;
let savedTotal = 0;
let zeroStreak = 0;       // 連続「新規ゼロ」クエリ数
const newQueriesDone = [];
const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36";

try {
  for (const [q, clip, kind] of QUERIES) {
    if (doneQ.has(q)) { console.log(`[SKIP done] ${q}`); continue; }
    if (zeroStreak >= 8) { console.log("=== 8クエリ連続 新規ゼロ → A4終了 ==="); break; }

    const filt = clip ? "&qft=+filterui:photo-clipart" : "";
    const url = `https://www.bing.com/images/search?q=${encodeURIComponent(q)}${filt}`;
    let items = [];
    try {
      await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
      await page.waitForTimeout(2500);
      items = await page.evaluate(() =>
        Array.from(document.querySelectorAll("a.iusc")).slice(0, 35)
          .map(a => { try { return JSON.parse(a.getAttribute("m")); } catch { return null; } })
          .filter(Boolean).map(m => ({ murl: m.murl, purl: m.purl, t: m.t || "" })));
    } catch (e) { console.log("  query err", q, e.message); }

    let newThisQ = 0;
    for (const it of items) {
      if (!it.murl) continue;
      try {
        const ref = it.purl || "https://www.bing.com/";
        const r = await fetch(it.murl, {
          headers: { "User-Agent": UA, "Referer": ref, "Accept": "image/avif,image/webp,image/*,*/*" },
          signal: AbortSignal.timeout(20000),
        });
        if (!r.ok) continue;
        const buf = Buffer.from(await r.arrayBuffer());
        if (buf.length < 5000) continue;
        const sig = buf.subarray(0, 4).toString("hex");
        let ext = "";
        if (sig.startsWith("89504e47")) ext = "png";
        else if (sig.startsWith("ffd8")) ext = "jpg";
        else if (buf.subarray(0, 6).toString("ascii").startsWith("GIF8")) ext = "gif";
        else if (buf.subarray(8, 12).toString("ascii") === "WEBP") ext = "webp";
        else continue;
        const md5 = crypto.createHash("md5").update(buf).digest("hex");
        if (md5set.has(md5)) continue;       // md5重複排除（既存img/index含む）
        md5set.add(md5);
        const fn = `${String(++n).padStart(4, "0")}.${ext}`;
        fs.writeFileSync(path.join(IMG, fn), buf);
        let dom = ""; try { dom = new URL(it.purl).hostname; } catch {}
        const memo = q.replace(/"/g, "'");
        const row = [
          n, fn, CATEGORY, kind,
          `"${(it.purl || "").replace(/"/g, "'")}"`,
          dom, `"${memo}"`, md5,
        ].join(",");
        fs.appendFileSync(CSV, row + "\r\n");
        savedTotal++; newThisQ++;
        console.log(`  saved ${fn} ${buf.length}b <- ${dom}`);
      } catch { /* skip individual */ }
    }
    console.log(`[Q] ${q} -> items=${items.length} new=${newThisQ}`);
    fs.appendFileSync(QDONE, q + "\r\n");
    newQueriesDone.push(q);
    if (newThisQ === 0) zeroStreak++; else zeroStreak = 0;
  }
} finally { try { await ctx.close(); } catch {} }

console.log(`\nA4 DONE: saved=${savedTotal}  totalImgNum=${n}  queriesRun=${newQueriesDone.length}`);
