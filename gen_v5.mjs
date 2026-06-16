/**
 * gen_v5.mjs  --kind=illust|photo
 * v5用イラスト/写真を Gemini ブラウザ(画像生成/Nano Banana系)で6枚生成。
 * - APIキー不使用。.cache/browser-profile-gemini を流用。chrome は kill しない。
 * - 同一チャットで6枚→画風統一(各プロンプトに画風ロック)。日本語は焼き込まない。
 * - DL: page内fetch(複数リトライ)→失敗時 <img> 要素スクショ救済。
 * 出力: safe1/images/{kind}_v5/gen01..06.png + manifest.json
 */
import path from "node:path"; import fs from "node:fs";
const KIND = (process.argv.find(a=>a.startsWith("--kind="))||"--kind=illust").split("=")[1];
const LIB = "C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser, saveScreenshot, dismissOverlays, ensureGeminiLoggedIn } = await import(`file:///${LIB}/browser-helpers.mjs`);
const { startNewChat, selectImageCreationTool, isImageToolActive, submitPrompt } = await import(`file:///${LIB}/gemini-helpers.mjs`);

const OUT = `C:/Users/kanet/20260522/safe1/images/${KIND}_v5`;
fs.mkdirSync(OUT, { recursive: true });

const STYLE_ILLUST =
  "Professional occupational-safety training ILLUSTRATION, modern semi-realistic style: full color, confident clean linework with soft cel-shading, subtle gradients, strong depth and perspective, a dynamic cinematic three-quarter camera angle that captures the split-second a near-miss unfolds with a clear sense of motion. " +
  "The worker and the equipment are rendered in the SAME illustration style and the SAME light — fully integrated, never a flat pasted-on cut-out, never a black silhouette. " +
  "The worker wears correct PPE: hard hat, hi-visibility vest or work jacket, safety boots. The subject fills the frame edge to edge with minimal empty background. Landscape 3:2 composition. " +
  "NO text, NO letters, NO numbers, NO logos, NO watermark. No blood, no gore, no injury — show the dangerous hazard moment only.";

const STYLE_PHOTO =
  "Photorealistic DOCUMENTARY PHOTOGRAPH at a real Japanese worksite / exhibition-hall build-out. Natural light, realistic colours, shallow depth of field, candid photojournalistic feel, 35mm look. " +
  "The worker wears correct Japanese-site PPE: helmet, hi-vis vest or work jacket, safety boots. To keep the face and hands natural, show the worker from the SIDE or from BEHIND at mid-distance, helmet on, face never a close-up. " +
  "The subject fills the frame. Landscape 3:2 composition. NO text overlays, NO logos, NO watermark. No blood, no injury — capture the dangerous near-miss moment only.";

const SCENES_ILLUST = [
 "Scene: the rear of a flat-bed truck with a hydraulic tail-lift platform (tailgate lifter). A worker in hard hat and hi-vis is steadying a 200-litre steel drum on the platform but has lost his balance and is stepping backward off the rear edge — which has NO guardrail — arms flailing, body tipping, the instant before he falls to the ground.",
 "Scene: close on the rear of a truck where the tail-lift platform is partway up, between the ground and the truck bed. A worker in hard hat and hi-vis has his safety boot caught in the narrowing gap between the moving platform edge and the truck bed — the dangerous pinch moment, his body twisting in reaction.",
 "Scene: a tail-lift platform with a step/slope. A tall wheeled roll-cage cart (metal mesh roll box pallet loaded with goods) is tipping and toppling sideways toward a worker in hard hat and hi-vis, who recoils with arms raised as the heavy cage leans over and down onto him.",
 "Scene: high in the air, the basket of a boom-type aerial work platform (cherry picker). A worker in hard hat and a full-body fall-arrest harness is leaning his upper body far out over the basket's guardrail to reach the work, dangerously off-balance, and his harness lanyard hook dangles UNCLIPPED and loose — the instant before a fall.",
 "Scene: a boom-type aerial work platform on uneven, sloping ground with its outrigger stabiliser legs NOT deployed. The whole machine is tilting and beginning to tip over to one side; the worker in the raised basket grips the rail as it leans — caught mid-tip.",
 "Scene: the basket of a boom-type aerial work platform raised up close beneath a steel ceiling truss / horizontal overhead beam. The worker in hard hat and harness is about to be caught in the shrinking gap between the basket's top rail and the beam just above his head — the pinch moment.",
];
const SCENES_PHOTO = SCENES_ILLUST; // 同一の状況、スタイルだけ差し替え

const STYLE = KIND==="photo" ? STYLE_PHOTO : STYLE_ILLUST;
const SCENES = KIND==="photo" ? SCENES_PHOTO : SCENES_ILLUST;

function prompt(i){
  const lock = i===0
    ? ""
    : " IMPORTANT: keep the EXACT same rendering style, colour palette, lighting, line/texture quality and worker character design as the previous images in this chat, so all six look like one consistent set.";
  return `${SCENES[i]}\n\n${STYLE}${lock}`;
}

