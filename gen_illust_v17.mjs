// gen_illust_v17.mjs — 1事例(N01..N15)のベース写真を「事故事例イラスト」化（OpenAI+Google各1）。
// 使い方: node gen_illust_v17.mjs <N01..N15>
// base.png を参照入力に、構図/向き/接触点/機種/人数/PPEを保ち画風を安全教育イラストへ変換。
// キー値は出力しない。既存スキップ(再開安全)。削除/上書きしない。
import fs from "node:fs";
import path from "node:path";

const BASE = "C:/Users/kanet/20260522/safe1";
const N = (process.argv[2] || "").trim().toUpperCase();

// 機序・創作タイトル・設営文脈（gen_v16.mjs の MAP と整合）
const MAP = {
  N01:{cat:"TGL",title:"展示パネル積み下ろし中、昇降板からの墜落",mech:"a worker steps off a truck tail-gate lifter, misjudges the gap/step, and FALLS off the platform toward the ground"},
  N02:{cat:"TGL",title:"什器の積み下ろし中、昇降板と車体の間に足を挟まれ",mech:"a worker on the tail-gate lift platform gets a foot PINCHED between the rising lift gate and the truck body"},
  N03:{cat:"TGL",title:"パワーゲートでの荷役中、昇降板から転落しかけ",mech:"during cargo handling on a truck power-gate, the worker overbalances at the open edge and FALLS off the platform"},
  N04:{cat:"TGL",title:"台車を昇降装置へ移す際、台車が落下し下敷きに",mech:"a loaded cart tips/drops off the tail-gate lift and the worker is STRUCK and PINNED UNDER it"},
  N05:{cat:"TGL",title:"荷下ろし中、カゴ台車が倒れ作業員が転倒",mech:"a cargo roll-cage topples and the worker bracing it is KNOCKED DOWN to the ground"},
  N06:{cat:"高所",title:"会場天井付近の作業中、作業床手すりと上方構造物の間に挟まれ",mech:"a worker in an aerial work platform basket is PINCHED at the waist between the basket top rail and an overhead structure"},
  N07:{cat:"高所",title:"梁下を移動中、上方の梁と操作盤の間に挟まれ",mech:"the worker is PINCHED between an overhead beam and the platform control panel while moving"},
  N08:{cat:"高所",title:"養生ネットを外そうとしてバスケットから墜落",mech:"reaching to a beam, the worker's foot slips and he FALLS from the aerial work platform basket"},
  N09:{cat:"高所",title:"看板取付で身を乗り出し、作業床から墜落",mech:"leaning out over the guardrail too far, the worker FALLS from the aerial work platform floor"},
  N10:{cat:"高所",title:"作業床上昇中、操作盤フレームと天井の間に胸部を挟まれ",mech:"raising the platform into a ceiling step, the worker's chest is PINCHED between the control-panel frame and the ceiling"},
  N11:{cat:"高所",title:"バスケットから移ろうとして墜落",mech:"transferring from the basket to an adjacent structure, the worker FALLS several meters to the ground"},
  N12:{cat:"高所",title:"傾斜地で旋回中、機体がバランスを崩し転倒",mech:"on sloped ground the whole aerial work platform TIPS OVER while slewing, throwing the worker"},
  N13:{cat:"高所",title:"手すりに足をかけたダクト取付中に墜落",mech:"with a foot on the basket rail, the worker loses balance and FALLS from the aerial work platform"},
  N14:{cat:"高所",title:"外周作業で作業床から身を出し、高所から墜落",mech:"climbing out of the platform to check, the worker loses balance and FALLS from height"},
  N15:{cat:"高所",title:"低い梁下を移動中、下がり壁と手すりの間に挟まれ",mech:"driving under a low beam, the worker is PINCHED between a hanging wall/low beam and the platform handrail"},
};
const m = MAP[N];
if (!m) { console.error("usage: node gen_illust_v17.mjs <N01..N15>"); process.exit(2); }

function readEnv(){const o={};const p=path.join(BASE,".env");if(!fs.existsSync(p))return o;
  for(const ln of fs.readFileSync(p,"utf8").split(/\r?\n/)){const mm=ln.match(/^([A-Z0-9_]+)=(.*)$/);if(mm)o[mm[1]]=mm[2];}return o;}
const ENV=readEnv();
const OPENAI=ENV.OPENAI_API_KEY||process.env.OPENAI_API_KEY||"";
const GEMINI=ENV.GEMINI_API_KEY||process.env.GEMINI_API_KEY||"";
if(!OPENAI||!GEMINI){console.error("キー未設定");process.exit(3);}

const SRC=path.join(BASE,"photos_v16",N,"base.png");
if(!fs.existsSync(SRC)){console.error("base.png 無し:",SRC);process.exit(4);}
const OUT=path.join(BASE,"illust_v17",N); fs.mkdirSync(OUT,{recursive:true});

