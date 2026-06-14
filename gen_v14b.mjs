/** gen_v14b.mjs --id=T1 [--n=4] --account=geminiv14
 * v14 改良版: クリーンなraw画像URLを最優先で取得（UIツールバー/スパークルの焼込み回避）。
 * fetch失敗時のみ、マウスをコーナーに退避→ホバーUI消滅を待ってから要素スクショで救済。
 * 出力: v14/{ID}/cand/cNN.png（c05/c06など既存は温存し連番継続）。 */
import path from "node:path"; import fs from "node:fs";
const arg=(k,d)=>{const a=process.argv.find(x=>x.startsWith(`--${k}=`));return a?a.split("=")[1]:d;};
const ID=arg("id","T1"), N=parseInt(arg("n","4"),10), ACCT=arg("account","geminiv14");
const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser, saveScreenshot, dismissOverlays, ensureGeminiLoggedIn } = await import(`file:///${LIB}/browser-helpers.mjs`);
const { startNewChat, submitPrompt } = await import(`file:///${LIB}/gemini-helpers.mjs`);
const BASE="C:/Users/kanet/20260522/safe1";
const OUT=`${BASE}/v14/${ID}/cand`; fs.mkdirSync(OUT,{recursive:true});
const refDir=`${BASE}/refs`;
const refFile=fs.readdirSync(refDir).find(f=>f.startsWith(`I-${ID}_ref.`) && /\.(jpg|jpeg|png|gif)$/i.test(f));
const REF=path.resolve(refDir,refFile);

const DESC={
 T1:"At the rear of a Japanese cab-over BOX TRUCK fitted with a folding TAIL-LIFT (tailgate lifter) extended near ground level, at an exhibition-venue back-of-house loading area. A tall wheeled ROLL-CAGE cart loaded with flat EXHIBITION DISPLAY PANELS / wooden crates sits on the tail-lift platform. A JAPANESE worker is FALLING off the OPEN OUTER EDGE of the tail-lift platform — losing balance and pitching head/shoulder-first DOWNWARD to the concrete beside the truck. Contact point: the open outer edge of the tail-lift platform. Fall direction: from the platform edge straight DOWN to the ground. Keep this exact geometry.",
};
const APPROACH=[
 "Camera: true side elevation, wide 3:2 landscape framing, standard lens, even soft daylight.",
 "Camera: from diagonally behind the truck, slightly elevated, wide 3:2 landscape framing, overcast soft light.",
 "Camera: low angle near ground looking up to the platform edge, wide 3:2 landscape framing, directional afternoon light.",
];
const SUF=" Setting: a real Japanese exhibition/event venue loading dock (plain concrete, panels/crates around). The worker is a JAPANESE man in Japanese site PPE: safety helmet WITH CHIN STRAP, hi-vis vest or work jacket, safety boots. Japanese-spec tail-lift box truck (NOT a forklift/excavator). NO company logos, NO readable text, no blood. Absolutely NO decorative sparkles, stars, glitter, lens-flare or magical effects anywhere. Clean photorealistic documentary photograph, natural light, only the dangerous moment. Fill the whole frame with the scene, no borders.";
const prompt=(i)=>"The attached image is the OFFICIAL accident-prevention line illustration. Use it STRICTLY as the composition/force-direction/contact-point reference: keep the SAME fall direction, the SAME contact point (tail-lift platform edge) and the SAME machine (truck tail-lift). Recreate as a PHOTOREALISTIC photo (NOT line-art). "+DESC[ID]+" "+APPROACH[i%APPROACH.length]+SUF;

