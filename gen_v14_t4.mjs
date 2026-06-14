/** gen_v14_t4.mjs --id=T4 [--n=8] [--account=geminiv14]
 * 元絵(refs/I-T4_ref.jpg)を参照画像として添付し、構図・力の向き・接触点・機種を厳守して
 * 博展業態へ文脈調整した写実写真を生成。スパークル/ロゴ/流血なし。
 * I-T4 機序: テールゲートリフター(昇降板=水平)の上で、資材を積んだカゴ車(ロールボックスパレット)が
 *   自重バランスで横に倒れ、昇降板上／後方の作業者の頭部・上体に激突して後方へ突き倒される瞬間。
 * 出力: v14/T4/cand/cNN.png（候補）。最良3枚は後段で 01〜03.png に確定。 */
import path from "node:path"; import fs from "node:fs";
const arg=(k,d)=>{const a=process.argv.find(x=>x.startsWith(`--${k}=`));return a?a.split("=")[1]:d;};
const ID=arg("id","T4"), N=parseInt(arg("n","8"),10), ACCT=arg("account","geminiv14");
const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser, saveScreenshot, dismissOverlays, ensureGeminiLoggedIn } = await import(`file:///${LIB}/browser-helpers.mjs`);
const { startNewChat, submitPrompt } = await import(`file:///${LIB}/gemini-helpers.mjs`);
const BASE="C:/Users/kanet/20260522/safe1";
const OUT=`${BASE}/v14/${ID}/cand`; fs.mkdirSync(OUT,{recursive:true});
// 参照画像（元絵） refs/I-{ID}_ref.(jpg|png|gif)
const refDir=`${BASE}/refs`;
const refFile=fs.readdirSync(refDir).find(f=>f.startsWith(`I-${ID}_ref.`) && /\.(jpg|jpeg|png|gif)$/i.test(f));
if(!refFile){ console.error("ref not found for",ID); process.exit(1); }
const REF=path.resolve(refDir,refFile);

// 機序ごとの厳密記述（力の向き・接触点・機種を固定）。博展文脈=展示資材を積んだカゴ車。
const DESC={
 T4:"At the rear of a Japanese box truck fitted with a folding TAIL-LIFT (tailgate lifter / power-gate) platform, at an exhibition-venue loading dock. The tail-lift platform is HORIZONTAL / LEVEL (not tilted). A tall metal CAGE CART (roll box pallet / Japanese kago-sha — an upright wheeled wire-mesh cage on casters) LOADED with exhibition materials (stacked packed cardboard boxes and flat display panels) is standing ON the level tail-lift platform and is now TOPPLING SIDEWAYS / TIPPING OVER by its own weight toward a worker. The loaded cage cart is FALLING ONTO the worker — its upper frame and load SLAMMING INTO the worker's head and upper body, knocking him BACKWARD off balance. The worker had been steadying the cage cart with both hands but cannot hold it and is being struck and pushed over backward. Contact point: the top frame / body of the toppling loaded cage cart striking the worker's head and chest. Force direction: the loaded cage cart toppling sideways off the level platform and crashing onto/into the worker, knocking him backward and down. Keep this exact geometry — a loaded upright metal cage cart toppling over on a LEVEL tail-lift and slamming into the worker who is on/just behind the platform.",
};
const APPROACH=[
 "Camera: true side view (side elevation), standard 35mm lens, even soft daylight, clearly showing the loaded cage cart toppling sideways off the level platform and slamming into the worker.",
 "Camera: from diagonally behind the truck and slightly elevated, overcast soft light, looking down along the platform at the cage cart tipping over onto the worker.",
 "Camera: a low angle near ground level looking up at the level tail-lift platform and the loaded cage cart toppling toward the camera onto the struck worker, slightly wide lens, directional afternoon light.",
];
const SUF=" Setting: a real Japanese exhibition/event venue loading area (back-of-house dock, plain concrete, exhibition panels/crates around). The worker is a JAPANESE man in Japanese site PPE: safety helmet WITH CHIN STRAP, hi-vis vest or work jacket, safety boots. Equipment is Japanese-spec (a Japanese tail-lift box truck and a Japanese wire-mesh cage cart / roll box pallet, NOT a forklift/excavator). NO company logos, NO readable text/signage, no blood/gore. NO decorative sparkles, glitter, lens-flare or magical effects. Photorealistic documentary photograph, natural light, show only the dangerous moment.";
function prompt(i){
 return "The attached image is the OFFICIAL accident-prevention diagram (line illustration) of a loaded metal cage cart toppling over and slamming into a worker on a truck tail-lift. Use it STRICTLY as the composition / layout / force-direction / contact-point reference: keep the SAME mechanism (a tall loaded wire-mesh cage cart tipping sideways and crashing into the worker) on a TRUCK TAIL-LIFT (power-gate) that is LEVEL, and keep the SAME contact point (the toppling cage cart frame coming onto the worker's head/upper body). Recreate it as a PHOTOREALISTIC photograph (do NOT keep the drawing/line-art style — make it a real photo). "
  + DESC[ID] + " " + APPROACH[i%APPROACH.length] + SUF;
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

// 既存候補をスキップ（再開で重複生成しない）
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
