// gen_v16.mjs — 1事例(N01..N15)のリアル化3枚(base/openai/google)を生成。
// 使い方: node gen_v16.mjs <N01..N15>
// 採用画像(photos_v15/{old}/{adopt}.png)を参照入力に、リアル化＋イベント設営の創作事故へ寄せる。
// キー値は出力しない。既存スキップ(再開安全)。削除/上書きしない。
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";

const BASE = "C:/Users/kanet/20260522/safe1";
const N = (process.argv[2] || "").trim().toUpperCase();

// 新No -> {old, adopt, cat, title(創作), mech(機序), event(設営文脈), fix(補正)}
const MAP = {
  N01:{old:"0001",adopt:"A_openai",cat:"TGL",title:"展示パネル積み下ろし中、昇降板からの墜落",
       mech:"a worker stepping off a truck tail-gate lifter (rear lift platform) misjudges the gap/step between the truck bed and the lift and loses balance, falling toward the ground",
       event:"unloading EXHIBITION PANELS/display fixtures from a truck tail-gate lifter at an event hall loading bay"},
  N02:{old:"0002",adopt:"A_openai",cat:"TGL",title:"什器の積み下ろし中、昇降板と車体の間に足を挟まれ",
       mech:"a worker standing on the tail-gate lift platform operates it and gets a foot pinched between the rising lift gate and the truck body",
       event:"loading exhibition fixtures with a truck tail-gate lifter at a venue loading dock"},
  N03:{old:"0003",adopt:"D_google_event",cat:"TGL",title:"パワーゲートでの荷役中、昇降板から転落しかけ",
       mech:"during cargo handling on a truck power-gate (tail-gate lifter), the worker on the platform overbalances at the open edge and nearly falls off",
       event:"handling event cargo on a truck power-gate at an exhibition hall"},
  N04:{old:"0017",adopt:"D_google_event",cat:"TGL",title:"台車を昇降装置へ移す際、台車が落下し下敷きに",
       mech:"while moving a loaded cart from the truck bed onto the tail-gate lift, the cart tips/drops off the platform and the worker is struck/pinned under it",
       event:"transferring a loaded display cart onto a truck tail-gate lifter at a venue"},
  N05:{old:"0019",adopt:"C_openai_event",cat:"TGL",title:"荷下ろし中、カゴ台車が倒れ作業員が転倒",
       mech:"during unloading, a cargo roll-cage on the truck bed collides with another cart, topples, and the worker bracing it is knocked down",
       event:"unloading roll-cages of exhibition materials at an event loading bay"},
  N06:{old:"0040",adopt:"C_openai_event",cat:"高所",title:"会場天井付近の作業中、作業床手すりと上方構造物の間に挟まれ",
       mech:"a worker in an aerial work platform basket is pinched at the waist between the basket top rail and an overhead structure (ceiling rail/beam) as the basket moves",
       event:"overhead work at an exhibition hall (ceiling rail/truss) using an aerial work platform"},
  N07:{old:"0042",adopt:"D_google_event",cat:"高所",title:"梁下を移動中、上方の梁と操作盤の間に挟まれ",
       mech:"moving an aerial work platform under an overhead beam, the worker is pinched between the overhead beam and the platform control panel",
       event:"moving an aerial work platform under a ceiling beam/truss at a venue"},
  N08:{old:"0043",adopt:"D_google_event",cat:"高所",title:"養生ネットを外そうとしてバスケットから墜落",
       mech:"trying to free a snagged sheet/net by reaching to a beam, the worker steps on the basket rail, foot slips and falls from the aerial work platform basket",
       event:"removing snagged rigging/sheet near a truss from an aerial work platform at a venue"},
  N09:{old:"0044",adopt:"D_google_event",cat:"高所",title:"看板取付で身を乗り出し、作業床から墜落",
       mech:"reaching out and leaning over the guardrail too far during fixing work, the worker falls from the aerial work platform work floor",
       event:"fixing venue signage while leaning out of an aerial work platform"},
  N10:{old:"0046",adopt:"D_google_event",cat:"高所",title:"作業床上昇中、操作盤フレームと天井の間に胸部を挟まれ",
       mech:"raising the platform without noticing a ceiling step, the worker's chest is pinched between the control-panel frame and the ceiling",
       event:"installing ceiling ductwork/lighting from an aerial work platform at a hall"},
  N11:{old:"0050",adopt:"D_google_event",cat:"高所",title:"バスケットから移ろうとして墜落",
       mech:"trying to transfer from the aerial platform basket to an adjacent structure, the worker falls a few meters to the ground",
       event:"transferring from an aerial work platform basket near booth/structure at a venue"},
  N12:{old:"0052",adopt:"D_google_event",cat:"高所",title:"傾斜地で旋回中、機体がバランスを崩し転倒",
       mech:"on sloped ground, swinging the boom left, the aerial work platform loses balance and the whole machine tips over",
       event:"outdoor venue ground; aerial work platform tipping over while slewing on a slope"},
  N13:{old:"0054",adopt:"D_google_event",cat:"高所",title:"手すりに足をかけたダクト取付中に墜落",
       mech:"with a foot on the basket guardrail during overhead duct fixing, the worker loses balance and falls from the aerial work platform",
       event:"installing ceiling ducts/equipment from an aerial work platform at a venue"},
  N14:{old:"0057",adopt:"C_openai_event",cat:"高所",title:"外周作業で作業床から身を出し、高所から墜落",
       mech:"the work floor contacts a facade and the worker climbs out of the platform to check, loses balance and falls from height",
       event:"facade/perimeter work at a venue using an aerial work platform"},
  N15:{old:"0071",adopt:"C_openai_event",cat:"高所",title:"低い梁下を移動中、下がり壁と手すりの間に挟まれ",
       mech:"driving the aerial work platform through a low opening, the worker is pinched between a hanging wall/low beam and the platform handrail",
       event:"moving an aerial work platform under a low hanging beam in a venue basement/back area"},
};
const m = MAP[N];
if (!m) { console.error("usage: node gen_v16.mjs <N01..N15>"); process.exit(2); }

