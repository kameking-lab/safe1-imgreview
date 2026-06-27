import fs from "node:fs"; import path from "node:path"; import { fileURLToPath } from "node:url";
import { KEY, COMMON_NEG, download } from "./mllib.mjs";
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(__dirname,"_modeltest"); fs.mkdirSync(OUT,{recursive:true});
const RAW="https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/master/gen_modelslab_v1";
const draft=`${RAW}/draft/01.png`, base=`${RAW}/base/0002.jpg`;
const prompt="flat 2D anime safety education illustration, KYT poster, clean line art and cel shading, full scene wide shot, a Japanese worker with chin-strap helmet hi-vis vest and full harness on a vertical scissor lift platform at an exhibition booth with aluminum truss and blank signboards, leaning over the guardrail losing balance and starting to fall, alarmed face, not a photograph";
async function post(u,b){const r=await fetch(u,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(b)});let j;try{j=JSON.parse(await r.text());}catch{j={status:"parse_err"};}return{http:r.status,j};}
async function resolve(j){if(j.status==="success"&&j.output?.length)return j.output[0];if(j.status==="processing"){const f=j.fetch_result||`https://modelslab.com/api/v6/realtime/fetch/${j.id}`;await new Promise(r=>setTimeout(r,Math.min((j.eta||8),30)*1000));for(let i=0;i<30;i++){const{j:fj}=await post(f,{key:KEY});if(fj.status==="success"&&fj.output?.length)return fj.output[0];if(fj.status==="failed"||fj.status==="error")return null;await new Promise(r=>setTimeout(r,5000));}}return null;}
const tests=[
 ["rt-cn-scribble-mid","https://modelslab.com/api/v6/realtime/controlnet",{model_id:"flat-2d-animerge",init_image:draft,control_image:draft,controlnet_model:"scribble",width:768,height:1024}],
 ["rt-cn-canny-mid","https://modelslab.com/api/v6/realtime/controlnet",{model_id:"flat-2d-animerge",init_image:draft,control_image:draft,controlnet_model:"canny",width:768,height:1024}],
 ["img-i2i-base-0.4-portrait","https://modelslab.com/api/v6/images/img2img",{model_id:"flat-2d-animerge",init_image:base,prompt_strength:0.4,width:768,height:1024}],
 ["img-t2i-portrait","https://modelslab.com/api/v6/images/text2img",{model_id:"flat-2d-animerge",width:768,height:1024}],
];
for(const[tag,url,extra]of tests){const body={key:KEY,prompt,negative_prompt:COMMON_NEG,samples:1,num_inference_steps:28,guidance_scale:7.5,safety_checker:"no",enhance_prompt:"yes",seed:777,...extra};
 const t0=Date.now();const{http,j}=await post(url,body);const u=await resolve(j);let s=false;if(u)s=await download(u,path.join(OUT,`${tag}.png`));
 console.log(`${tag.padEnd(28)} http=${http} status=${j.status} saved=${s} ${((Date.now()-t0)/1000).toFixed(0)}s ${u?"":"err="+JSON.stringify(j).slice(0,160)}`);}
console.log("DONE cn_test");