const isA=m.cat!=="TGL";
const PPE="Japanese worker(s), hard hat WITH CHIN STRAP, hi-vis vest, safety boots"+(isA?", FULL-BODY SAFETY HARNESS":"")+". Japanese-spec equipment (NOT an excavator). NO company logos, NO readable text, NO blood/gore.";
const machine=isA?"a Japanese aerial work platform / MEWP (boom or scissor lift with a work basket)":"a Japanese truck with a TAIL-GATE LIFTER / power-gate (rear lift platform)";
const STYLE="Render as a CLEAN JAPANESE OCCUPATIONAL-SAFETY HAZARD ILLUSTRATION (KYT training / safety-poster style): flat vector / flat-color illustration with clean outlines, simple shading, allowed warning accents (a red X mark or red arrow and impact/motion lines to emphasize the danger). This is an ILLUSTRATION, NOT a photo.";
const MOMENT="Depict the ACCIDENT MOMENT UNAMBIGUOUSLY: the person is CLEARLY falling / tipping / being pinched (center of mass past the edge, body being thrown out, limbs flailing) — NOT a stable, balanced working pose. Make it obvious that the hazard is HAPPENING.";
const PROMPT=`${STYLE} Keep the SAME composition, direction of force, contact point, machine type (${machine}), number of people and PPE as the reference image, but convert the art style to the illustration described. Accident to depict: ${m.mech}. ${MOMENT} Setting: a Japanese exhibition/event build-up venue. ${PPE} Single frame, no collage.`;

const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const OAI=["gpt-image-2","gpt-image-1"];
async function genOpenAI(){let last="";for(const model of OAI){for(let a=0;a<4;a++){try{
  const fd=new FormData();fd.append("model",model);
  fd.append("image",new Blob([fs.readFileSync(SRC)],{type:"image/png"}),"ref.png");
  fd.append("prompt",PROMPT);fd.append("size","1024x1024");fd.append("quality","high");fd.append("n","1");
  const r=await fetch("https://api.openai.com/v1/images/edits",{method:"POST",headers:{Authorization:`Bearer ${OPENAI}`},body:fd});
  if(r.status===429||r.status>=500){last=`http ${r.status}`;await sleep(2000*2**a);continue;}
  const j=await r.json();if(j?.data?.[0]?.b64_json)return{b64:j.data[0].b64_json,model};
  const em=j?.error?.message||JSON.stringify(j).slice(0,180);last=em;
  if(/model/i.test(em)&&/not|exist|unknown|invalid/i.test(em))break;await sleep(1500*2**a);
}catch(e){last=e.message;await sleep(1500*2**a);}}}throw new Error("openai: "+last);}
const G=["gemini-3-pro-image-preview","gemini-2.5-flash-image"];
async function genGoogle(){const refB64=fs.readFileSync(SRC).toString("base64");let last="";
for(const model of G){for(let a=0;a<4;a++){try{
  const body={contents:[{parts:[{text:PROMPT},{inline_data:{mime_type:"image/png",data:refB64}}]}],generationConfig:{responseModalities:["IMAGE"]}};
  const r=await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`,{method:"POST",headers:{"Content-Type":"application/json","x-goog-api-key":GEMINI},body:JSON.stringify(body)});
  if(r.status===429||r.status>=500){last=`http ${r.status}`;await sleep(3000*2**a);continue;}
  const j=await r.json();const parts=j?.candidates?.[0]?.content?.parts||[];
  const img=parts.find(p=>p.inlineData?.data||p.inline_data?.data);
  if(img)return{b64:(img.inlineData||img.inline_data).data,model};
  const em=j?.error?.message||JSON.stringify(j).slice(0,180);last=em;
  if(/model/i.test(em)&&/not|found|unknown|invalid|support/i.test(em))break;await sleep(2000*2**a);
}catch(e){last=e.message;await sleep(2000*2**a);}}}throw new Error("google: "+last);}

const metaP=path.join(OUT,"gen_meta.json");
const meta=fs.existsSync(metaP)?JSON.parse(fs.readFileSync(metaP,"utf8")):{N,cat:m.cat,title:m.title,openai_model:null,google_model:null,results:{}};
let ok=0,fail=0;
for(const [file,fn] of [["openai_illust.png",genOpenAI],["google_illust.png",genGoogle]]){
  const out=path.join(OUT,file);
  if(fs.existsSync(out)&&fs.statSync(out).size>4000){console.log("skip",N,file);ok++;continue;}
  try{const res=await fn();fs.writeFileSync(out,Buffer.from(res.b64,"base64"));
    if(file.startsWith("openai"))meta.openai_model=res.model;else meta.google_model=res.model;
    meta.results[file]={ok:true,model:res.model};console.log("saved",N,file,"("+res.model+")");ok++;
  }catch(e){meta.results[file]={ok:false,error:String(e.message).slice(0,180)};console.error("FAIL",N,file,"-",String(e.message).slice(0,140));fail++;}
  fs.writeFileSync(metaP,JSON.stringify(meta,null,2));
}
console.log(`DONE ${N} ok=${ok} fail=${fail}`);
process.exit(0);