async function waitImg(page, prev, maxSec=260){
  await page.waitForTimeout(6000);
  for(let w=0; w<maxSec/5; w++){
    const c = await page.evaluate(()=>Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const ww=i.naturalWidth||i.width;return ww>220&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));}).length);
    if(c>prev) return true;
    const stop = await page.locator('button[aria-label*="停止"],button[aria-label*="Stop"]').first().isVisible({timeout:500}).catch(()=>false);
    if(!stop && w>2){ const t=await page.evaluate(()=>document.body.innerText); if(/制限に達|利用上限|quota|rate.?limit|後でもう一度/i.test(t)) throw new Error("QUOTA"); return false; }
    await page.waitForTimeout(5000);
  }
  return false;
}

async function dlFetch(page, out){
  for(let attempt=0; attempt<3; attempt++){
    const b = await page.evaluate(async ()=>{
      const im = Array.from(document.querySelectorAll("img")).filter(i=>{const s=i.src||"";const w=i.naturalWidth||i.width;return w>220&&(s.includes("googleusercontent")||s.startsWith("blob:")||s.startsWith("data:image"));});
      if(!im.length) return null;
      const g = im[im.length-1];
      if(g.src.startsWith("data:image")) return g.src.split(",")[1];
      try{ const r=await fetch(g.src,{credentials:"include"}); const bl=await r.blob(); return await new Promise(res=>{const rd=new FileReader();rd.onload=()=>res(rd.result.split(",")[1]);rd.onerror=()=>res(null);rd.readAsDataURL(bl);}); }
      catch{ try{ const c=document.createElement("canvas"); c.width=g.naturalWidth; c.height=g.naturalHeight; c.getContext("2d").drawImage(g,0,0); return c.toDataURL("image/png").split(",")[1]; }catch{ return null; } }
    });
    if(b){ fs.writeFileSync(out, Buffer.from(b,"base64")); if(fs.statSync(out).size>4000) return true; }
    await page.waitForTimeout(2500);
  }
  return false;
}

async function dlElementShot(page, out){
  try{
    const handle = await page.evaluateHandle(()=>{
      const im = Array.from(document.querySelectorAll("img")).filter(i=>{const w=i.naturalWidth||i.width;return w>220;});
      return im.length? im[im.length-1] : null;
    });
    const el = handle.asElement();
    if(!el) return false;
    await el.scrollIntoViewIfNeeded().catch(()=>{});
    await el.screenshot({ path: out });
    return fs.existsSync(out) && fs.statSync(out).size>4000;
  }catch{ return false; }
}

const manifest = { kind: KIND, ok: [], fail: [] };
const { ctx, page } = await launchBrowser("gemini", { viewport:{width:1500,height:1000}, acceptDownloads:true });
try{
  await ensureGeminiLoggedIn(page);
  await page.waitForTimeout(2000); await dismissOverlays(page);
  await startNewChat(page); await page.waitForTimeout(1500); await dismissOverlays(page);
  await selectImageCreationTool(page, { allowProFallback:true }); await page.waitForTimeout(1500);
  let prev = 0;
  for(let i=0;i<SCENES.length;i++){
    const out = path.join(OUT, `gen${String(i+1).padStart(2,"0")}.png`);
    let done=false;
    for(let a=1;a<=3 && !done;a++){
      console.log(`\n[${KIND}] scene ${i+1}/6 attempt ${a}`);
      try{
        if(i>0 && !(await isImageToolActive(page))){ await selectImageCreationTool(page,{allowProFallback:true}); await page.waitForTimeout(600); }
        await submitPrompt(page, prompt(i));
        const found = await waitImg(page, prev, 260);
        await page.waitForTimeout(2500);
        await saveScreenshot(page, `v5${KIND}`, `s${i+1}-a${a}`).catch(()=>{});
        if(found){
          if(await dlFetch(page, out) || await dlElementShot(page, out)){ prev++; done=true; console.log(`[${KIND}] saved ${out} (${fs.statSync(out).size}b)`); }
          else console.warn(`[${KIND}] dl failed s${i+1} a${a}`);
        } else { console.warn(`[${KIND}] no image s${i+1} a${a}`); await page.waitForTimeout(2500); }
      }catch(e){ console.error(`[${KIND}] err s${i+1}: ${e.message}`); if(e.message==="QUOTA"){ manifest.fail.push({scene:i+1,reason:"quota"}); break; } await page.waitForTimeout(3000); }
    }
    if(done) manifest.ok.push({scene:i+1,file:path.basename(out)});
    else if(!manifest.fail.find(f=>f.scene===i+1)) manifest.fail.push({scene:i+1,reason:"no-image"});
  }
} finally {
  fs.writeFileSync(path.join(OUT,"manifest.json"), JSON.stringify(manifest,null,2));
  try{ await ctx.close(); }catch{}
  console.log(`\n[${KIND}] DONE ok=${manifest.ok.length} fail=${manifest.fail.length}`);
}
