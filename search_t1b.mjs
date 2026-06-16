/** search_t1b.mjs : I-T1 元絵候補(テールゲートリフター 人が昇降板から墜落)を収集
 *  instagram-automation方式・別プロファイル(anzen)・Chromeはkillしない・追加は新ファイル名(refs/cand_T1b)。
 *  Bing画像検索でフルサイズURL(murl)+出所ページ(purl)を集め、墜落事故図を優先して保存。
 *  メタは1件ごとに追記保存(中断しても壊れない)。 */
import fs from "node:fs"; import path from "node:path";
const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);
const OUT="C:/Users/kanet/20260522/safe1/refs/cand_T1b"; fs.mkdirSync(OUT,{recursive:true});
const META=path.join(OUT,"_candidates.json");
const saved=[]; const flush=()=>fs.writeFileSync(META,JSON.stringify(saved,null,2));

const QUERIES=[
  "テールゲートリフター 墜落 災害 イラスト",
  "テールゲートリフター 昇降板 転落 事故 図",
  "陸災防 テールゲートリフター 墜落 注意 イラスト",
  "テールゲートリフター 作業者 墜落 危険 KYT",
  "荷台 昇降装置 作業床 墜落 災害事例 イラスト",
];
const { ctx, page } = await launchBrowser("anzen",{viewport:{width:1500,height:1200}});
const all=[];
try{
  for(const q of QUERIES){
    const url=`https://www.bing.com/images/search?q=${encodeURIComponent(q)}&qft=+filterui:photo-clipart`;
    try{
      await page.goto(url,{waitUntil:"domcontentloaded",timeout:60000}); await page.waitForTimeout(2500);
      const items=await page.evaluate(()=>Array.from(document.querySelectorAll("a.iusc")).slice(0,24).map(a=>{try{return JSON.parse(a.getAttribute("m"));}catch{return null;}}).filter(Boolean).map(m=>({murl:m.murl,purl:m.purl,t:m.t||""})));
      console.log(`[Q] ${q} -> ${items.length}`);
      items.forEach(it=>all.push({q,...it}));
    }catch(e){ console.log("  query err",q,e.message); }
  }
  const seen=new Set(); const uniq=[];
  for(const it of all){ if(it.murl && !seen.has(it.murl)){ seen.add(it.murl); uniq.push(it); } }
  console.log(`UNIQUE: ${uniq.length}`);
  let n=0;
  for(const it of uniq.slice(0,24)){
    try{
      const b=await page.evaluate(async(src)=>{try{const r=await fetch(src);if(!r.ok)return null;const bl=await r.blob();if(bl.size<3000)return null;return await new Promise(res=>{const rd=new FileReader();rd.onload=()=>res(rd.result.split(",")[1]);rd.onerror=()=>res(null);rd.readAsDataURL(bl);});}catch{return null;}}, it.murl);
      if(b){ let ext=(it.murl.split("?")[0].split(".").pop()||"jpg").toLowerCase(); if(ext.length>4||!/^(jpg|jpeg|png|gif|webp)$/.test(ext))ext="jpg"; const f=path.join(OUT,`d${String(++n).padStart(2,"0")}.${ext}`); fs.writeFileSync(f,Buffer.from(b,"base64")); const sz=fs.statSync(f).size; saved.push({file:path.basename(f),size:sz,murl:it.murl,purl:it.purl,t:it.t,q:it.q}); flush(); console.log(`  saved ${path.basename(f)} ${sz}b <- ${it.purl}`); }
    }catch(e){ console.log("  dl err",e.message); }
  }
  console.log(`SAVED ${saved.length} to ${OUT}`);
} finally{ try{await ctx.close();}catch{} console.log("SEARCH DONE"); }
