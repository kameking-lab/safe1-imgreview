// gen_photo.mjs — 1元絵の A/B/C/D 4枚を生成（OpenAI gpt-image-2 / Google Nano Banana Pro）。
// 使い方: node gen_photo.mjs <番号(例 0001)>
// キー値は一切出力しない。既存ファイルはスキップ（再開安全）。削除/上書きしない。
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";

const BASE = "C:/Users/kanet/20260522/safe1";
const NUM = (process.argv[2] || "").trim();
if (!/^\d{4}$/.test(NUM)) { console.error("usage: node gen_photo.mjs <4桁番号>"); process.exit(2); }

// ---- .env (値は出力しない) ----
function readEnv() {
  const out = {};
  const p = path.join(BASE, ".env");
  if (!fs.existsSync(p)) return out;
  for (const ln of fs.readFileSync(p, "utf8").split(/\r?\n/)) {
    const m = ln.match(/^([A-Z0-9_]+)=(.*)$/);
    if (m) out[m[1]] = m[2];
  }
  return out;
}
const ENV = readEnv();
const OPENAI = ENV.OPENAI_API_KEY || process.env.OPENAI_API_KEY || "";
const GEMINI = ENV.GEMINI_API_KEY || process.env.GEMINI_API_KEY || "";
if (!OPENAI || !GEMINI) { console.error("キー未設定 (OPENAI/GEMINI のいずれか欠落)"); process.exit(3); }

// ---- img_index.csv から該当行 ----
function parseCsv() {
  let txt = fs.readFileSync(path.join(BASE, "collect2", "img_index.csv"), "utf8");
  if (txt.charCodeAt(0) === 0xFEFF) txt = txt.slice(1);
  const rows = [];
  for (const line of txt.split(/\r?\n/)) {
    if (!line.trim()) continue;
    const cells = []; let cur = "", q = false;
    for (let i = 0; i < line.length; i++) {
      const c = line[i];
      if (q) { if (c === '"' && line[i + 1] === '"') { cur += '"'; i++; } else if (c === '"') q = false; else cur += c; }
      else { if (c === '"') q = true; else if (c === ",") { cells.push(cur); cur = ""; } else cur += c; }
    }
    cells.push(cur); rows.push(cells);
  }
  return rows;
}
const rows = parseCsv();
const rec = rows.find(r => (r[0] || "").trim() === NUM);
if (!rec) { console.error("番号が img_index.csv に無い:", NUM); process.exit(4); }
const refFile = rec[1].trim(), cat = rec[2].trim(), atype = (rec[3] || "").trim(), desc = (rec[6] || "").trim();
const isAerial = cat !== "TGL";

const OUTDIR = path.join(BASE, "photos_v15", NUM);
fs.mkdirSync(OUTDIR, { recursive: true });

// ---- 元絵を 1024px PNG に正規化（PIL を py で実行） ----
const SRC = path.join(OUTDIR, "source_ref.png");
if (!fs.existsSync(SRC)) {
  const inp = path.join(BASE, "collect2", "img", refFile);
  const code = `from PIL import Image
im=Image.open(r"${inp}")
try:
    im.seek(0)
except Exception: pass
im=im.convert("RGB")
w,h=im.size; s=1024/max(w,h);
if s<1: im=im.resize((max(1,int(w*s)),max(1,int(h*s))))
im.save(r"${SRC}")
print("ok")`;
  execFileSync("py", ["-c", code], { stdio: "pipe" });
}
const refB64 = fs.readFileSync(SRC).toString("base64");

// ---- プロンプト ----
const PPE = "Japanese male worker(s) on a real Japanese worksite, hard hat WITH CHIN STRAP, hi-vis vest and work clothes, safety boots" + (isAerial ? ", and a FULL-BODY SAFETY HARNESS" : "") + ". Japanese-spec equipment (NOT an excavator, NOT a forklift unless that is the depicted machine). NO company logos, NO readable text/signage, NO blood/gore. Capture the DANGEROUS MOMENT of the accident.";
const machine = isAerial
  ? "a Japanese-spec aerial work platform / MEWP (boom or scissor lift with a work basket)"
  : "a Japanese truck fitted with a TAIL-GATE LIFTER / power-gate (rear lift platform)";
const FAITH = `Reproduce the EXACT accident mechanism of the reference illustration: the same composition, the same direction of force, the same contact point, and the same machine type (${machine}). Keep precisely WHAT tips/falls/slides/pinches in WHICH direction and HOW the person is injured. Accident type: ${atype}. Reference note: ${desc}`;

const realPrompt = `A photorealistic documentary photograph of a workplace accident in Japan. ${FAITH} ${PPE} Realistic lighting, natural candid photo, single frame, no collage.`;
const eventCtx = isAerial
  ? "Change the context to an EXHIBITION / EVENT build-up venue: the aerial platform is being used for venue signage hanging / exhibition booth upper assembly / ceiling-truss work; background shows exhibition panels, booth frames and hall structure."
  : "Change the context to an EXHIBITION / EVENT build-up venue: the tail-gate lifter load is EXHIBITION PANELS / display fixtures being unloaded at a hall; background shows an exhibition hall and booth materials.";
