// gen_event_v23.mjs — 元絵を参照画像にして、Opusが1枚ずつ読込分析して書いた「専用プロンプト」(prompts_v23/<番号>.txt)で
//   安全教育用イラストを Google gemini-3-pro-image-preview のみで2枚生成する（OpenAI 不使用・矢印/文字なし）。
// 使い方: node gen_event_v23.mjs <baseNum> [retry]
//   ・プロンプトは prompts_v23/<baseNum>.txt から読み込む（汎用文字列をスクリプトに焼き込まない）。
//   ・参照画像は collect_aerial2/aerial2_index.csv の 通し番号→ファイル名 を引き collect_aerial2/img/<file>。
//   ・出力: gen_event_v23/<baseNum>/{google_1,google_2}.png （既存>4KBは skip＝再開安全・非破壊）。
//   ・retry を付けると再生成用に google_1b/google_2b.png（新ファイル名・上書きしない）へ出力。
// キー値は出力しない(.env から読む)。削除/上書き/Chrome killしない。OpenAI 経路は持たない。
import fs from "node:fs";
import path from "node:path";

const BASE = "C:/Users/kanet/20260522/safe1";
const baseNum = String(process.argv[2]||"").trim();
const RETRY = String(process.argv[3]||"").trim().toLowerCase()==="retry";
if(!baseNum){console.error("usage: node gen_event_v23.mjs <baseNum> [retry]");process.exit(2);}

function readEnv(){const o={};const p=path.join(BASE,".env");if(!fs.existsSync(p))return o;
  for(const ln of fs.readFileSync(p,"utf8").split(/\r?\n/)){const m=ln.match(/^([A-Z0-9_]+)=(.*)$/);if(m)o[m[1]]=m[2];}return o;}
const ENV=readEnv();
const GEMINI=ENV.GEMINI_API_KEY||process.env.GEMINI_API_KEY||"";
if(!GEMINI){console.error("GEMINI_API_KEY 未設定(.env)");process.exit(3);}
const sleep=ms=>new Promise(r=>setTimeout(r,ms));

// ---- CSV パース（ダブルクオート対応・最小実装） ----
function parseCsvLine(line){const out=[];let cur="",q=false;
  for(let i=0;i<line.length;i++){const c=line[i];
    if(q){ if(c==='"'){ if(line[i+1]==='"'){cur+='"';i++;} else q=false; } else cur+=c; }
    else { if(c===','){out.push(cur);cur="";} else if(c==='"'){q=true;} else cur+=c; } }
  out.push(cur);return out;}
const csvPath=path.join(BASE,"collect_aerial2/aerial2_index.csv");
const lines=fs.readFileSync(csvPath,"utf8").split(/\r?\n/).filter(Boolean);
const header=parseCsvLine(lines[0]);
const idx=k=>header.indexOf(k);
let row=null;
for(let i=1;i<lines.length;i++){const c=parseCsvLine(lines[i]);if(String(c[idx("通し番号")]).trim()===baseNum){row=c;break;}}
if(!row){console.error(`該当なし: 通し番号 ${baseNum} は CSV に存在しません`);process.exit(4);}
const refFile=row[idx("ファイル名")].trim();
const accType=row[idx("カテゴリ")].trim();
const refPath=path.join(BASE,"collect_aerial2/img",refFile);
if(!fs.existsSync(refPath)){console.error(`該当なし: 参照画像 ${refFile} が見つかりません`);process.exit(4);}

// ---- 専用プロンプト（Opusが元絵を読んで書いたもの）を txt から読み込む（焼き込み禁止） ----
const promptPath=path.join(BASE,"prompts_v23",`${baseNum}.txt`);
if(!fs.existsSync(promptPath)){console.error(`該当なし: 専用プロンプト ${promptPath} が見つかりません（先に prompts_v23/${baseNum}.txt を作成）`);process.exit(5);}
const PROMPT=fs.readFileSync(promptPath,"utf8").trim();
if(PROMPT.length<200){console.error(`専用プロンプトが短すぎます: ${promptPath}`);process.exit(5);}

// ---- 参照画像 ----
const refBuf=fs.readFileSync(refPath);
const refMime=refFile.toLowerCase().endsWith(".png")?"image/png":refFile.toLowerCase().endsWith(".webp")?"image/webp":refFile.toLowerCase().endsWith(".gif")?"image/gif":"image/jpeg";

async function genGoogle(prompt){
  const model="gemini-3-pro-image-preview";let last="";
  for(let a=0;a<4;a++){try{
    const body={contents:[{parts:[{inlineData:{mimeType:refMime,data:refBuf.toString("base64")}},{text:prompt}]}],generationConfig:{responseModalities:["IMAGE"]}};
    const r=await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`,{method:"POST",headers:{"Content-Type":"application/json","x-goog-api-key":GEMINI},body:JSON.stringify(body)});
    if(r.status===429||r.status>=500){last=`http ${r.status}`;await sleep(3500*2**a);continue;}
    const j=await r.json();const parts=j?.candidates?.[0]?.content?.parts||[];
    const img=parts.find(p=>p.inlineData?.data||p.inline_data?.data);
    if(img)return(img.inlineData||img.inline_data).data;
    last=j?.error?.message||JSON.stringify(j).slice(0,200);
    if(/RESOURCE_EXHAUSTED|quota|rate/i.test(last)){console.error("RATE/QUOTA:",last.slice(0,120));await sleep(4000*2**a);continue;}
    await sleep(2500*2**a);
  }catch(e){last=e.message;await sleep(2500*2**a);}}
  throw new Error("google: "+last);
}

// 2案は同一の専用プロンプトから生成（サンプリングで自然に異なる2枚になる）。
// 焼き込み禁止のため、汎用文字列の付加はしない。プロンプトは prompts_v23 のみが真実。
const outDir=path.join(BASE,"gen_event_v23",baseNum);
fs.mkdirSync(outDir,{recursive:true});
const sfx=RETRY?"b":"";
const jobs=[
  {name:`google_1${sfx}.png`,fn:()=>genGoogle(PROMPT)},
  {name:`google_2${sfx}.png`,fn:()=>genGoogle(PROMPT)},
];
let ok=0,failed=[];
for(const j of jobs){
  const out=path.join(outDir,j.name);
  if(fs.existsSync(out)&&fs.statSync(out).size>4000){console.log("skip(exists)",out);ok++;continue;}
  try{const b64=await j.fn();fs.writeFileSync(out,Buffer.from(b64,"base64"));console.log("saved",out);ok++;}
  catch(e){console.error("FAIL",j.name,"-",String(e.message).slice(0,160));failed.push(j.name);}
}
console.log(`DONE base=${baseNum} type=${accType} ref=${refFile} retry=${RETRY} promptChars=${PROMPT.length} ok=${ok}/2 failed=${failed.join(",")||"none"}`);
process.exit(failed.length?1:0);
