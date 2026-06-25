// gen_event_v20.mjs — aerial2 元絵を参照画像にして「展示会場ブース設営中の事故」イラストを4枚生成。
//   OpenAI gpt-image-2 quality=high x2 (images/edits・参照画像つき) + Google gemini-3-pro-image-preview x2 (generateContent inlineData)。
// 使い方: node gen_event_v20.mjs <baseNum>
//   collect_aerial2/aerial2_index.csv から baseNum の ファイル名/事故の型 を引き、collect_aerial2/img/<file> を参照画像として渡す。
//   出力: gen_event_v20/<baseNum>/{openai_1,openai_2,google_1,google_2}.png （既存>4KBは skip＝再開安全・非破壊）。
//   event_index_v20.csv に1行追記（既存行があれば追記しない）。
// キー値は出力しない(.env から読む)。削除/上書き/Chrome killしない。
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";

const BASE = "C:/Users/kanet/20260522/safe1";
const baseNum = String(process.argv[2]||"").trim();
if(!baseNum){console.error("usage: node gen_event_v20.mjs <baseNum>");process.exit(2);}

function readEnv(){const o={};const p=path.join(BASE,".env");if(!fs.existsSync(p))return o;
  for(const ln of fs.readFileSync(p,"utf8").split(/\r?\n/)){const m=ln.match(/^([A-Z0-9_]+)=(.*)$/);if(m)o[m[1]]=m[2];}return o;}
const ENV=readEnv();
const OPENAI=ENV.OPENAI_API_KEY||process.env.OPENAI_API_KEY||"";
const GEMINI=ENV.GEMINI_API_KEY||process.env.GEMINI_API_KEY||"";
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
const memo=row[idx("状況メモ")].trim();
const domain=row[idx("出所ドメイン")].trim();
const refPath=path.join(BASE,"collect_aerial2/img",refFile);
if(!fs.existsSync(refPath)){console.error(`該当なし: 参照画像 ${refFile} が見つかりません`);process.exit(4);}

// ---- 統一スタイル + 事故の型ごとの瞬間描写 ----
const STYLE=[
 "High-quality, realistic Japanese workplace-safety educational illustration (clean professional vector-style art with rich shading, depth and a sense of presence). Do NOT imitate the source picture's drawing style; only inherit its accident type, composition and who-gets-injured.",
 "Setting: a JAPANESE EXHIBITION HALL / trade-show booth SETUP site (half-built exhibition booths, aluminium truss frames, large blank signage panels, display fixtures, cardboard crates, a loading dock in the background).",
 "Workers: Japanese exhibition crew wearing chin-strap helmets, hi-vis vests, work gloves and safety boots; when working at height they wear a full-body safety harness.",
 "Any aerial work platform MUST be a SCISSOR LIFT only (vertical scissor-type elevating platform). Never a boom lift or truck-mounted boom.",
 "Show the ACCIDENT MOMENT / the danger actually happening (not a calm normal-work scene).",
 "Absolutely NO text, NO letters, NO numbers, NO arrows, NO captions, NO speech bubbles, NO symbols anywhere in the image. No blood/gore. No real brand names or real logos.",
].join(" ");
const TYPE_SCENE={
 "墜落・転落":"Accident type: FALL FROM HEIGHT. A booth-setup worker falls/tumbles down from the elevated platform of a scissor lift (or from the half-built booth structure) at the exhibition hall.",
 "挟まれ":"Accident type: CAUGHT-IN / CRUSHED. A worker's body or hand gets caught/pinched between the scissor lift's moving scissor mechanism or between heavy booth panels/fixtures.",
 "転倒・横転":"Accident type: TIP-OVER / OVERTURN. The scissor lift loses balance and tips/overturns, or a worker trips and falls, on the exhibition-hall floor during booth setup.",
 "不安全行動":"Accident type: UNSAFE ACT. A worker performs a dangerous unsafe action (overreaching far out of the scissor-lift platform, standing on the guardrail, no harness) and is about to fall during booth setup.",
 "感電":"Accident type: ELECTRIC SHOCK. A worker handling exhibition lighting/power wiring on a scissor lift receives an electric shock while setting up the booth.",
 "飛来・落下":"Accident type: FALLING / FLYING OBJECT. A tool, truss bar or signage panel falls from height and strikes a worker below at the booth-setup site.",
 "その他":"Accident type: other booth-setup hazard. A clear dangerous accident moment involving a scissor lift during exhibition booth setup.",
};
// 完全一致が無ければ前方/部分一致でフォールバック（例「挟まれ・巻き込まれ」→「挟まれ」）。
const sceneKey=TYPE_SCENE[accType]?accType:(Object.keys(TYPE_SCENE).find(k=>k!=="その他"&&(accType.startsWith(k)||accType.includes(k)))||"その他");
const scene=TYPE_SCENE[sceneKey];
const VARIANTS=[
 "Wide angle showing the whole scissor lift and the half-built booth.",
 "Closer dramatic angle emphasising the worker and the moment of danger.",
];
const buildPrompt=(vi)=>`${scene} ${STYLE} ${VARIANTS[vi%VARIANTS.length]}`;

// ---- 生成器 ----
const refBuf=fs.readFileSync(refPath);
const refMime=refFile.toLowerCase().endsWith(".png")?"image/png":refFile.toLowerCase().endsWith(".webp")?"image/webp":refFile.toLowerCase().endsWith(".gif")?"image/gif":"image/jpeg";

