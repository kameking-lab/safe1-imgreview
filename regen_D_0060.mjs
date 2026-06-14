// regen_D_0060.mjs — #0060 の D_google_event.png のみ再生成（元版に実在ロゴ風の看板「東芝/東北ビ…」が出たため）。
// gen_photo.mjs の Google 経路を流用。キー値は出力しない。canonical D を上書き（自己点検の再生成）。
import fs from "node:fs";
import path from "node:path";

const BASE = "C:/Users/kanet/20260522/safe1";
const NUM = "0060";
const OUTDIR = path.join(BASE, "photos_v15", NUM);

function readEnv() {
  const out = {}; const p = path.join(BASE, ".env");
  if (!fs.existsSync(p)) return out;
  for (const ln of fs.readFileSync(p, "utf8").split(/\r?\n/)) {
    const m = ln.match(/^([A-Z0-9_]+)=(.*)$/); if (m) out[m[1]] = m[2];
  }
  return out;
}
const ENV = readEnv();
const GEMINI = ENV.GEMINI_API_KEY || process.env.GEMINI_API_KEY || "";
if (!GEMINI) { console.error("キー未設定 (GEMINI)"); process.exit(3); }

const SRC = path.join(OUTDIR, "source_ref.png");
const refB64 = fs.readFileSync(SRC).toString("base64");

const PPE = "Japanese male worker(s) on a real Japanese worksite, hard hat WITH CHIN STRAP, hi-vis vest and work clothes, safety boots, and a FULL-BODY SAFETY HARNESS. Japanese-spec equipment (NOT an excavator). Capture the DANGEROUS MOMENT of the accident.";
const machine = "a Japanese-spec aerial work platform / MEWP (truck-mounted telescopic boom lift with a work basket)";
const FAITH = `Reproduce the EXACT accident mechanism of the reference illustration: same composition, same direction of force, same contact point, same machine type (${machine}). The work basket at the boom tip makes ELECTRICAL CONTACT with an overhead line, producing a bright arc-flash burst of sparks at the basket; the worker(s) in the elevated basket are struck by the electrical flash.`;
const eventCtx = "Context: a Japanese EXHIBITION / EVENT build-up venue — the aerial platform is used for ceiling-truss / venue signage work; background shows exhibition booth frames and hall structure.";
const NOLOGO = "ABSOLUTELY NO brand names, NO manufacturer logos, NO company names, NO readable text/signage/booth banners anywhere — all booths, panels, trucks and equipment must be PLAIN and UNBRANDED with blank surfaces (no kanji company names like '東芝'/'東北', no maker text on grille/door/body). NO blood/gore.";
const prompt = `A photorealistic documentary photograph of a workplace accident at a Japanese exhibition / event set-up site. ${FAITH} ${eventCtx} Keep the accident direction, contact point and machine type UNCHANGED. ${PPE} ${NOLOGO} Realistic lighting, natural candid photo, single frame, no collage.`;

const G_MODELS = ["gemini-3-pro-image-preview", "gemini-2.5-flash-image"];
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function genGoogle() {
  let lastErr = "";
  for (const model of G_MODELS) {
    for (let attempt = 0; attempt < 4; attempt++) {
      try {
        const body = { contents: [{ parts: [{ text: prompt }, { inline_data: { mime_type: "image/png", data: refB64 } }] }], generationConfig: { responseModalities: ["IMAGE"] } };
        const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`, { method: "POST", headers: { "Content-Type": "application/json", "x-goog-api-key": GEMINI }, body: JSON.stringify(body) });
        if (r.status === 429 || r.status >= 500) { lastErr = `http ${r.status}`; await sleep(3000 * 2 ** attempt); continue; }
        const j = await r.json();
        const parts = j?.candidates?.[0]?.content?.parts || [];
        const img = parts.find(p => p.inlineData?.data || p.inline_data?.data);
        if (img) return { b64: (img.inlineData || img.inline_data).data, model };
        const em = j?.error?.message || JSON.stringify(j).slice(0, 200); lastErr = em;
        if (/model/i.test(em) && /not|found|unknown|invalid|support/i.test(em)) break;
        await sleep(2000 * 2 ** attempt);
      } catch (e) { lastErr = e.message; await sleep(2000 * 2 ** attempt); }
    }
  }
  throw new Error("google: " + lastErr);
}

const res = await genGoogle();
fs.writeFileSync(path.join(OUTDIR, "D_google_event.png"), Buffer.from(res.b64, "base64"));
const metaPath = path.join(OUTDIR, "gen_meta.json");
const meta = JSON.parse(fs.readFileSync(metaPath, "utf8"));
meta.google_model = res.model;
meta.results["D_google_event.png"] = { ok: true, model: res.model, regen: "no-logo-fix(booth-brand)" };
fs.writeFileSync(metaPath, JSON.stringify(meta, null, 2));
console.log("regen D_google_event.png", "(" + res.model + ")");
