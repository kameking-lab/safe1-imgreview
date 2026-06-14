/** gen_v14_a1.mjs --id=A1 [--n=8] [--account=geminiv14]
 * 元絵(refs/I-A1_ref.jpg)を参照画像として添付し、構図・力の向き・接触点・機種を厳守して
 * 博展業態へ文脈調整した写実写真を生成。スパークル/ロゴ/可読文字/流血なし。単一フレーム厳守。
 * I-A1 機序: 自走式の高所作業車(MEWP)が不整地/傾斜地で安定を失い、機体ごと後方(坂上側)へ転倒し、
 *   作業床(バスケット)上の作業者が高所から振り落とされる(墜落)瞬間。
 *   接触点=走行台車の支持喪失(片側が浮き/沈む)。力の向き=機体全体が後方へ倒れ込み、作業者が宙に投げ出される。
 * 出力: v14/A1/cand/cNN.png（候補）。最良3枚は後段で 01〜03.png に確定。 */
import path from "node:path"; import fs from "node:fs";
const arg=(k,d)=>{const a=process.argv.find(x=>x.startsWith(`--${k}=`));return a?a.split("=")[1]:d;};
const ID=arg("id","A1"), N=parseInt(arg("n","8"),10), ACCT=arg("account","geminiv14");
const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser, saveScreenshot, dismissOverlays, ensureGeminiLoggedIn } = await import(`file:///${LIB}/browser-helpers.mjs`);
const { startNewChat, submitPrompt } = await import(`file:///${LIB}/gemini-helpers.mjs`);
const BASE="C:/Users/kanet/20260522/safe1";
const OUT=`${BASE}/v14/${ID}/cand`; fs.mkdirSync(OUT,{recursive:true});
const refDir=`${BASE}/refs`;
const refFile=fs.readdirSync(refDir).find(f=>f.startsWith(`I-${ID}_ref.`) && /\.(jpg|jpeg|png|gif)$/i.test(f));
if(!refFile){ console.error("ref not found for",ID); process.exit(1); }
const REF=path.resolve(refDir,refFile);

const DESC="At an outdoor Japanese exhibition/event venue, a SELF-PROPELLED AERIAL WORK PLATFORM (a mobile elevating work platform / boom or scissor type MEWP on its own travelling chassis, with a raised work basket up high) is set up on UNEVEN, SLOPED ground (a soft / poorly-matted slope with a step or rut). The whole MACHINE is TIPPING OVER BACKWARD — toppling as one unit toward the up-slope / rear side because the chassis has lost its support on one side (one side of the undercarriage lifting / sinking). High up, a JAPANESE worker who was in the elevated work basket is being THROWN OUT and flung through the air, falling from height as the machine topples. Contact point: the loss of support under the travelling chassis (the base going over). Force direction: the entire machine rotating / falling BACKWARD and the worker being flung out of the high basket. Keep this exact geometry — the whole self-propelled aerial platform tipping over backward on uneven/sloped ground while the basket worker is thrown from height. The hazard is the WHOLE MACHINE toppling over (not a load tipping, not a simple fall from a stationary intact machine).";
// 元絵はライン画。コラージュ/インセット/2コマ化・線画化を強く禁止。アングルを3種で振る。
const APPROACH=[
 "Camera: true side view (side elevation), standard 35mm lens, even soft daylight, clearly showing the whole aerial platform tipped over backward on the slope with the worker flung from the high basket.",
 "Camera: from diagonally behind the machine and slightly elevated, overcast soft light, showing the chassis lifting off the uneven ground as the machine topples backward.",
 "Camera: a low angle near ground level looking up at the toppling aerial platform and the worker thrown out of the basket high above, slightly wide lens, directional afternoon light.",
];
const SUF=" Setting: a real Japanese outdoor exhibition/event venue work area (haul road / venue ground, doing signage installation, exhibition booth assembly, or overhead truss work; exhibition panels/booth frames around). The worker is a JAPANESE man in Japanese site PPE: safety helmet WITH CHIN STRAP, hi-vis vest or work jacket, safety boots, and (for height work) a FULL-BODY HARNESS. Equipment is Japanese-spec (a Japanese self-propelled aerial work platform / MEWP, NOT an excavator, NOT a forklift). NO company logos, NO readable text/signage, no blood/gore.";
const NEG=" CRITICAL OUTPUT FORMAT: produce ONE SINGLE photorealistic documentary photograph filling the WHOLE frame — a single continuous real scene. Do NOT make a collage, montage, multi-panel, split-screen, comic strip, storyboard, or any inset/circle zoom bubble. Do NOT keep the line-art / cartoon / illustration / drawing style of the attached reference. No borders, no white frames, no panels. NO decorative sparkles, glitter, lens-flare or magical effects. Just one realistic photo of the dangerous moment.";
function prompt(i){
 return "The attached image is the OFFICIAL accident-prevention LINE DIAGRAM of a self-propelled aerial work platform tipping over backward on uneven/sloped ground while the basket worker is thrown from height. Use it ONLY as the composition / force-direction / contact-point reference (same mechanism = the whole machine toppling backward on uneven ground, same contact point = the chassis losing support and the worker flung from the high basket), but COMPLETELY redraw it as a real photo. "
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
