// gen_img.mjs — テキスト→画像 1枚生成（OpenAI gpt-image-2 / Google Nano Banana Pro）。
// 使い方: node gen_img.mjs <openai|google> <out.png> "<prompt>" [transparent]
//  - transparent 指定かつ openai のときは背景透過PNGをネイティブ生成（gpt-image-2 background=transparent）。
//  - google は透過非対応のため不透過生成（パーツは純白背景で生成→ cutout_white.py で後処理）。
// キー値は出力しない。既存スキップ(再開安全)。削除/上書きしない（出力先が既にあれば skip）。
import fs from "node:fs";
import path from "node:path";

const BASE = "C:/Users/kanet/20260522/safe1";
const provider = (process.argv[2]||"").toLowerCase();
const out = process.argv[3];
const prompt = process.argv[4]||"";
const transparent = (process.argv[5]||"").toLowerCase()==="transparent";
if(!["openai","google"].includes(provider)||!out||!prompt){console.error('usage: node gen_img.mjs <openai|google> <out.png> "<prompt>" [transparent]');process.exit(2);}

function readEnv(){const o={};const p=path.join(BASE,".env");if(!fs.existsSync(p))return o;
  for(const ln of fs.readFileSync(p,"utf8").split(/\r?\n/)){const m=ln.match(/^([A-Z0-9_]+)=(.*)$/);if(m)o[m[1]]=m[2];}return o;}
const ENV=readEnv();
const OPENAI=ENV.OPENAI_API_KEY||process.env.OPENAI_API_KEY||"";
const GEMINI=ENV.GEMINI_API_KEY||process.env.GEMINI_API_KEY||"";
if(provider==="openai"&&!OPENAI){console.error("キー未設定(OPENAI)");process.exit(3);}
if(provider==="google"&&!GEMINI){console.error("キー未設定(GEMINI)");process.exit(3);}

if(fs.existsSync(out)&&fs.statSync(out).size>4000){console.log("skip(exists)",out);process.exit(0);}
fs.mkdirSync(path.dirname(out),{recursive:true});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));

async function genOpenAI(){
  const OAI=["gpt-image-2","gpt-image-1"];let last="";
  for(const model of OAI){for(let a=0;a<4;a++){try{
    const body={model,prompt,size:"1024x1024",quality:"high",n:1};
    if(transparent) body.background="transparent";
    const r=await fetch("https://api.openai.com/v1/images/generations",{method:"POST",headers:{Authorization:`Bearer ${OPENAI}`,"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(r.status===429||r.status>=500){last=`http ${r.status}`;await sleep(2500*2**a);continue;}
    const j=await r.json();if(j?.data?.[0]?.b64_json)return{b64:j.data[0].b64_json,model};
    const em=j?.error?.message||JSON.stringify(j).slice(0,180);last=em;
    if(/model/i.test(em)&&/not|exist|unknown|invalid/i.test(em))break;
    if(/background/i.test(em)){delete body.background;} await sleep(1500*2**a);
  }catch(e){last=e.message;await sleep(1500*2**a);}}}
  throw new Error("openai: "+last);
}
async function genGoogle(){
  const G=["gemini-3-pro-image-preview","gemini-2.5-flash-image"];let last="";
  for(const model of G){for(let a=0;a<4;a++){try{
    const body={contents:[{parts:[{text:prompt}]}],generationConfig:{responseModalities:["IMAGE"]}};
    const r=await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`,{method:"POST",headers:{"Content-Type":"application/json","x-goog-api-key":GEMINI},body:JSON.stringify(body)});
    if(r.status===429||r.status>=500){last=`http ${r.status}`;await sleep(3000*2**a);continue;}
    const j=await r.json();const parts=j?.candidates?.[0]?.content?.parts||[];
    const img=parts.find(p=>p.inlineData?.data||p.inline_data?.data);
    if(img)return{b64:(img.inlineData||img.inline_data).data,model};
    const em=j?.error?.message||JSON.stringify(j).slice(0,180);last=em;
    if(/model/i.test(em)&&/not|found|unknown|invalid|support/i.test(em))break;await sleep(2000*2**a);
  }catch(e){last=e.message;await sleep(2000*2**a);}}}
  throw new Error("google: "+last);
}
try{
  const res = provider==="openai" ? await genOpenAI() : await genGoogle();
  fs.writeFileSync(out,Buffer.from(res.b64,"base64"));
  console.log("saved",out,"("+res.model+")");
  process.exit(0);
}catch(e){console.error("FAIL",out,"-",String(e.message).slice(0,160));process.exit(1);}