async function attach(page, absPath){
  for(const inp of await page.locator('input[type="file"]').all().catch(()=>[])){ try{ await inp.setInputFiles(absPath); return true; }catch{} }
  const sels=['button[aria-label*="アップロード"][aria-label*="メニュー"]','button[aria-label*="追加"]','button[aria-label*="ファイル"]','button[aria-label*="アップロード"]','button:has(mat-icon)'];
  for(const s of sels){ const b=page.locator(s).first(); if(await b.isVisible({timeout:700}).catch(()=>false)){ await b.click().catch(()=>{}); await page.waitForTimeout(800);
    for(const inp of await page.locator('input[type="file"]').all().catch(()=>[])){ try{ await inp.setInputFiles(absPath); return true; }catch{} }
    for(const it of ['[role="menuitem"]:has-text("ファイルをアップロード")','button:has-text("ファイルをアップロード")']){ const item=page.locator(it).first(); if(await item.isVisible({timeout:1000}).catch(()=>false)){ try{ const [ch]=await Promise.all([page.waitForEvent("filechooser",{timeout:8000}),item.click()]); await ch.setFiles(absPath); return true; }catch{} } }
  } }
  return false;
}
const bigImgs=`Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const w=i.naturalWidth||i.width;return w>240&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));})`;
async function imgCount(page){return await page.evaluate(`(${bigImgs}).length`);}
async function waitImg(page,prev,maxSec=260){await page.waitForTimeout(6000);for(let w=0;w<maxSec/5;w++){const c=await imgCount(page);if(c>prev)return true;const stop=await page.locator('button[aria-label*="停止"],button[aria-label*="Stop"]').first().isVisible({timeout:500}).catch(()=>false);if(!stop&&w>2){const t=await page.evaluate(()=>document.body.innerText);if(/制限に達|quota|rate.?limit|後でもう一度/i.test(t))throw new Error("QUOTA");return false;}await page.waitForTimeout(5000);}return false;}
// クリーン取得: 生成imgのsrcを高解像度化してfetch（UIは含まれない）
async function dlClean(page,out,beforeCount){
  const r=await page.evaluate(async(bc)=>{
    const im=Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const w=i.naturalWidth||i.width;return w>240&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));});
    if(im.length<=bc) return {ok:false,why:"no-new-img",n:im.length};
    // 添付した参照サムネ等を避け、面積最大の生成画像を選ぶ
    const g=im.slice().sort((a,b)=>((b.naturalWidth*b.naturalHeight)-(a.naturalWidth*a.naturalHeight)))[0]; let src=g.src;
    if(src.startsWith("data:image")) return {ok:true,b64:src.split(",")[1],src:"data"};
    // googleusercontent のサイズトークンを引き上げ（=s512 / =w400-h300 等 → =s1600）
    let up=src.replace(/=s\d+(-[a-z0-9]+)*$/i,"=s1600").replace(/=w\d+-h\d+(-[a-z0-9]+)*$/i,"=s1600");
    for(const u of [up,src]){ try{ const rr=await fetch(u,{credentials:"include"}); if(!rr.ok) continue; const bl=await rr.blob(); if(bl.size<4000) continue; const b64=await new Promise(res=>{const rd=new FileReader();rd.onload=()=>res(rd.result.split(",")[1]);rd.onerror=()=>res(null);rd.readAsDataURL(bl);}); if(b64) return {ok:true,b64,src:u.slice(0,80)}; }catch(e){} }
    return {ok:false,why:"fetch-failed",src:src.slice(0,80)};
  },beforeCount);
  if(r&&r.ok&&r.b64){ fs.writeFileSync(out,Buffer.from(r.b64,"base64")); console.log("    clean dl via",r.src); return fs.statSync(out).size>4000; }
  console.log("    clean dl miss:",r&&(r.why||r.src)); return false;
}
// 救済: ホバーUIを消すためマウスを退避→img要素のみスクショ
async function dlShot(page,out,beforeCount){
  try{
    await page.mouse.move(3,3); await page.keyboard.press("Escape").catch(()=>{}); await page.waitForTimeout(1200);
    const h=await page.evaluateHandle((bc)=>{const im=Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const w=i.naturalWidth||i.width;return w>240&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));});if(im.length<=bc)return null;return im.slice().sort((a,b)=>((b.naturalWidth*b.naturalHeight)-(a.naturalWidth*a.naturalHeight)))[0];},beforeCount);
    const el=h.asElement(); if(!el) return false;
    await el.scrollIntoViewIfNeeded().catch(()=>{}); await page.mouse.move(3,3); await page.waitForTimeout(600);
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
  for(let k=0;k<N;k++){
    const ci=idx+made; const out=path.join(OUT,`c${String(ci).padStart(2,"0")}.png`); let done=false;
    for(let a=1;a<=2 && !done;a++){
      console.log(`\n[v14b ${ID}] cand ${ci} (approach ${(k%APPROACH.length)+1}) try ${a}`);
      try{
        await startNewChat(page); await page.waitForTimeout(1500); await dismissOverlays(page);
        const att=await attach(page,REF); console.log("  attach:",att); await page.waitForTimeout(2500);
        const before=await imgCount(page);
        await submitPrompt(page,prompt(k));
        const f=await waitImg(page,before,260); await page.waitForTimeout(2500);
        await saveScreenshot(page,`v14b${ID}`,`c${ci}-${a}`).catch(()=>{});
        if(f && (await dlClean(page,out,before) || await dlShot(page,out,before))){ done=true; console.log("  saved",out); }
        else console.warn("  no/dl-fail");
      }catch(e){ console.error("  err",e.message); if(e.message==="QUOTA"){manifest.fail.push({c:ci,reason:"quota"});break;} await page.waitForTimeout(2500); }
    }
    if(done){ manifest.ok.push(ci); made++; } else { manifest.fail.push({c:ci,reason:"no-image"}); if(manifest.fail.find(x=>x.reason==="quota")) break; }
  }
} finally{ fs.writeFileSync(path.join(OUT,"manifest_b.json"),JSON.stringify(manifest,null,2)); try{await ctx.close();}catch{} console.log(`\n[v14b ${ID}] DONE ok=${manifest.ok.length}`); }
})();