// OpenAI images/edits accepts only jpeg/png/webp. For unsupported formats (e.g. GIF) make a
// PNG copy via ImageMagick into the output dir (additive・non-destructive; original is untouched).
const outDir0=path.join(BASE,"gen_event_v20",baseNum);
let oaBuf=refBuf, oaMime=refMime, oaName=refFile;
if(!["image/jpeg","image/png","image/webp"].includes(refMime)){
  fs.mkdirSync(outDir0,{recursive:true});
  const conv=path.join(outDir0,"_ref_openai.png");
  if(!(fs.existsSync(conv)&&fs.statSync(conv).size>1000)){
    execFileSync("magick",[refPath+"[0]",conv]);
  }
  oaBuf=fs.readFileSync(conv);oaMime="image/png";oaName="_ref_openai.png";
}

async function genOpenAI(prompt){
  let last="";
  for(let a=0;a<3;a++){try{
    const fd=new FormData();
    fd.append("model","gpt-image-2");
    fd.append("image",new Blob([oaBuf],{type:oaMime}),oaName);
    fd.append("prompt",prompt);
    fd.append("size","1024x1024");
    fd.append("quality","high");
    fd.append("n","1");
    const r=await fetch("https://api.openai.com/v1/images/edits",{method:"POST",headers:{Authorization:`Bearer ${OPENAI}`},body:fd});
    if(r.status===429||r.status>=500){last=`http ${r.status}`;await sleep(3000*2**a);continue;}
    const j=await r.json();if(j?.data?.[0]?.b64_json)return j.data[0].b64_json;
    last=j?.error?.message||JSON.stringify(j).slice(0,180);await sleep(2000*2**a);
  }catch(e){last=e.message;await sleep(2000*2**a);}}
  throw new Error("openai: "+last);
}
async function genGoogle(prompt){
  const G=["gemini-3-pro-image-preview","gemini-2.5-flash-image"];let last="";
  for(const model of G){for(let a=0;a<3;a++){try{
    const body={contents:[{parts:[{inlineData:{mimeType:refMime,data:refBuf.toString("base64")}},{text:prompt}]}],generationConfig:{responseModalities:["IMAGE"]}};
    const r=await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`,{method:"POST",headers:{"Content-Type":"application/json","x-goog-api-key":GEMINI},body:JSON.stringify(body)});
    if(r.status===429||r.status>=500){last=`http ${r.status}`;await sleep(3500*2**a);continue;}
    const j=await r.json();const parts=j?.candidates?.[0]?.content?.parts||[];
    const img=parts.find(p=>p.inlineData?.data||p.inline_data?.data);
    if(img)return(img.inlineData||img.inline_data).data;
    last=j?.error?.message||JSON.stringify(j).slice(0,180);
    if(/model/i.test(last)&&/not|found|unknown|invalid|support/i.test(last))break;await sleep(2500*2**a);
  }catch(e){last=e.message;await sleep(2500*2**a);}}}
  throw new Error("google: "+last);
}

const outDir=path.join(BASE,"gen_event_v20",baseNum);
fs.mkdirSync(outDir,{recursive:true});
const jobs=[
  {name:"openai_1.png",fn:()=>genOpenAI(buildPrompt(0)),model:"gpt-image-2"},
  {name:"openai_2.png",fn:()=>genOpenAI(buildPrompt(1)),model:"gpt-image-2"},
  {name:"google_1.png",fn:()=>genGoogle(buildPrompt(0)),model:"gemini-3-pro-image-preview"},
  {name:"google_2.png",fn:()=>genGoogle(buildPrompt(1)),model:"gemini-3-pro-image-preview"},
];
let ok=0,failed=[];
for(const j of jobs){
  const out=path.join(outDir,j.name);
  if(fs.existsSync(out)&&fs.statSync(out).size>4000){console.log("skip(exists)",out);ok++;continue;}
  try{const b64=await j.fn();fs.writeFileSync(out,Buffer.from(b64,"base64"));console.log("saved",out);ok++;}
  catch(e){console.error("FAIL",j.name,"-",String(e.message).slice(0,160));failed.push(j.name);}
}

// ---- event_index_v20.csv 追記（既存番号行があれば skip） ----
const idxCsv=path.join(BASE,"gen_event_v20","event_index_v20.csv");
const idxHeader="元番号,元ファイル,事故の型,生成タイトル,openai_1,openai_2,google_1,google_2,使用モデル\n";
if(!fs.existsSync(idxCsv))fs.writeFileSync(idxCsv,idxHeader);
const existing=fs.readFileSync(idxCsv,"utf8").split(/\r?\n/).some(l=>parseCsvLine(l)[0]===baseNum);
if(!existing&&failed.length===0){
  const title=`展示会場ブース設営中の${accType}事故`;
  const esc=s=>`"${String(s).replace(/"/g,'""')}"`;
  const line=[baseNum,refFile,accType,title,"openai_1.png","openai_2.png","google_1.png","google_2.png","gpt-image-2 / gemini-3-pro-image-preview"].map(esc).join(",");
  fs.appendFileSync(idxCsv,line+"\n");
  console.log("index appended",baseNum);
}
console.log(`DONE base=${baseNum} type=${accType} ref=${refFile} domain=${domain} memo=${memo} ok=${ok}/4 failed=${failed.join(",")||"none"}`);
process.exit(failed.length?1:0);
