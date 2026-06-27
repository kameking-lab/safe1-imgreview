/** ml_models.mjs — get_all_models からアニメ/イラスト系の有効 model_id を抽出（keyは出力しない）。 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { KEY } from "./mllib.mjs";
const __dirname = path.dirname(fileURLToPath(import.meta.url));
async function tryFetch(url, method, withKey) {
  try {
    const opt = { method, headers: { "Content-Type": "application/json" } };
    if (method === "POST") opt.body = JSON.stringify(withKey ? { key: KEY } : {});
    const r = await fetch(url, opt);
    const t = await r.text();
    return { http: r.status, t };
  } catch (e) { return { http: 0, t: "ERR " + e.message }; }
}
let res = await tryFetch("https://modelslab.com/api/v1/enterprise/get_all_models", "POST", true);
if (res.http !== 200 || res.t.length < 50) res = await tryFetch("https://modelslab.com/api/v1/enterprise/get_all_models", "GET", false);
console.log("HTTP", res.http, "len", res.t.length);
let arr;
try { const j = JSON.parse(res.t); arr = Array.isArray(j) ? j : (j.models || j.data || j.output || []); } catch { arr = null; }
if (!arr) { console.log("RAW_HEAD", res.t.slice(0, 600)); process.exit(0); }
fs.writeFileSync(path.join(__dirname, "_models_raw.json"), res.t);
console.log("TOTAL_MODELS", arr.length);
const norm = arr.map(m => ({ id: m.model_id || m.id || m.modelId || "", name: (m.model_name||m.name||""), cat: (m.category||m.type||m.style||"") }));
const want = /anime|illustration|cartoon|toon|comic|manga|2d|flat|line|cel/i;
const hits = norm.filter(m => want.test(m.id) || want.test(m.name) || want.test(m.cat));
console.log("ILLUST_CANDIDATES", hits.length);
for (const m of hits.slice(0, 40)) console.log("  ", JSON.stringify(m));
const sdxl = norm.filter(m => /xl|sdxl/i.test(m.id) && want.test(m.id+m.name+m.cat));
console.log("SDXL_ILLUST", JSON.stringify(sdxl.slice(0,15)));
