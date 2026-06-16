/**
 * gen_vn.mjs --kind=illust|photo --ver=6 [--scenes=all|1,3] [--prev=5]
 * prompts.mjs を読み、指定版の画像を Gemini ブラウザ生成。前版を引き継ぎ、指定シーンのみ再生成。
 */
import path from "node:path"; import fs from "node:fs";
import { STYLE, SCENES } from "file:///C:/Users/kanet/20260522/safe1/prompts.mjs";
const arg = (k,d)=>{ const a=process.argv.find(x=>x.startsWith(`--${k}=`)); return a? a.split("=")[1] : d; };
const KIND = arg("kind","illust");
const VER  = arg("ver","6");
const PREV = arg("prev","");
const scenesArg = arg("scenes","all");
const SEL = scenesArg==="all" ? [1,2,3,4,5,6] : scenesArg.split(",").map(n=>parseInt(n,10));

const LIB = "C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser, saveScreenshot, dismissOverlays, ensureGeminiLoggedIn } = await import(`file:///${LIB}/browser-helpers.mjs`);
const { startNewChat, selectImageCreationTool, isImageToolActive, submitPrompt } = await import(`file:///${LIB}/gemini-helpers.mjs`);

const BASE = "C:/Users/kanet/20260522/safe1";
const OUT = `${BASE}/images/${KIND}_v${VER}`;
fs.mkdirSync(OUT, { recursive: true });
// 前版引き継ぎ
if (PREV) {
  const prevDir = `${BASE}/images/${KIND}_v${PREV}`;
  for (let i=1;i<=6;i++){ const f=`gen${String(i).padStart(2,"0")}.png`; const src=path.join(prevDir,f);
    if (fs.existsSync(src) && !fs.existsSync(path.join(OUT,f))) fs.copyFileSync(src, path.join(OUT,f)); }
  console.log(`[carry] copied prev v${PREV} -> v${VER}`);
}

const style = STYLE[KIND];
const scenes = SCENES[KIND];
function prompt(i, firstGen){
  const lock = firstGen ? "" : " IMPORTANT: keep the EXACT same rendering style, colour palette, lighting and Japanese-worker character design as the previous image in this chat, so the set looks consistent.";
  return `${scenes[i]}\n\n${style}${lock}`;
}

async function waitImg(page, prev, maxSec=260){ await page.waitForTimeout(6000);
  for(let w=0; w<maxSec/5; w++){
    const c=await page.evaluate(()=>Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const ww=i.naturalWidth||i.width;return ww>220&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));}).length);
    if(c>prev) return true;
    const stop=await page.locator('button[aria-label*="停止"],button[aria-label*="Stop"]').first().isVisible({timeout:500}).catch(()=>false);
    if(!stop && w>2){ const t=await page.evaluate(()=>document.body.innerText); if(/制限に達|利用上限|quota|rate.?limit|後でもう一度/i.test(t)) throw new Error("QUOTA"); return false; }
    await page.waitForTimeout(5000);
  } return false; }
async function dlFetch(page, out){ for(let a=0;a<3;a++){ const b=await page.evaluate(async()=>{const im=Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const w=i.naturalWidth||i.width;return w>220&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));});if(!im.length)return null;const g=im[im.length-1];if(g.src.startsWith("data:image"))return g.src.split(",")[1];try{const r=await fetch(g.src,{credentials:"include"});const bl=await r.blob();return await new Promise(res=>{const rd=new FileReader();rd.onload=()=>res(rd.result.split(",")[1]);rd.onerror=()=>res(null);rd.readAsDataURL(bl);});}catch{try{const c=document.createElement("canvas");c.width=g.naturalWidth;c.height=g.naturalHeight;c.getContext("2d").drawImage(g,0,0);return c.toDataURL("image/png").split(",")[1];}catch{return null;}}});
  if(b){fs.writeFileSync(out,Buffer.from(b,"base64"));if(fs.statSync(out).size>4000)return true;} await page.waitForTimeout(2500);} return false; }
async function dlShot(page,out){ try{ const h=await page.evaluateHandle(()=>{const im=Array.from(document.querySelectorAll("img")).filter(i=>{const w=i.naturalWidth||i.width;return w>220;});return im.length?im[im.length-1]:null;}); const el=h.asElement(); if(!el)return false; await el.scrollIntoViewIfNeeded().catch(()=>{}); await el.screenshot({path:out}); return fs.existsSync(out)&&fs.statSync(out).size>4000; }catch{return false;} }

const manifest = { kind:KIND, ver:VER, sel:SEL, ok:[], fail:[] };
const { ctx, page } = await launchBrowser("gemini", { viewport:{width:1500,height:1000}, acceptDownloads:true });
try{
  await ensureGeminiLoggedIn(page); await page.waitForTimeout(2000); await dismissOverlays(page);
  await startNewChat(page); await page.waitForTimeout(1500); await dismissOverlays(page);
  await selectImageCreationTool(page, { allowProFallback:true }); await page.waitForTimeout(1500);
  let prev=0, firstGen=true;
  for(const sc of SEL){
    const i=sc-1; const out=path.join(OUT, `gen${String(sc).padStart(2,"0")}.png`);
    let done=false;
    for(let a=1;a<=3 && !done;a++){
      console.log(`\n[${KIND} v${VER}] scene ${sc} attempt ${a}`);
      try{
        if(!firstGen && !(await isImageToolActive(page))){ await selectImageCreationTool(page,{allowProFallback:true}); await page.waitForTimeout(600); }
        await submitPrompt(page, prompt(i, firstGen));
        const found=await waitImg(page, prev, 260);
        await page.waitForTimeout(2500);
        await saveScreenshot(page, `v${VER}${KIND}`, `s${sc}-a${a}`).catch(()=>{});
        if(found){ if(await dlFetch(page,out)||await dlShot(page,out)){ prev++; done=true; firstGen=false; console.log(`saved ${out} ${fs.statSync(out).size}b`); } else console.warn("dl fail"); }
        else { console.warn("no image"); await page.waitForTimeout(2500); }
      }catch(e){ console.error(e.message); if(e.message==="QUOTA"){manifest.fail.push({scene:sc,reason:"quota"});break;} await page.waitForTimeout(3000); }
    }
    if(done) manifest.ok.push(sc); else if(!manifest.fail.find(f=>f.scene===sc)) manifest.fail.push({scene:sc,reason:"no-image"});
  }
} finally { fs.writeFileSync(path.join(OUT,"manifest.json"), JSON.stringify(manifest,null,2)); try{await ctx.close();}catch{} console.log(`\n[${KIND} v${VER}] DONE ok=${manifest.ok.length} fail=${manifest.fail.length}`); }
