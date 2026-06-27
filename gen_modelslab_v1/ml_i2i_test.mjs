/** ml_i2i_test.mjs — images endpoint で img2img / controlnet(scribble,canny) を flat-2d-animerge + 下書きrawURLで検証。 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { KEY, COMMON_NEG, download } from "./mllib.mjs";
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(__dirname, "_modeltest"); fs.mkdirSync(OUT, { recursive: true });
const RAW = "https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/master/gen_modelslab_v1";
const draft = `${RAW}/draft/01.png`;
const base  = `${RAW}/base/0002.jpg`;
const prompt = "flat 2D anime safety education illustration, KYT poster, clean line art and cel shading, Japanese worker with chin-strap helmet, hi-vis vest and full harness on a vertical scissor lift platform at an exhibition booth with aluminum truss, leaning over the guardrail losing balance and starting to fall, alarmed face, blank signboards, not a photograph";
async function post(url, body) { const r = await fetch(url, { method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(body)});
  let j; try{ j=JSON.parse(await r.text()); }catch{ j={status:"parse_err"};} return {http:r.status,j}; }
async function resolve(j){ if(j.status==="success"&&j.output?.length) return j.output[0];
  if(j.status==="processing"){ const f=j.fetch_result||`https://modelslab.com/api/v6/realtime/fetch/${j.id}`; await new Promise(r=>setTimeout(r,Math.min((j.eta||8),30)*1000));
    for(let i=0;i<30;i++){ const {j:fj}=await post(f,{key:KEY}); if(fj.status==="success"&&fj.output?.length) return fj.output[0]; if(fj.status==="failed"||fj.status==="error") return null; await new Promise(r=>setTimeout(r,5000)); } } return null; }
// raw 到達確認
for (const u of [draft, base]) { const r = await fetch(u, {method:"HEAD"}); console.log("RAW", r.status, u.split("/").pop()); }
const tests = [
  ["images-i2i-draft-0.65", "https://modelslab.com/api/v6/images/img2img", { model_id:"flat-2d-animerge", init_image:draft, prompt_strength:0.65 }],
  ["images-i2i-base-0.5",   "https://modelslab.com/api/v6/images/img2img", { model_id:"flat-2d-animerge", init_image:base,  prompt_strength:0.5 }],
  ["images-cn-scribble",    "https://modelslab.com/api/v6/images/controlnet", { model_id:"flat-2d-animerge", init_image:draft, control_image:draft, controlnet_model:"scribble" }],
  ["images-cn-canny",       "https://modelslab.com/api/v6/images/controlnet", { model_id:"flat-2d-animerge", init_image:draft, control_image:draft, controlnet_model:"canny" }],
];
for (const [tag, url, extra] of tests) {
  const body = { key:KEY, prompt, negative_prompt:COMMON_NEG, width:768, height:768, samples:1, num_inference_steps:25, guidance_scale:7.5, safety_checker:"no", enhance_prompt:"yes", seed:777, ...extra };
  const t0=Date.now(); const {http,j}=await post(url, body); const u=await resolve(j);
  let saved=false; if(u) saved=await download(u, path.join(OUT,`${tag}.png`));
  console.log(`${tag.padEnd(24)} http=${http} status=${j.status} saved=${saved} ${((Date.now()-t0)/1000).toFixed(0)}s ${u?"":"err="+JSON.stringify(j).slice(0,200)}`);
}
console.log("DONE i2i_test");
