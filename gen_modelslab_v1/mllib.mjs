/** mllib.mjs — ModelsLab v6 realtime クライアント。keyは .secrets/modelslab.key から読み、値は出力しない。 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const KEYFILE = path.resolve(__dirname, "..", ".secrets", "modelslab.key");
export const KEY = fs.readFileSync(KEYFILE, "utf8").trim();
export const KEY_TAIL = "…" + KEY.slice(-4);   // ログ表示用（末尾4桁のみ）

const BASE = "https://modelslab.com/api/v6/realtime";

async function postJSON(url, body) {
  const r = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  const txt = await r.text();
  let j; try { j = JSON.parse(txt); } catch { j = { status: "parse_error", raw: txt.slice(0, 400) }; }
  return { http: r.status, j };
}

// processing の場合 fetch_result/idでポーリングして最終URLを返す
async function resolveResult(j, maxWaitMs = 180000) {
  if (j.status === "success" && Array.isArray(j.output) && j.output.length) return { ok: true, urls: j.output, meta: j };
  if (j.status === "processing") {
    const id = j.id;
    const fetchUrl = j.fetch_result || `https://modelslab.com/api/v6/realtime/fetch/${id}`;
    const eta = Math.min(Math.max((j.eta || 8), 3), 40);
    const start = Date.now();
    await new Promise(r => setTimeout(r, eta * 1000));
    while (Date.now() - start < maxWaitMs) {
      const { j: fj } = await postJSON(fetchUrl, { key: KEY });
      if (fj.status === "success" && Array.isArray(fj.output) && fj.output.length) return { ok: true, urls: fj.output, meta: fj };
      if (fj.status === "error" || fj.status === "failed") return { ok: false, err: (fj.message || fj.messege || JSON.stringify(fj).slice(0,200)) };
      await new Promise(r => setTimeout(r, 5000));
    }
    return { ok: false, err: "poll_timeout" };
  }
  if (j.status === "error" || j.status === "failed") return { ok: false, err: (j.message || j.messege || JSON.stringify(j).slice(0,300)) };
  return { ok: false, err: "unexpected:" + JSON.stringify(j).slice(0, 300) };
}

const COMMON_NEG = "photo, photorealistic, realistic photo, 3d render, cgi, text, letters, words, numbers, watermark, signature, logo, arrows, caption, speech bubble, blood, gore, extra limbs, extra arms, extra legs, bad anatomy, deformed, deformed hands, mutated hands, bad hands, missing fingers, fused fingers, lowres, blurry, jpeg artifacts, tilted machine, fallen machine, overturned vehicle";

export async function text2img({ prompt, negative_prompt, width=1024, height=1024, steps=30, guidance=7.5, seed=null, model_id=null }) {
  const body = { key: KEY, prompt, negative_prompt: negative_prompt || COMMON_NEG, width, height, samples: 1,
    num_inference_steps: steps, guidance_scale: guidance, safety_checker: "no", enhance_prompt: "yes" };
  if (seed != null) body.seed = seed;
  if (model_id) body.model_id = model_id;
  const { http, j } = await postJSON(`${BASE}/text2img`, body);
  return { http, ...(await resolveResult(j)), rawStatus: j.status };
}

export async function img2img({ prompt, init_image, negative_prompt, prompt_strength=0.5, width=1024, height=1024, steps=30, guidance=7.5, seed=null, model_id=null }) {
  const body = { key: KEY, prompt, negative_prompt: negative_prompt || COMMON_NEG, init_image, prompt_strength,
    width, height, samples: 1, num_inference_steps: steps, guidance_scale: guidance, safety_checker: "no", enhance_prompt: "yes" };
  if (seed != null) body.seed = seed;
  if (model_id) body.model_id = model_id;
  const { http, j } = await postJSON(`${BASE}/img2img`, body);
  return { http, ...(await resolveResult(j)), rawStatus: j.status };
}

export async function controlnet({ prompt, init_image, controlnet_model="canny", negative_prompt, width=1024, height=1024, steps=30, guidance=7.5, seed=null, model_id=null }) {
  const body = { key: KEY, prompt, negative_prompt: negative_prompt || COMMON_NEG, init_image, control_image: init_image,
    controlnet_model, width, height, samples: 1, num_inference_steps: steps, guidance_scale: guidance,
    safety_checker: "no", enhance_prompt: "yes" };
  if (seed != null) body.seed = seed;
  if (model_id) body.model_id = model_id;
  const { http, j } = await postJSON(`${BASE}/controlnet`, body);
  return { http, ...(await resolveResult(j)), rawStatus: j.status };
}

export async function download(url, outPath) {
  const r = await fetch(url);
  if (!r.ok) return false;
  const buf = Buffer.from(await r.arrayBuffer());
  fs.writeFileSync(outPath, buf);
  return fs.statSync(outPath).size > 3000;
}
export { COMMON_NEG };
