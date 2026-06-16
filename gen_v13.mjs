/** gen_v13.mjs --case=N [--n=3]
 * 公式事故図(refs/anzen/caseN_1.*)を参照画像に添付し、構図・向き・接触点を厳守して写実写真を生成。
 * 出力: images/v13photo/case{N}/0{i}.png */
import path from "node:path"; import fs from "node:fs";
const arg=(k,d)=>{const a=process.argv.find(x=>x.startsWith(`--${k}=`));return a?a.split("=")[1]:d;};
const CASE=arg("case","1"), N=parseInt(arg("n","3"),10);
const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser, saveScreenshot, dismissOverlays, ensureGeminiLoggedIn } = await import(`file:///${LIB}/browser-helpers.mjs`);
const { startNewChat, submitPrompt } = await import(`file:///${LIB}/gemini-helpers.mjs`);
const BASE="C:/Users/kanet/20260522/safe1";
const OUT=`${BASE}/images/v13photo/case${CASE}`; fs.mkdirSync(OUT,{recursive:true});
// 参照画像
const refDir=`${BASE}/refs/anzen`;
const ref=fs.readdirSync(refDir).find(f=>f.startsWith(`case${CASE}_`));
const REF=path.resolve(refDir,ref);

const DESC={
 1:"At the rear of a Japanese 2-ton truck fitted with a folding tail-lift. A worker is operating the control switch on the truck-bed rear, and his head and upper body are caught and PINCHED in the closing gap between the RISING tail-lift platform and the truck-bed rear edge. He is upright / leaning in, NOT falling; the platform squeezes him from below. Keep this exact pinch geometry and direction.",
 2:"A Japanese truck with a folding tail-lift at the rear, parked on ground that slopes DOWN toward a warehouse entrance so the truck rear sinks. An overloaded heavy machine on the tilted tail-lift is sliding and tipping BACKWARD and DOWN off the platform, and the worker behind it is crushed underneath, moving the SAME backward-down direction. Keep load and man in the same direction.",
 3:"On a Japanese truck's tail-lift platform, a heavy ~200kg tall wheeled cart is TOPPLING sideways toward the worker standing beside it and striking him; the cart and the man go the SAME direction. The man is struck/crushed, NOT falling from height.",
 4:"A Japanese self-propelled aerial work platform (boom/mast lift with a basket — NOT an excavator) on a slope / uneven ground is TIPPING OVER BACKWARD; the whole machine, the basket and the worker inside all fall the SAME backward direction toward the ground.",
 5:"A Japanese aerial work platform basket raised up under a concrete bridge girder; the worker is PINCHED between the basket's top guardrail and the underside of the girder directly above him (overhead pinch), squeezed upward against the overhead structure.",
 6:"A Japanese aerial work platform on a road slope has run away downhill; the worker is PINCHED between the machine's outrigger/chassis base and the edge of an uncovered roadside ditch at the bottom of the slope.",
};
const APPROACH=[
 "Camera: true side view (side elevation), standard 35mm lens, even soft daylight.",
 "Camera: from diagonally behind and slightly elevated, overcast soft light.",
 "Camera: a lower angle closer to the worker, slightly wide lens, directional afternoon light.",
];
const SUF=" Setting: a real Japanese worksite/warehouse/road. The worker is a JAPANESE man in Japanese site PPE: safety helmet WITH CHIN STRAP, hi-vis vest or work jacket, safety boots (full-body fall-arrest harness for aerial work). Equipment is Japanese-spec. NO company logos, NO text, no blood/gore — show only the dangerous moment. Photorealistic documentary photograph, natural light.";
function prompt(i){
 return "The attached image is the OFFICIAL accident diagram. Use it STRICTLY as the composition / layout / direction reference: keep the SAME direction of fall/topple and the SAME contact/pinch point as the diagram. Recreate it as a PHOTOREALISTIC photograph (do NOT keep the line-art/drawing style — make it a real photo). "
  + DESC[CASE] + " " + APPROACH[i] + SUF;
}

async function attach(page, absPath){
  // 戦略1: 既存 input[type=file]
  let ok=false;
  for(const inp of await page.locator('input[type="file"]').all().catch(()=>[])){
    try{ await inp.setInputFiles(absPath); ok=true; break; }catch{}
  }
  if(ok) return true;
  // 戦略2: [+]/アップロードメニュー
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
    await el.scrollIntoViewIfNeeded().catch(()=>{}); await page.waitForTimeout(400);
    await el.screenshot({path:out});
    return fs.existsSync(out)&&fs.statSync(out).size>4000;
  }catch{ return false; }
}

const manifest={case:CASE,ref,ok:[],fail:[]};
await (async () => {
const { ctx, page } = await launchBrowser("gemini",{viewport:{width:1500,height:1000},acceptDownloads:true});
try{
  await ensureGeminiLoggedIn(page); await page.waitForTimeout(2000); await dismissOverlays(page);
  for(let i=0;i<N;i++){
    const out=path.join(OUT,`0${i+1}.png`); let done=false;
    for(let a=1;a<=2 && !done;a++){
      console.log(`\n[v13 c${CASE}] approach ${i+1} try ${a}`);
      try{
        await startNewChat(page); await page.waitForTimeout(1500); await dismissOverlays(page);
        const att=await attach(page,REF); console.log("  attach:",att);
        await page.waitForTimeout(2500);
        const before=await imgCount(page);  // 添付画像が含まれる場合あり
        await submitPrompt(page,prompt(i));
        const f=await waitImg(page,before,260); await page.waitForTimeout(2500);
        await saveScreenshot(page,`v13c${CASE}`,`a${i+1}-${a}`).catch(()=>{});
        if(f && (await dl(page,out,before) || await dlShot(page,out,before))){ done=true; console.log("  saved",out); }
        else console.warn("  no/dl-fail");
      }catch(e){ console.error("  err",e.message); if(e.message==="QUOTA"){manifest.fail.push({a:i+1,reason:"quota"});break;} await page.waitForTimeout(2500); }
    }
    if(done) manifest.ok.push(i+1); else if(!manifest.fail.find(x=>x.a===i+1)) manifest.fail.push({a:i+1,reason:"no-image"});
  }
} finally{ fs.writeFileSync(path.join(OUT,"manifest.json"),JSON.stringify(manifest,null,2)); try{await ctx.close();}catch{} console.log(`\n[v13 c${CASE}] DONE ok=${manifest.ok.length}`); }
})();
