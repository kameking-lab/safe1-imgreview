/** search_t1c.mjs : I-T1 元絵 追加探索(陸災防/厚労省の TGL 墜落"災害事例図"を狙い撃ち)
 *  別プロファイル(anzen)・Chrome killしない・追加は新ファイル名(refs/cand_T1c)。メタ逐次保存。 */
import fs from "node:fs"; import path from "node:path";
const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);
const OUT="C:/Users/kanet/20260522/safe1/refs/cand_T1c"; fs.mkdirSync(OUT,{recursive:true});
const META=path.join(OUT,"_candidates.json");
const saved=[]; const flush=()=>fs.writeFileSync(META,JSON.stringify(saved,null,2));
const QUERIES=[
  "テールゲートリフター 災害事例 昇降板 墜落 リフト上昇中",
  "テールゲートリフター 労働災害 事例 昇降装置 転落 厚生労働省",
  "tail lift loading platform worker fall hazard illustration safety",
  "テールゲートリフター プラットフォーム 端部 墜落 注意喚起 イラスト",
];
const { ctx, page } = await launchBrowser("anzen",{viewport:{width:1500,height:1200}});
const all=[];
try{
  for(const q of QUERIES){
    const url=`https://www.bing.com/images/search?q=${encodeURIComponent(q)}&qft=+filterui:photo-clipart`;
    try{ await page.goto(url,{waitUntil:"domcontentloaded",timeout:60000}); await page.waitForTimeout(2500);
      const items=await page.evaluate(()=>Array.from(document.querySelectorAll("a.iusc")).slice(0,24).map(a=>{try{return JSON.parse(a.getAttribute("m"));}catch{return null;}}).filter(Boolean).map(m=>({murl:m.murl,purl:m.purl,t:m.t||""})));
      console.log(`[Q] ${q} -> ${items.length}`); items.forEach(it=>all.push({q,...it}));
    }catch(e){ console.log("  query err",q,e.message); }
  }
  const seen=new Set(); const uniq=[];
  for(const it of all){ if(it.murl && !seen.has(it.murl)){ seen.add(it.murl); uniq.push(it); } }
  console.log(`UNIQUE: ${uniq.length}`);
  let n=0;
  for(const it of uniq.slice(0,24)){
    try{
      const b=await page.evaluate(async(src)=>{try{const r=await fetch(src);if(!r.ok)return null;const bl=await r.blob();if(bl.size<3000)return null;return await new Promise(res=>{const rd=new FileReader();rd.onload=()=>res(rd.result.split(",")[1]);rd.onerror=()=>res(null);rd.readAsDataURL(bl);});}catch{return null;}}, it.murl);
      if(b){ let ext=(it.murl.split("?")[0].split(".").pop()||"jpg").toLowerCase(); if(ext.length>4||!/^(jpg|jpeg|png|gif|webp)$/.test(ext))ext="jpg"; const f=path.join(OUT,`e${String(++n).padStart(2,"0")}.${ext}`); fs.writeFileSync(f,Buffer.from(b,"base64")); const sz=fs.statSync(f).size; saved.push({file:path.basename(f),size:sz,murl:it.murl,purl:it.purl,t:it.t,q:it.q}); flush(); console.log(`  saved ${path.basename(f)} ${sz}b <- ${it.purl}`); }
    }catch(e){ console.log("  dl err",e.message); }
  }
  console.log(`SAVED ${saved.length} to ${OUT}`);
} finally{ try{await ctx.close();}catch{} console.log("SEARCH DONE"); }
