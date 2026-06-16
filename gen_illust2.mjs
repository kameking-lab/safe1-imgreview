// 事例②(はさまれ)の再生成。2バリアント生成 → 最良を採用。
import path from "node:path"; import fs from "node:fs";
const LIB = "C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser, saveScreenshot, dismissOverlays, ensureGeminiLoggedIn } = await import(`file:///${LIB}/browser-helpers.mjs`);
const { startNewChat, selectImageCreationTool, isImageToolActive, submitPrompt } = await import(`file:///${LIB}/gemini-helpers.mjs`);
const OUT = "C:/Users/kanet/20260522/safe1/images/gen"; fs.mkdirSync(OUT, { recursive: true });
const STYLE = "Black and white technical line drawing, clean thin vector outlines on a pure white background, industrial occupational-safety manual illustration style, simple schematic, side view. The human worker is drawn as a solid black silhouette. Absolutely NO text, no letters, no numbers, no labels, no watermark. Minimal, generous white space, single scene centered. Match a consistent clean line-art style.";
const VARIANTS = [
  // A: 足が昇降板と地面のすき間にはさまれ(下降中)
  "The rear of a delivery truck with a tail-lift platform that is descending toward the ground and is now just above ground level. A worker silhouette stands next to it and his foot is caught and pinched in the narrow gap between the lowering edge of the platform and the ground. Draw the trapped foot and the pinch gap clearly, with a pained posture.",
  // B: 足が昇降板と荷台のすき間にはさまれ(上昇し荷台高さ)
  "The rear of a delivery truck. The tail-lift platform has risen to the same height as the truck bed, leaving a narrow horizontal gap between the platform edge and the truck-bed edge. A worker silhouette stands on the platform and his foot is caught and pinched in that narrow gap between the platform and the truck bed. Show the pinch point and the trapped foot clearly.",
];
const FILES = ["gen02a.png","gen02b.png"];
async function waitImg(page, prev, maxSec=240){ await page.waitForTimeout(6000);
  for(let w=0; w<maxSec/5; w++){ const c=await page.evaluate(()=>Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const ww=i.naturalWidth||i.width;return ww>200&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));}).length);
    if(c>prev) return true; const stop=await page.locator('button[aria-label*="停止"],button[aria-label*="Stop"]').first().isVisible({timeout:500}).catch(()=>false);
    if(!stop&&w>2){const t=await page.evaluate(()=>document.body.innerText); if(/制限に達|quota|rate.?limit/i.test(t)) throw new Error("QUOTA"); return false;} await page.waitForTimeout(5000);} return false; }
async function dl(page,out){ const b=await page.evaluate(async()=>{const im=Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const w=i.naturalWidth||i.width;return w>200&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));}); if(!im.length)return null; const g=im[im.length-1]; if(g.src.startsWith("data:image"))return g.src.split(",")[1]; try{const r=await fetch(g.src,{credentials:"include"});const bl=await r.blob();return await new Promise(res=>{const rd=new FileReader();rd.onload=()=>res(rd.result.split(",")[1]);rd.onerror=()=>res(null);rd.readAsDataURL(bl);});}catch{return null;}}); if(!b)return false; fs.writeFileSync(out,Buffer.from(b,"base64")); return fs.statSync(out).size>1000; }
const { ctx, page } = await launchBrowser("gemini", { viewport:{width:1400,height:900}, acceptDownloads:true });
try{ await ensureGeminiLoggedIn(page); await page.waitForTimeout(2000); await dismissOverlays(page); await startNewChat(page); await page.waitForTimeout(1500); await dismissOverlays(page); await selectImageCreationTool(page,{allowProFallback:true}); await page.waitForTimeout(1500);
  let prev=0;
  for(let i=0;i<VARIANTS.length;i++){ const out=path.join(OUT,FILES[i]); let done=false;
    for(let a=1;a<=3&&!done;a++){ console.log(`variant ${i+1} attempt ${a}`); try{ if(i>0&&!(await isImageToolActive(page))){await selectImageCreationTool(page,{allowProFallback:true});await page.waitForTimeout(500);} await submitPrompt(page, `${VARIANTS[i]}\n\n${STYLE}`); const f=await waitImg(page,prev,240); await page.waitForTimeout(2500); await saveScreenshot(page,"gen2",`v${i+1}-a${a}`).catch(()=>{}); if(f&&await dl(page,out)){prev++;done=true;console.log("saved",out);} else {await page.waitForTimeout(3000);} }catch(e){console.error(e.message); if(e.message==="QUOTA")break; await page.waitForTimeout(3000);} } }
} finally { try{await ctx.close();}catch{} console.log("DONE"); }
