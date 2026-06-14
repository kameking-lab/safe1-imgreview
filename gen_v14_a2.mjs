/** gen_v14_a2.mjs --id=A2 [--n=8] [--account=geminiv14]
 * 元絵(refs/I-A2_ref.gif)を参照画像として添付し、構図・力の向き・接触点・機種を厳守して
 * 博展業態へ文脈調整した写実写真を生成。スパークル/ロゴ/可読文字/流血なし。単一フレーム厳守。
 * I-A2 機序: 高所作業車の作業床(バスケット)を上昇させた際、作業者の頭部/頚部/上半身が、
 *   上方の構造物=梁/桁/吊看板/天井トラス下弦材などの下面と、作業床(バスケット)の手すりとの間に挟まれる。
 *   接触点=バスケット上縁の手すり×上方構造物下面。力の向き=バスケット上昇(上向き)で作業者が上方構造物へ挟圧される。
 * 出力: v14/A2/cand/cNN.png（候補）。最良3枚は後段で 01〜03.png に確定。 */
import path from "node:path"; import fs from "node:fs";
const arg=(k,d)=>{const a=process.argv.find(x=>x.startsWith(`--${k}=`));return a?a.split("=")[1]:d;};
const ID=arg("id","A2"), N=parseInt(arg("n","8"),10), ACCT=arg("account","geminiv14");
const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser, saveScreenshot, dismissOverlays, ensureGeminiLoggedIn } = await import(`file:///${LIB}/browser-helpers.mjs`);
const { startNewChat, submitPrompt } = await import(`file:///${LIB}/gemini-helpers.mjs`);
const BASE="C:/Users/kanet/20260522/safe1";
const OUT=`${BASE}/v14/${ID}/cand`; fs.mkdirSync(OUT,{recursive:true});
const refDir=`${BASE}/refs`;
const refFile=fs.readdirSync(refDir).find(f=>f.startsWith(`I-${ID}_ref.`) && /\.(jpg|jpeg|png|gif)$/i.test(f));
if(!refFile){ console.error("ref not found for",ID); process.exit(1); }
const REF=path.resolve(refDir,refFile);

const DESC="At a Japanese exhibition/event venue, a SELF-PROPELLED or TRUCK-MOUNTED AERIAL WORK PLATFORM (a mobile elevating work platform / MEWP with a work basket on a boom) has its work basket RAISED UP HIGH toward an OVERHEAD STRUCTURE — an event-hall steel BEAM / girder underside, a suspended hanging sign, or the lower chord of a CEILING TRUSS. A JAPANESE worker standing in the elevated basket is being CRUSHED / PINCHED: the basket has risen too far and the worker's HEAD and UPPER BODY are caught and squeezed BETWEEN the TOP GUARD RAIL of the work basket and the UNDERSIDE of the overhead structure (the beam / truss / hanging sign). Contact point: the worker's head/neck pinned between the basket's top rail and the underside of the overhead structure. Force direction: the basket rising UPWARD pressing the worker UP against the fixed overhead structure (an upward crushing / pinch force). Keep this exact geometry — the raised aerial-platform basket and the worker's head/upper body pinched between the basket top rail and the overhead beam/truss/sign above. The hazard is the worker being CRUSHED between the rising work basket and the overhead structure (not a fall, not a machine tipping over, not a load tipping).";
// 元絵はライン画。コラージュ/インセット/2コマ化・線画化を強く禁止。アングルを3種で振る。
const APPROACH=[
 "Camera: true side view (side elevation), standard 35mm lens, even soft daylight, clearly showing the gap closed between the basket top rail and the overhead beam with the worker's head pinned between them.",
 "Camera: from diagonally behind and slightly above the basket, soft indoor venue light, showing the worker's upper body squeezed up against the underside of the overhead truss/beam.",
 "Camera: a low angle from below looking up at the raised basket and the worker's head crushed against the overhead structure, slightly wide lens, directional hall lighting.",
];
const SUF=" Setting: a real Japanese exhibition/event venue work area (overhead truss / beam / hanging-sign installation, exhibition booth upper assembly; exhibition panels/booth frames and hall structure around). The worker is a JAPANESE man in Japanese site PPE: safety helmet WITH CHIN STRAP, hi-vis vest or work jacket, safety boots, and a FULL-BODY HARNESS. Equipment is Japanese-spec (a Japanese aerial work platform / MEWP work basket, NOT an excavator, NOT a forklift). NO company logos, NO readable text/signage, no blood/gore.";
const NEG=" CRITICAL OUTPUT FORMAT: produce ONE SINGLE photorealistic documentary photograph filling the WHOLE frame — a single continuous real scene. Do NOT make a collage, montage, multi-panel, split-screen, comic strip, storyboard, or any inset/circle zoom bubble. Do NOT keep the line-art / cartoon / illustration / drawing style of the attached reference. No borders, no white frames, no panels. NO decorative sparkles, glitter, lens-flare or magical effects. Just one realistic photo of the dangerous moment.";
function prompt(i){
 return "The attached image is the OFFICIAL accident-prevention LINE DIAGRAM of an aerial-work-platform basket worker whose head is pinched between the basket top rail and an overhead structure as the basket is raised. Use it ONLY as the composition / force-direction / contact-point reference (same mechanism = worker crushed between the rising basket rail and the overhead beam/structure, same contact point = head/upper body between the basket top rail and the overhead structure underside), but COMPLETELY redraw it as a real photo. "
  + DESC + " " + APPROACH[i%APPROACH.length] + SUF + NEG;
}

