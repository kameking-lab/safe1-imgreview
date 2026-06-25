// gen_event_v21.mjs — aerial2 元絵を参照画像にして「展示会場ブース設営中の事故＋その"原因"が見える」イラストを
//   Google gemini-3-pro-image-preview のみで2枚生成（OpenAI 不使用）。
// 使い方: node gen_event_v21.mjs <baseNum> [strong]
//   collect_aerial2/aerial2_index.csv から baseNum の ファイル名/事故の型 を引き、collect_aerial2/img/<file> を参照画像として渡す。
//   出力: gen_event_v21/<baseNum>/{google_1,google_2}.png （既存>4KBは skip＝再開安全・非破壊）。
//   strong を付けると再生成用の強い原因指示で google_1b/google_2b.png（新ファイル名・上書きしない）に出力。
//   event_index_v21.csv に1行追記（既存番号行があれば追記しない）。
// 【最重要】各イラストに「事故の原因（不安全行動・不安全状態）」を転落/転倒の瞬間と同じ画面に描く。
// キー値は出力しない(.env から読む)。削除/上書き/Chrome killしない。OpenAI 経路は持たない。
import fs from "node:fs";
import path from "node:path";

const BASE = "C:/Users/kanet/20260522/safe1";
const baseNum = String(process.argv[2]||"").trim();
const STRONG = String(process.argv[3]||"").trim().toLowerCase()==="strong";
if(!baseNum){console.error("usage: node gen_event_v21.mjs <baseNum> [strong]");process.exit(2);}

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
const memo=row[idx("状況メモ")].trim();
const domain=row[idx("出所ドメイン")].trim();
const refPath=path.join(BASE,"collect_aerial2/img",refFile);
if(!fs.existsSync(refPath)){console.error(`該当なし: 参照画像 ${refFile} が見つかりません`);process.exit(4);}

