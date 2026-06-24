/** collect_aerial2_a5.mjs : A5「感電・飛来落下・不安全行動・その他」高所作業車の事故/危険イメージ画像 収集。
 *  感電(架空線/充電部接触)、飛来落下(工具/資材の落下)、不安全行動(安全帯未使用/定員超過/移動時搭乗 等)、その他。
 *  instagram-automation方式・別プロファイル(anzen)・Chromeはkillしない・画像生成はしない・追記専用・非破壊。
 *  保存: collect_aerial2/img/NNNN.ext (4桁通し連番) / 重複排除: md5 / 索引: collect_aerial2/aerial2_index.csv
 *  実行済みクエリ: collect_aerial2/queries_done.txt に追記し再実行しない。
 *  雛形 safe1/search_ra1.mjs / collect_aerial2_a4.mjs 準拠（a.iusc解析・Referer fetch・拡張子中身判定）。
 *  カテゴリはA5内で複数型にまたがるためクエリ毎に指定（[query, clipart寄りか, 種別, カテゴリ]）。*/
import fs from "node:fs"; import path from "node:path"; import crypto from "node:crypto";
const LIB = "C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);

const ROOT = "C:/Users/kanet/20260522/safe1/collect_aerial2";
const IMG  = path.join(ROOT, "img");
const CSV  = path.join(ROOT, "aerial2_index.csv");
const QDONE = path.join(ROOT, "queries_done.txt");
fs.mkdirSync(IMG, { recursive: true });

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

// --- A5 感電・飛来落下・不安全行動・その他 クエリ（[query, clipart寄りか, 種別, カテゴリ]）---
const QUERIES = [
  // 感電
  ["高所作業車 感電 災害 イラスト", true, "教育イラスト", "感電"],
  ["高所作業車 架空線 接触 感電 イラスト", true, "教育イラスト", "感電"],
  ["高所作業車 高圧線 充電部 接近 感電 危険 イラスト", true, "教育イラスト", "感電"],
  ["高所作業車 電線 感電 注意喚起 ポスター", true, "注意喚起ポスター", "感電"],
  ["高所作業車 感電 KYT ヒヤリハット 教材 イラスト", true, "KYT教材", "感電"],
  ["高所作業車 感電 死亡災害 事例 厚生労働省", false, "実事例図/写真", "感電"],
  ["aerial work platform power line electrocution accident illustration", true, "教育イラスト", "感電"],
  ["boom lift overhead power line contact electrocution hazard illustration", true, "教育イラスト", "感電"],
  // 飛来・落下
  ["高所作業車 工具 落下 飛来 災害 イラスト", true, "教育イラスト", "飛来・落下"],
  ["高所作業車 資材 落下 下部 作業員 災害 イラスト", true, "教育イラスト", "飛来・落下"],
  ["高所作業車 落下物 飛来 注意喚起 ポスター", true, "注意喚起ポスター", "飛来・落下"],
  ["高所作業車 工具 落下 ヒヤリハット KYT イラスト", true, "KYT教材", "飛来・落下"],
  ["高所作業車 飛来落下 災害事例 厚生労働省", false, "実事例図/写真", "飛来・落下"],
  ["aerial lift falling object tool dropped hazard illustration", true, "教育イラスト", "飛来・落下"],
  ["MEWP dropped object struck by falling tool accident illustration", true, "教育イラスト", "飛来・落下"],
  // 不安全行動
  ["高所作業車 安全帯 未使用 不安全行動 イラスト", true, "教育イラスト", "不安全行動"],
  ["高所作業車 定員超過 過積載 危険 イラスト", true, "教育イラスト", "不安全行動"],
  ["高所作業車 走行中 搭乗 移動 危険 イラスト", true, "教育イラスト", "不安全行動"],
  ["高所作業車 手すり 乗り越え 身を乗り出す 危険 イラスト", true, "教育イラスト", "不安全行動"],
  ["高所作業車 脚立 併用 立ち上がり 危険 イラスト", true, "教育イラスト", "不安全行動"],
  ["高所作業車 やってはいけない 不安全行動 注意喚起 ポスター", true, "注意喚起ポスター", "不安全行動"],
  ["高所作業車 ヘルメット 未着用 不安全 KYT イラスト", true, "KYT教材", "不安全行動"],
  ["aerial work platform unsafe behavior no harness illustration", true, "教育イラスト", "不安全行動"],
  ["boom lift climbing over railing standing on rails unsafe illustration", true, "教育イラスト", "不安全行動"],
  ["scissor lift overloading exceeding capacity unsafe act illustration", true, "教育イラスト", "不安全行動"],
  // その他・総合
  ["高所作業車 事故 危険 イラスト 種類", true, "教育イラスト", "その他"],
  ["高所作業車 災害 ヒヤリハット 事例集 イラスト", true, "ヒヤリハット挿絵", "その他"],
  ["高所作業車 安全 注意喚起 ポスター イラスト", true, "注意喚起ポスター", "その他"],
  ["高所作業車 危険予知 KYT シート イラスト", true, "KYT教材", "その他"],
  ["aerial work platform safety hazard accident types illustration", true, "教育イラスト", "その他"],
];

const { ctx, page } = await launchBrowser("anzen", { viewport: { width: 1500, height: 1200 } });
let n = maxNum;
let savedTotal = 0;
let zeroStreak = 0;       // 連続「新規ゼロ」クエリ数
const newQueriesDone = [];
const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36";

try {
  for (const [q, clip, kind, cat] of QUERIES) {
    if (doneQ.has(q)) { console.log(`[SKIP done] ${q}`); continue; }
    if (zeroStreak >= 8) { console.log("=== 8クエリ連続 新規ゼロ → A5終了 ==="); break; }

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
          n, fn, cat, kind,
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

console.log(`\nA5 DONE: saved=${savedTotal}  totalImgNum=${n}  queriesRun=${newQueriesDone.length}`);
