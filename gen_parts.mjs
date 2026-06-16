/** gen_parts.mjs : M2用パーツを無地白背景・側面視・統一画風で別々に生成 */
import path from "node:path"; import fs from "node:fs";
const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser, saveScreenshot, dismissOverlays, ensureGeminiLoggedIn } = await import(`file:///${LIB}/browser-helpers.mjs`);
const { startNewChat, selectImageCreationTool, isImageToolActive, submitPrompt } = await import(`file:///${LIB}/gemini-helpers.mjs`);
const OUT="C:/Users/kanet/20260522/safe1/images/proto/parts"; fs.mkdirSync(OUT,{recursive:true});
const STYLE=" Clean modern FLAT vector-style illustration, simple even flat lighting, bold clean outlines, limited flat colours, on a PURE PLAIN WHITE background (#ffffff), the subject centered with margin, strict SIDE PROFILE (side elevation), no ground shadow, no text, no letters, no numbers, no logos, no watermark.";
const PARTS=[
 ["A","A Japanese flat-bed cargo truck in strict SIDE PROFILE facing left, with a folding hydraulic tail-lift platform at the rear (right side) lowered to a slightly tilted position. NO people, NO cargo loaded."+STYLE],
 ["B","A single heavy industrial machine mounted on a low wheeled steel base, heavy and bulky (about 1.2 tonnes look), in strict SIDE PROFILE, isolated alone. NO truck, NO people."+STYLE],
 ["C1","A single Japanese male worker wearing a white safety helmet WITH CHIN STRAP, hi-vis vest, work trousers and safety boots, in strict SIDE PROFILE, crouching low and bracing as if pushed/knocked BACKWARD and DOWN, one arm raised to protect his head, body leaning back. Isolated alone, no equipment."+STYLE],
 ["C2","A single Japanese male worker (white helmet with chin strap, hi-vis vest, safety boots) in strict SIDE PROFILE, falling/being crushed downward, knees buckling, both arms up defensively. Isolated alone, no equipment."+STYLE],
];
async function waitImg(page,prev,maxSec=240){await page.waitForTimeout(6000);for(let w=0;w<maxSec/5;w++){const c=await page.evaluate(()=>Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const ww=i.naturalWidth||i.width;return ww>220&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));}).length);if(c>prev)return true;const stop=await page.locator('button[aria-label*="停止"],button[aria-label*="Stop"]').first().isVisible({timeout:500}).catch(()=>false);if(!stop&&w>2){return false;}await page.waitForTimeout(5000);}return false;}
async function dl(page,out){for(let a=0;a<3;a++){const b=await page.evaluate(async()=>{const im=Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const w=i.naturalWidth||i.width;return w>220&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));});if(!im.length)return null;const g=im[im.length-1];if(g.src.startsWith("data:image"))return g.src.split(",")[1];try{const r=await fetch(g.src,{credentials:"include"});const bl=await r.blob();return await new Promise(res=>{const rd=new FileReader();rd.onload=()=>res(rd.result.split(",")[1]);rd.onerror=()=>res(null);rd.readAsDataURL(bl);});}catch{return null;}});if(b){fs.writeFileSync(out,Buffer.from(b,"base64"));if(fs.statSync(out).size>4000)return true;}await page.waitForTimeout(2200);}return false;}
const { ctx, page } = await launchBrowser("gemini",{viewport:{width:1500,height:1000},acceptDownloads:true});
try{ await ensureGeminiLoggedIn(page); await page.waitForTimeout(2000); await dismissOverlays(page); await startNewChat(page); await page.waitForTimeout(1500); await dismissOverlays(page); await selectImageCreationTool(page,{allowProFallback:true}); await page.waitForTimeout(1500);
  let prev=0,first=true;
  for(const [name,p] of PARTS){ const out=path.join(OUT,`${name}.png`); let done=false;
    for(let a=1;a<=2&&!done;a++){ console.log(`[parts] ${name} try ${a}`); try{ if(!first&&!(await isImageToolActive(page))){await selectImageCreationTool(page,{allowProFallback:true});await page.waitForTimeout(600);} await submitPrompt(page,p); const f=await waitImg(page,prev,240); await page.waitForTimeout(2200); await saveScreenshot(page,"parts",`${name}-${a}`).catch(()=>{}); if(f&&await dl(page,out)){prev++;done=true;first=false;console.log("saved",out);} else await page.waitForTimeout(2000); }catch(e){console.error(e.message);await page.waitForTimeout(2000);} }
  }
} finally{ try{await ctx.close();}catch{} console.log("PARTS DONE"); }