async function attach(page, absPath){
  let ok=false;
  for(const inp of await page.locator('input[type="file"]').all().catch(()=>[])){
    try{ await inp.setInputFiles(absPath); ok=true; break; }catch{}
  }
  if(ok) return true;
  const sels=['button[aria-label*="アップロード"][aria-label*="メニュー"]','button[aria-label*="メニューを開く"]','button[aria-label*="追加"]','button[aria-label*="ファイル"]','button[aria-label*="アップロード"]','button[aria-label*="add" i]','button[aria-label*="attach" i]','button:has(mat-icon)'];
  for(const s of sels){ const b=page.locator(s).first(); if(await b.isVisible({timeout:700}).catch(()=>false)){ await b.click().catch(()=>{}); await page.waitForTimeout(800);
    for(const inp of await page.locator('input[type="file"]').all().catch(()=>[])){ try{ await inp.setInputFiles(absPath); ok=true; break; }catch{} }
    if(ok) break;
    for(const it of ['[role="menuitem"]:has-text("ファイルをアップロード")','button:has-text("ファイルをアップロード")','[role="menuitem"]:has-text("アップロード")']){
      const item=page.locator(it).first(); if(await item.isVisible({timeout:1000}).catch(()=>false)){ try{ const [ch]=await Promise.all([page.waitForEvent("filechooser",{timeout:8000}),item.click()]); await ch.setFiles(absPath); ok=true; break; }catch{} } }
    if(ok) break;
    }
  }
  return ok;
}
async function waitImg(page,prev,maxSec=240){await page.waitForTimeout(6000);for(let w=0;w<maxSec/5;w++){const c=await page.evaluate(()=>Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const ww=i.naturalWidth||i.width;return ww>240&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));}).length);if(c>prev)return true;const stop=await page.locator('button[aria-label*="停止"],button[aria-label*="Stop"]').first().isVisible({timeout:500}).catch(()=>false);if(!stop&&w>2){const t=await page.evaluate(()=>document.body.innerText);if(/制限に達|quota|rate.?limit|後でもう一度/i.test(t))throw new Error("QUOTA");return false;}await page.waitForTimeout(5000);}return false;}
async function dl(page,out,beforeCount){const b=await page.evaluate(async(bc)=>{const im=Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const w=i.naturalWidth||i.width;return w>240&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));});if(im.length<=bc)return null;const g=im[im.length-1];if(g.src.startsWith("data:image"))return g.src.split(",")[1];try{const r=await fetch(g.src,{credentials:"include"});const bl=await r.blob();return await new Promise(res=>{const rd=new FileReader();rd.onload=()=>res(rd.result.split(",")[1]);rd.onerror=()=>res(null);rd.readAsDataURL(bl);});}catch{return null;}},beforeCount);if(b){fs.writeFileSync(out,Buffer.from(b,"base64"));return fs.statSync(out).size>4000;}return false;}
async function imgCount(page){return await page.evaluate(()=>Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const w=i.naturalWidth||i.width;return w>240&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));}).length);}
async function dlShot(page,out,beforeCount){
  try{
    const h=await page.evaluateHandle((bc)=>{const im=Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const w=i.naturalWidth||i.width;return w>240&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));});return im.length>bc?im[im.length-1]:null;},beforeCount);
    const el=h.asElement(); if(!el) return false;
    await page.mouse.move(3,3).catch(()=>{}); await page.keyboard.press("Escape").catch(()=>{});
    await el.scrollIntoViewIfNeeded().catch(()=>{}); await page.waitForTimeout(400);
    await el.screenshot({path:out});
    return fs.existsSync(out)&&fs.statSync(out).size>4000;
  }catch{ return false; }
}

function nextIdx(){ let i=1; while(fs.existsSync(path.join(OUT,`c${String(i).padStart(2,"0")}.png`))) i++; return i; }
const manifest={id:ID,ref:refFile,ok:[],fail:[]};
await (async () => {
const { ctx, page } = await launchBrowser(ACCT,{viewport:{width:1500,height:1000},acceptDownloads:true});
try{
  await ensureGeminiLoggedIn(page); await page.waitForTimeout(2000); await dismissOverlays(page);
  let made=0, idx=nextIdx();
  for(let k=0; k<N; k++){
    const ci=idx+made; const out=path.join(OUT,`c${String(ci).padStart(2,"0")}.png`); let done=false;
    for(let a=1;a<=2 && !done;a++){
      console.log(`\n[v14 ${ID}] cand ${ci} (approach ${(k%APPROACH.length)+1}) try ${a}`);
      try{
        await startNewChat(page); await page.waitForTimeout(1500); await dismissOverlays(page);
        const att=await attach(page,REF); console.log("  attach:",att);
        await page.waitForTimeout(2500);
        const before=await imgCount(page);
        await submitPrompt(page,prompt(k));
        const f=await waitImg(page,before,260); await page.waitForTimeout(2500);
        await saveScreenshot(page,`v14${ID}`,`c${ci}-${a}`).catch(()=>{});
        if(f && (await dl(page,out,before) || await dlShot(page,out,before))){ done=true; console.log("  saved",out); }
        else console.warn("  no/dl-fail");
      }catch(e){ console.error("  err",e.message); if(e.message==="QUOTA"){manifest.fail.push({c:ci,reason:"quota"});break;} await page.waitForTimeout(2500); }
    }
    if(done){ manifest.ok.push(ci); made++; }
    else { manifest.fail.push({c:ci,reason:"no-image"}); if(manifest.fail.find(x=>x.reason==="quota")) break; }
  }
} finally{ fs.writeFileSync(path.join(OUT,"manifest.json"),JSON.stringify(manifest,null,2)); try{await ctx.close();}catch{} console.log(`\n[v14 ${ID}] DONE ok=${manifest.ok.length}`); }
})();
