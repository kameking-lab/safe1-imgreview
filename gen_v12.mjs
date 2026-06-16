/** gen_v12.mjs --case=1 --kind=illust|photo [--n=5]
 * 1事例の5アプローチ画像を生成。images/cand_v12/case{N}/{kind}/01..05.png */
import path from "node:path"; import fs from "node:fs";
import { STYLE, APPROACH, SCN } from "file:///C:/Users/kanet/20260522/safe1/prompts_v12.mjs";
const arg=(k,d)=>{const a=process.argv.find(x=>x.startsWith(`--${k}=`));return a?a.split("=")[1]:d;};
const CASE=arg("case","1"), KIND=arg("kind","illust"), N=parseInt(arg("n","5"),10);
const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser, saveScreenshot, dismissOverlays, ensureGeminiLoggedIn } = await import(`file:///${LIB}/browser-helpers.mjs`);
const { startNewChat, selectImageCreationTool, isImageToolActive, submitPrompt } = await import(`file:///${LIB}/gemini-helpers.mjs`);
const OUT=`C:/Users/kanet/20260522/safe1/images/cand_v12/case${CASE}/${KIND}`;
fs.mkdirSync(OUT,{recursive:true});
const scn=SCN[CASE], style=STYLE[KIND];
function prompt(i){ const cons=" Keep the same Japanese worker character and the same Japanese setting/equipment across this set, but change the camera/composition as instructed so the five images are clearly different."; return `${scn}\n\n${APPROACH[i]}\n\n${style}${i>0?cons:""}`; }

async function waitImg(page,prev,maxSec=260){ await page.waitForTimeout(6000);
  for(let w=0;w<maxSec/5;w++){ const c=await page.evaluate(()=>Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const ww=i.naturalWidth||i.width;return ww>220&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));}).length);
    if(c>prev) return true; const stop=await page.locator('button[aria-label*="停止"],button[aria-label*="Stop"]').first().isVisible({timeout:500}).catch(()=>false);
    if(!stop&&w>2){const t=await page.evaluate(()=>document.body.innerText); if(/制限に達|利用上限|quota|rate.?limit|後でもう一度/i.test(t)) throw new Error("QUOTA"); return false;} await page.waitForTimeout(5000);} return false; }
async function dlFetch(page,out){ for(let a=0;a<3;a++){ const b=await page.evaluate(async()=>{const im=Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const w=i.naturalWidth||i.width;return w>220&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));});if(!im.length)return null;const g=im[im.length-1];if(g.src.startsWith("data:image"))return g.src.split(",")[1];try{const r=await fetch(g.src,{credentials:"include"});const bl=await r.blob();return await new Promise(res=>{const rd=new FileReader();rd.onload=()=>res(rd.result.split(",")[1]);rd.onerror=()=>res(null);rd.readAsDataURL(bl);});}catch{return null;}});
  if(b){fs.writeFileSync(out,Buffer.from(b,"base64"));if(fs.statSync(out).size>4000)return true;} await page.waitForTimeout(2200);} return false; }
async function dlShot(page,out){ try{ const h=await page.evaluateHandle(()=>{const im=Array.from(document.querySelectorAll("img")).filter(i=>{const w=i.naturalWidth||i.width;return w>220;});return im.length?im[im.length-1]:null;}); const el=h.asElement(); if(!el)return false; await el.scrollIntoViewIfNeeded().catch(()=>{}); await el.screenshot({path:out}); return fs.existsSync(out)&&fs.statSync(out).size>4000; }catch{return false;} }

const manifest={case:CASE,kind:KIND,ok:[],fail:[]};
const { ctx, page } = await launchBrowser("gemini",{viewport:{width:1500,height:1000},acceptDownloads:true});
try{
  await ensureGeminiLoggedIn(page); await page.waitForTimeout(2000); await dismissOverlays(page);
  await startNewChat(page); await page.waitForTimeout(1500); await dismissOverlays(page);
  await selectImageCreationTool(page,{allowProFallback:true}); await page.waitForTimeout(1500);
  let prev=0, first=true;
  for(let i=0;i<N;i++){ const out=path.join(OUT,`${String(i+1).padStart(2,"0")}.png`); let done=false;
    for(let a=1;a<=2&&!done;a++){ console.log(`\n[c${CASE} ${KIND}] approach ${i+1} try ${a}`);
      try{ if(!first&&!(await isImageToolActive(page))){await selectImageCreationTool(page,{allowProFallback:true});await page.waitForTimeout(600);}
        await submitPrompt(page,prompt(i)); const f=await waitImg(page,prev,260); await page.waitForTimeout(2200);
        await saveScreenshot(page,`v12c${CASE}${KIND}`,`a${i+1}-${a}`).catch(()=>{});
        if(f){ if(await dlFetch(page,out)||await dlShot(page,out)){prev++;done=true;first=false;console.log(`saved ${out}`);} else console.warn("dl fail"); }
        else { console.warn("no image"); await page.waitForTimeout(2000);} }
      catch(e){ console.error(e.message); if(e.message==="QUOTA"){manifest.fail.push({a:i+1,reason:"quota"});break;} await page.waitForTimeout(2500);} }
    if(done) manifest.ok.push(i+1); else if(!manifest.fail.find(x=>x.a===i+1)) manifest.fail.push({a:i+1,reason:"no-image"});
  }
} finally { fs.writeFileSync(path.join(OUT,"manifest.json"),JSON.stringify(manifest,null,2)); try{await ctx.close();}catch{} console.log(`\n[c${CASE} ${KIND}] DONE ok=${manifest.ok.length} fail=${manifest.fail.length}`); }