const eventPrompt = `A photorealistic documentary photograph of a workplace accident at a Japanese EXHIBITION / EVENT set-up site. ${FAITH} ${eventCtx} Keep the accident direction, contact point and machine type UNCHANGED. ${PPE} Realistic lighting, natural candid photo, single frame, no collage.`;

const TARGETS = [
  { file: "A_openai.png", api: "openai", prompt: realPrompt },
  { file: "B_google.png", api: "google", prompt: realPrompt },
  { file: "C_openai_event.png", api: "openai", prompt: eventPrompt },
  { file: "D_google_event.png", api: "google", prompt: eventPrompt },
];

const meta = fs.existsSync(path.join(OUTDIR, "gen_meta.json"))
  ? JSON.parse(fs.readFileSync(path.join(OUTDIR, "gen_meta.json"), "utf8"))
  : { num: NUM, cat, refFile, openai_model: null, google_model: null, results: {} };

const sleep = ms => new Promise(r => setTimeout(r, ms));

// ---- OpenAI Images edits (gpt-image-2 -> gpt-image-1) ----
const OAI_MODELS = ["gpt-image-2", "gpt-image-1"];
async function genOpenAI(prompt) {
  let lastErr = "";
  for (const model of OAI_MODELS) {
    for (let attempt = 0; attempt < 4; attempt++) {
      try {
        const fd = new FormData();
        fd.append("model", model);
        fd.append("image", new Blob([fs.readFileSync(SRC)], { type: "image/png" }), "ref.png");
        fd.append("prompt", prompt);
        fd.append("size", "1024x1024");
        fd.append("quality", "high");
        fd.append("n", "1");
        const r = await fetch("https://api.openai.com/v1/images/edits", {
          method: "POST", headers: { Authorization: `Bearer ${OPENAI}` }, body: fd,
        });
        if (r.status === 429 || r.status >= 500) { lastErr = `http ${r.status}`; await sleep(2000 * 2 ** attempt); continue; }
        const j = await r.json();
        if (j?.data?.[0]?.b64_json) return { b64: j.data[0].b64_json, model };
        const em = j?.error?.message || JSON.stringify(j).slice(0, 200);
        lastErr = em;
        if (/model/i.test(em) && /not|exist|unknown|invalid/i.test(em)) break; // try next model
        await sleep(1500 * 2 ** attempt);
      } catch (e) { lastErr = e.message; await sleep(1500 * 2 ** attempt); }
    }
  }
  throw new Error("openai: " + lastErr);
}

// ---- Google generateContent (gemini-3-pro-image-preview -> gemini-2.5-flash-image) ----
const G_MODELS = ["gemini-3-pro-image-preview", "gemini-2.5-flash-image"];
async function genGoogle(prompt) {
  let lastErr = "";
  for (const model of G_MODELS) {
    for (let attempt = 0; attempt < 4; attempt++) {
      try {
        const body = {
          contents: [{ parts: [{ text: prompt }, { inline_data: { mime_type: "image/png", data: refB64 } }] }],
          generationConfig: { responseModalities: ["IMAGE"] },
        };
        const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`, {
          method: "POST", headers: { "Content-Type": "application/json", "x-goog-api-key": GEMINI }, body: JSON.stringify(body),
        });
        if (r.status === 429 || r.status >= 500) { lastErr = `http ${r.status}`; await sleep(3000 * 2 ** attempt); continue; }
        const j = await r.json();
        const parts = j?.candidates?.[0]?.content?.parts || [];
        const img = parts.find(p => p.inlineData?.data || p.inline_data?.data);
        if (img) return { b64: (img.inlineData || img.inline_data).data, model };
        const em = j?.error?.message || JSON.stringify(j).slice(0, 200);
        lastErr = em;
        if (/model/i.test(em) && /not|found|unknown|invalid|support/i.test(em)) break; // next model
        await sleep(2000 * 2 ** attempt);
      } catch (e) { lastErr = e.message; await sleep(2000 * 2 ** attempt); }
    }
  }
  throw new Error("google: " + lastErr);
}

let ok = 0, fail = 0;
for (const t of TARGETS) {
  const out = path.join(OUTDIR, t.file);
  if (fs.existsSync(out) && fs.statSync(out).size > 4000) { console.log("skip(exists)", NUM, t.file); ok++; continue; }
  try {
    const res = t.api === "openai" ? await genOpenAI(t.prompt) : await genGoogle(t.prompt);
    fs.writeFileSync(out, Buffer.from(res.b64, "base64"));
    if (t.api === "openai") meta.openai_model = res.model; else meta.google_model = res.model;
    meta.results[t.file] = { ok: true, model: res.model };
    console.log("saved", NUM, t.file, "(" + res.model + ")");
    ok++;
  } catch (e) {
    meta.results[t.file] = { ok: false, error: String(e.message).slice(0, 200) };
    console.error("FAIL", NUM, t.file, "-", String(e.message).slice(0, 160));
    fail++;
  }
  fs.writeFileSync(path.join(OUTDIR, "gen_meta.json"), JSON.stringify(meta, null, 2));
}
console.log(`DONE ${NUM} ok=${ok} fail=${fail}`);
process.exit(0);
