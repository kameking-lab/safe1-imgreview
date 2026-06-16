// 単発再生成: node gen_one.mjs <outdir> <outname> "<prompt>"
import path from "node:path"; import fs from "node:fs";
const [,, OUTDIR, OUTNAME, PROMPT] = process.argv;
const LIB = "C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser, saveScreenshot, dismissOverlays, ensureGeminiLoggedIn } = await import(`file:///${LIB}/browser-helpers.mjs`);
const { startNewChat, selectImageCreationTool, submitPrompt } = await import(`file:///${LIB}/gemini-helpers.mjs`);
fs.mkdirSync(OUTDIR, { recursive: true });
const out = path.join(OUTDIR, OUTNAME);
async function waitImg(page){ await page.waitForTimeout(6000);
  for(let w=0;w<52;w++){ const c=await page.evaluate(()=>Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const ww=i.naturalWidth||i.width;return ww>220&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));}).length);
    if(c>0) return true; const stop=await page.locator('button[aria-label*="停止"],button[aria-label*="Stop"]').first().isVisible({timeout:500}).catch(()=>false);
    if(!stop&&w>2){return false;} await page.waitForTimeout(5000);} return false; }
async function dl(page,o){ for(let a=0;a<3;a++){ const b=await page.evaluate(async()=>{const im=Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const w=i.naturalWidth||i.width;return w>220&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));});if(!im.length)return null;const g=im[im.length-1];if(g.src.startsWith("data:image"))return g.src.split(",")[1];try{const r=await fetch(g.src,{credentials:"include"});const bl=await r.blob();return await new Promise(res=>{const rd=new FileReader();rd.onload=()=>res(rd.result.split(",")[1]);rd.onerror=()=>res(null);rd.readAsDataURL(bl);});}catch{return null;}});
  if(b){fs.writeFileSync(o,Buffer.from(b,"base64"));if(fs.statSync(o).size>4000)return true;} await page.waitForTimeout(2500);} return false; }
const { ctx, page } = await launchBrowser("gemini", { viewport:{width:1500,height:1000}, acceptDownloads:true });
try{ await ensureGeminiLoggedIn(page); await page.waitForTimeout(2000); await dismissOverlays(page); await startNewChat(page); await page.waitForTimeout(1500); await dismissOverlays(page); await selectImageCreationTool(page,{allowProFallback:true}); await page.waitForTimeout(1500);
  for(let a=1;a<=3;a++){ console.log("attempt",a); await submitPrompt(page, PROMPT); const f=await waitImg(page); await page.waitForTimeout(2500); await saveScreenshot(page,"one",`a${a}`).catch(()=>{}); if(f && await dl(page,out)){ console.log("saved",out,fs.statSync(out).size); break; } await page.waitForTimeout(2500); }
} finally{ try{await ctx.close();}catch{} console.log("ONE DONE"); }