function readEnv(){const o={};const p=path.join(BASE,".env");if(!fs.existsSync(p))return o;
  for(const ln of fs.readFileSync(p,"utf8").split(/\r?\n/)){const mm=ln.match(/^([A-Z0-9_]+)=(.*)$/);if(mm)o[mm[1]]=mm[2];}return o;}
const ENV=readEnv();
const OPENAI=ENV.OPENAI_API_KEY||process.env.OPENAI_API_KEY||"";
const GEMINI=ENV.GEMINI_API_KEY||process.env.GEMINI_API_KEY||"";
if(!OPENAI||!GEMINI){console.error("キー未設定");process.exit(3);}

const OUT=path.join(BASE,"photos_v16",N); fs.mkdirSync(OUT,{recursive:true});
const SRCADOPT=path.join(BASE,"photos_v15",m.old,m.adopt+".png");
const BASEPNG=path.join(OUT,"base.png");
if(!fs.existsSync(BASEPNG)){
  const code=`from PIL import Image
im=Image.open(r"${SRCADOPT}").convert("RGB")
w,h=im.size; s=1024/max(w,h)
if s<1: im=im.resize((max(1,int(w*s)),max(1,int(h*s))))
im.save(r"${BASEPNG}")
print("ok")`;
  execFileSync("py",["-c",code],{stdio:"pipe"});
}

const isA=m.cat!=="TGL";
const PPE="Japanese male worker(s) at a real Japanese exhibition/event build-up venue, hard hat WITH CHIN STRAP, hi-vis vest/work clothes, safety boots"+(isA?", and a FULL-BODY SAFETY HARNESS":"")+". Japanese-spec equipment (NOT an excavator). NO company logos, NO readable text/signage, NO blood/gore. The dangerous MOMENT of the accident.";
const machine=isA?"a Japanese aerial work platform / MEWP (boom or scissor lift with a work basket)":"a Japanese truck with a TAIL-GATE LIFTER / power-gate (rear lift platform)";
const PROMPT=`A photorealistic documentary photograph (natural light, realistic textures, shallow depth of field, candid cluttered real worksite) of a workplace accident at a Japanese EXHIBITION / EVENT set-up venue. Scene: ${m.event}. Accident: ${m.mech}. Keep the same composition, direction of force, contact point and machine type (${machine}) as a safety re-enactment. Correct any unnatural anatomy/hands, wrong machine, physics inconsistency or missing PPE from the reference; make it physically plausible and natural. ${PPE} Single frame, no collage, no text.`;

const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const OAI=["gpt-image-2","gpt-image-1"];
async function genOpenAI(){let last="";for(const model of OAI){for(let a=0;a<4;a++){try{
  const fd=new FormData();fd.append("model",model);
  fd.append("image",new Blob([fs.readFileSync(BASEPNG)],{type:"image/png"}),"ref.png");
  fd.append("prompt",PROMPT);fd.append("size","1024x1024");fd.append("quality","high");fd.append("n","1");
  const r=await fetch("https://api.openai.com/v1/images/edits",{method:"POST",headers:{Authorization:`Bearer ${OPENAI}`},body:fd});
  if(r.status===429||r.status>=500){last=`http ${r.status}`;await sleep(2000*2**a);continue;}
  const j=await r.json();if(j?.data?.[0]?.b64_json)return{b64:j.data[0].b64_json,model};
  const em=j?.error?.message||JSON.stringify(j).slice(0,180);last=em;
  if(/model/i.test(em)&&/not|exist|unknown|invalid/i.test(em))break;await sleep(1500*2**a);
}catch(e){last=e.message;await sleep(1500*2**a);}}}throw new Error("openai: "+last);}
const G=["gemini-3-pro-image-preview","gemini-2.5-flash-image"];
async function genGoogle(){const refB64=fs.readFileSync(BASEPNG).toString("base64");let last="";
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
const meta=fs.existsSync(metaP)?JSON.parse(fs.readFileSync(metaP,"utf8")):{N,old:m.old,adopt:m.adopt,cat:m.cat,title:m.title,openai_model:null,google_model:null,results:{}};
let ok=1,fail=0; // base counts as ok
for(const [file,fn] of [["openai.png",genOpenAI],["google.png",genGoogle]]){
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