// ---- 番号ごとに設定した「原因シナリオ」(英語=生成用 / 日本語=記録用) ----
// その番号が無ければ事故の型ごとの既定原因にフォールバック。
const CAUSE_BY_NUM={
 "1":{ja:"高所作業車(シザースリフト)を上昇させたまま走行させ、組みかけブースのアルミトラスに激突。衝撃で手すり際の作業員がバランスを崩し手すりを越えて転落",
      en:"CAUSE (must be clearly visible in frame): the scissor lift was DRIVEN/TRAVELLED while still fully elevated and its raised platform edge SLAMS into a half-built aluminium booth truss/signage frame; the collision is happening right now and the impact throws the edge worker off balance so he is tipping/being thrown OVER the guardrail. Show BOTH the collision (the platform wedged/striking the truss, the truss frame bending) AND the worker falling over the rail in the SAME image."},
 "2":{ja:"高い看板パネルを取付けようとシザースリフトの手すりに片足を掛けて乗り上がり、身を大きく乗り出した不安全姿勢からバランスを崩して手すりを越え転落",
      en:"CAUSE (must be clearly visible in frame): to reach and fix a high signage panel a worker has PUT ONE FOOT UP ONTO THE GUARDRAIL of the scissor-lift platform and is standing/leaning far out over the rail in a clearly unsafe posture; from that posture he loses balance and is tipping head-first OVER the guardrail. Show BOTH the unsafe act (foot up on the rail, body leaning way out past the railing toward the booth panel) AND the worker falling over the rail in the SAME image."},
 "3":{ja:"シザースリフト乗降口の安全チェーン(開閉バー)を掛け忘れたまま高所作業し、開いた乗降口の側へ後退りして、ガードのない開口部からそのまま転落",
      en:"CAUSE (must be clearly visible in frame): the platform's ENTRY GATE / safety chain of the scissor lift was LEFT UNFASTENED (the entry gap in the guardrail is wide OPEN, the chain dangling unhooked); while working the worker steps/stumbles BACKWARD toward that open unguarded gap and is now falling straight out through the OPEN gate. Show BOTH the cause (the clearly open, unguarded entry gap with the dangling unhooked chain) AND the worker dropping through that gap in the SAME image."},
 "45":{ja:"作業床から組みかけブースのトラスへ直接乗り移ろうとして、シザースリフトと未固定のトラスの間で足を踏み外し、フルハーネスのフックを未接続のまま機体とブースの隙間へ転落",
      en:"CAUSE (must be clearly visible in frame): instead of repositioning the platform, the worker tries to CLIMB ACROSS / STEP OVER directly from the scissor-lift platform onto a half-built booth truss to reach a sign; his full-body harness LANYARD HOOK IS UNCONNECTED and dangles loose; the unsecured truss shifts and he MISSES HIS FOOTING, now falling into the GAP between the lift and the booth structure. Show BOTH the cause (the worker straddling/transferring from the platform to the truss with the clearly DANGLING UNHOOKED lanyard, the truss tilting) AND the worker dropping into the gap in the SAME image."},
 "64":{ja:"シザースリフトの作業床から離れた高い看板パネル/トラス上部に手を届かせようと、手すりの外へ上半身を大きく乗り出して無理に背伸び。重心が手すりの外側へ出てバランスを崩し、頭から手すりを越えて転落",
      en:"CAUSE (must be clearly visible in frame): the scissor-lift platform was NOT driven close enough to the work, so the worker LEANS HIS UPPER BODY FAR OUT past the guardrail and stretches/over-reaches with both arms toward a tall signage panel / upper booth truss that is beyond arm's reach; his centre of gravity has gone OUTSIDE the rail and he is now tipping HEAD-FIRST OVER the guardrail. Show BOTH the cause (the worker over-reaching, torso bent way out across and beyond the guardrail toward the out-of-reach booth panel, feet lifting off the platform floor) AND the worker pitching over the rail in the SAME image. This is over-reaching from the basket, NOT a foot placed up on the rail."},
};
const CAUSE_BY_TYPE={
 "墜落・転落":{ja:"手すりに足を掛けて/身を乗り出して無理な姿勢で看板を取付け、バランスを崩して手すりを越え転落",
   en:"CAUSE (visible): a worker on the scissor-lift platform OVERREACHES far out / puts a foot on or leans over the guardrail to fix a signage panel, loses balance and tips over the rail. Show the unsafe overreaching posture AND the fall together."},
 "転倒・横転":{ja:"アウトリガー/接地不良または床の段差・ケーブルに片輪が乗り上げ、上昇中のシザースリフトが傾いて横転",
   en:"CAUSE (visible): the scissor lift tips/overturns because one wheel has ridden up onto a floor step/gap or a thick cable run, OR it stands on uneven ground; show the tilted lift AND the visible floor step/cable/uneven ground underneath that caused it."},
 "挟まれ":{ja:"下降操作中に身体/手をシザース機構の隙間に入れて挟まれる、または重い什器・パネルとの間に挟まれる",
   en:"CAUSE (visible): while the scissor mechanism is being lowered a worker's hand/body is inside the closing scissor linkage (or pinched between a heavy panel and a fixture); show the body part caught at the pinch point AND the moving mechanism."},
 "不安全行動":{ja:"フルハーネスのフック未接続のまま手すりに立つ/構造物へ乗り移ろうとして転落",
   en:"CAUSE (visible): the worker performs an unsafe act — standing on the guardrail or trying to climb across onto the booth structure with the harness hook UNCONNECTED (dangling); show the dangling unhooked lanyard AND the worker falling."},
 "感電":{ja:"展示用照明/電源配線を活線のまま触り感電、上で身体がのけぞり墜落",
   en:"CAUSE (visible): the worker touches live exhibition lighting/power wiring; show the contact with the wiring AND the worker recoiling/falling from the platform."},
 "飛来・落下":{ja:"上で固定不十分なトラス材/看板パネルが落下し下の作業員に直撃",
   en:"CAUSE (visible): an unsecured truss bar / signage panel slips from the height; show it dropping from the unfinished structure AND striking the worker below."},
 "その他":{ja:"ブース設営中の不安全状態によりシザースリフト上の作業員が被災",
   en:"CAUSE (visible): a clear unsafe condition/act on a scissor lift during booth setup is shown together with the resulting accident moment."},
};
const sceneKey=CAUSE_BY_TYPE[accType]?accType:(Object.keys(CAUSE_BY_TYPE).find(k=>k!=="その他"&&(accType.startsWith(k)||accType.includes(k)))||"その他");
const cause=CAUSE_BY_NUM[baseNum]||CAUSE_BY_TYPE[sceneKey];

