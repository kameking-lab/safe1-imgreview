import fs from "node:fs"; import path from "node:path"; import { fileURLToPath } from "node:url";
import { KEY, COMMON_NEG, download } from "./mllib.mjs";
const __dirname=path.dirname(fileURLToPath(import.meta.url)); const OUT=path.join(__dirname,"_modeltest"); fs.mkdirSync(OUT,{recursive:true});
const RAW="https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/master/gen_modelslab_v1";
const prompt="clean flat illustration, safety education KYT poster art style, a Japanese worker with chin-strap helmet hi-vis vest full harness on a vertical scissor lift platform at an exhibition booth with aluminum truss, leaning over the guardrail losing balance and beginning to fall, alarmed face, not a photograph, illustration, anime style, cel shading";
async function post(u,b){const r=await fetch(u,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(b)});let j;try{j=JSON.parse(await r.text());}catch{j={status:"parse_err"};}return{http:r.status,j};}
async function resolve(j){if(j.status==="success"&&j.output?.length)return j.output[0];if(j.status==="processing"){const f=j.fetch_result||`https://modelslab.com/api/v6/realtime/fetch/${j.id}`;await new Promise(r=>setTimeout(r,Math.min((j.eta||8),30)*1000));for(let i=0;i<30;i++){const{j:fj}=await post(f,{key:KEY});if(fj.status==="success"&&fj.output?.length)return fj.output[0];if(fj.status==="failed"||fj.status==="error")return null;await new Promise(r=>setTimeout(r,5000));}}return null;}
const tests=[
 ["rt-i2i-base0002-0.55",`${RAW}/base/0002.jpg`,0.55],
 ["rt-i2i-base0215-0.55",`${RAW}/base/0215.jpg`,0.55],
 ["rt-i2i-draft01-0.6",`${RAW}/draft/01.png`,0.6],
 ["rt-i2i-draft01-0.4",`${RAW}/draft/01.png`,0.4],
];
for(const[tag,init,ps]of tests){const body={key:KEY,prompt,negative_prompt:COMMON_NEG,init_image:init,prompt_strength:ps,width:768,height:1024,samples:1,num_inference_steps:28,guidance_scale:8,safety_checker:"no",enhance_prompt:false,seed:777};
 const t0=Date.now();const{http,j}=await post("https://modelslab.com/api/v6/realtime/img2img",body);const u=await resolve(j);let s=false;if(u)s=await download(u,path.join(OUT,`${tag}.png`));
 console.log(`${tag.padEnd(26)} http=${http} status=${j.status} saved=${s} ${((Date.now()-t0)/1000).toFixed(0)}s ${u?"":"err="+JSON.stringify(j).slice(0,140)}`);}
console.log("DONE rt_i2i");
