/** ml_modeltest.mjs — イラスト系 model_id と endpoint(realtime/images) の組合せを試し、画風を比較する。 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { KEY, COMMON_NEG, download } from "./mllib.mjs";
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(__dirname, "_modeltest"); fs.mkdirSync(OUT, { recursive: true });
const prompt = "flat 2D anime style safety education illustration, KYT training poster, clean bold line art and cel shading, a Japanese male construction worker with chin-strap helmet, high-visibility vest and full-body harness, on the platform of a vertical scissor lift at an exhibition hall booth with aluminum truss, leaning out over the guardrail losing balance and beginning to fall, alarmed face, flat colors, not a photograph";

async function post(url, body) {
  const r = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  let j; try { j = JSON.parse(await r.text()); } catch (e) { j = { status: "parse_err" }; }
  return { http: r.status, j };
}
async function resolve(j) {
  if (j.status === "success" && j.output?.length) return j.output[0];
  if (j.status === "processing") {
    const f = j.fetch_result || `https://modelslab.com/api/v6/realtime/fetch/${j.id}`;
    await new Promise(r => setTimeout(r, Math.min((j.eta||8),30) * 1000));
    for (let i = 0; i < 30; i++) {
      const { j: fj } = await post(f, { key: KEY });
      if (fj.status === "success" && fj.output?.length) return fj.output[0];
      if (fj.status === "failed" || fj.status === "error") return null;
      await new Promise(r => setTimeout(r, 5000));
    }
  }
  return null;
}
const combos = [
  ["realtime", null, "realtime-default"],
  ["images", "flat-2d-animerge", "img-flat2d"],
  ["images", "anything-v5", "img-anythingv5"],
  ["images", "samaritan-3d-cartoon", "img-samaritan"],
  ["images", "toonyou", "img-toonyou"],
];
for (const [ep, model_id, tag] of combos) {
  const url = ep === "realtime" ? "https://modelslab.com/api/v6/realtime/text2img" : "https://modelslab.com/api/v6/images/text2img";
  const body = { key: KEY, prompt, negative_prompt: COMMON_NEG, width: 768, height: 768, samples: 1, num_inference_steps: 25, guidance_scale: 7.5, safety_checker: "no", enhance_prompt: "yes", seed: 555 };
  if (model_id) body.model_id = model_id;
  const t0 = Date.now();
  const { http, j } = await post(url, body);
  const u = await resolve(j);
  let saved = false;
  if (u) saved = await download(u, path.join(OUT, `${tag}.png`));
  console.log(`${tag.padEnd(18)} ep=${ep} model=${model_id||"-"} http=${http} status=${j.status} saved=${saved} ${((Date.now()-t0)/1000).toFixed(0)}s ${u? "":"err="+JSON.stringify(j).slice(0,160)}`);
}
console.log("DONE modeltest");