// ---- 統一スタイル ----
const STYLE=[
 "High-quality, realistic Japanese workplace-safety educational illustration (clean professional art with rich shading, depth and a sense of presence). Do NOT imitate the source picture's drawing style; only inherit its accident TYPE. The source image is a reference for the hazard type only.",
 "Setting: a JAPANESE EXHIBITION HALL / trade-show booth SETUP site (half-built exhibition booths, aluminium truss frames, large blank signage panels, display fixtures, cardboard crates, floor cable runs and small floor steps, a loading dock in the background).",
 "Workers: Japanese exhibition crew wearing chin-strap helmets, hi-vis vests, work gloves and safety boots; when at height they wear a full-body safety harness.",
 "Any aerial work platform MUST be a SCISSOR LIFT only (vertical scissor-type elevating platform). Never a boom lift or truck-mounted boom.",
 "Absolutely NO text, NO letters, NO numbers, NO arrows, NO captions, NO speech bubbles, NO symbols anywhere. No blood/gore. No real brand names or real logos. Proper PPE on workers.",
].join(" ");
const MOST_IMPORTANT="MOST IMPORTANT: this is a CAUSE-AND-EFFECT safety illustration. The viewer must instantly understand WHAT WENT WRONG. Draw the accident MOMENT (the fall / tip-over / being struck) AND the CAUSE (the unsafe act or unsafe condition) TOGETHER in the same frame. Do NOT draw a person merely falling through empty air with no visible cause.";
const STRONG_EXTRA=STRONG?" EXTRA EMPHASIS: the previous attempt failed because the CAUSE was not visible. Make the unsafe condition/act unmistakably large and central in the foreground, clearly connected to why the person is falling.":"";
const VARIANTS=[
 "Composition A: wide angle showing the whole scissor lift, the half-built booth and the cause-object clearly, with the worker at the accident moment.",
 "Composition B: closer dramatic angle that still keeps BOTH the cause and the falling/struck worker visible in frame.",
];
const buildPrompt=(vi)=>`${cause.en} ${MOST_IMPORTANT}${STRONG_EXTRA} ${STYLE} ${VARIANTS[vi%VARIANTS.length]}`;

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

const outDir=path.join(BASE,"gen_event_v21",baseNum);
fs.mkdirSync(outDir,{recursive:true});
const sfx=STRONG?"b":"";
const jobs=[
  {name:`google_1${sfx}.png`,fn:()=>genGoogle(buildPrompt(0))},
  {name:`google_2${sfx}.png`,fn:()=>genGoogle(buildPrompt(1))},
];
let ok=0,failed=[];
for(const j of jobs){
  const out=path.join(outDir,j.name);
  if(fs.existsSync(out)&&fs.statSync(out).size>4000){console.log("skip(exists)",out);ok++;continue;}
  try{const b64=await j.fn();fs.writeFileSync(out,Buffer.from(b64,"base64"));console.log("saved",out);ok++;}
  catch(e){console.error("FAIL",j.name,"-",String(e.message).slice(0,160));failed.push(j.name);}
}

// ---- event_index_v21.csv 追記（既存番号行があれば skip・通常生成時のみ） ----
if(!STRONG){
  const idxCsv=path.join(BASE,"gen_event_v21","event_index_v21.csv");
  const idxHeader="元番号,元ファイル,元の事故の型,設定した原因シナリオ,生成タイトル,google_1,google_2\n";
  if(!fs.existsSync(idxCsv))fs.writeFileSync(idxCsv,idxHeader);
  const existing=fs.readFileSync(idxCsv,"utf8").split(/\r?\n/).some(l=>parseCsvLine(l)[0]===baseNum);
  if(!existing&&failed.length===0){
    const title=`展示会場ブース設営中の${accType}事故（原因が見える）`;
    const esc=s=>`"${String(s).replace(/"/g,'""')}"`;
    const line=[baseNum,refFile,accType,cause.ja,title,"google_1.png","google_2.png"].map(esc).join(",");
    fs.appendFileSync(idxCsv,line+"\n");
    console.log("index appended",baseNum);
  }
}
console.log(`DONE base=${baseNum} type=${accType} ref=${refFile} domain=${domain} strong=${STRONG} cause="${cause.ja}" ok=${ok}/2 failed=${failed.join(",")||"none"}`);
process.exit(failed.length?1:0);
