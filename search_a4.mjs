/** search_a4.mjs : I-A4 元絵探索（高所作業車 安全帯未使用で作業床から墜落）
 *  Bing画像検索・別プロファイル anzen・Chrome killしない。新ファイル名(refs/cand_A4)。 */
import fs from "node:fs"; import path from "node:path";
const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);
const OUT="C:/Users/kanet/20260522/safe1/refs/cand_A4"; fs.mkdirSync(OUT,{recursive:true});
const META=path.join(OUT,"_candidates.json");
const saved=[]; const flush=()=>fs.writeFileSync(META,JSON.stringify(saved,null,2));
const QUERIES=[
  "高所作業車 安全帯 未使用 作業床 墜落 災害 イラスト",
  "高所作業車 バスケット 身を乗り出し 墜落 労働災害 イラスト",
  "高所作業車 作業床 フルハーネス 未着用 墜落 死亡災害 イラスト",
  "高所作業車 墜落 安全帯 命綱 未使用 KYT イラスト",
  "高所作業車 バスケットから墜落 注意喚起 ポスター イラスト",
  "高所作業車 作業床 乗り出し 転落 厚生労働省 災害事例 イラスト",
  "aerial work platform fall from basket no harness worker accident illustration",
  "boom lift bucket fall worker not wearing harness safety illustration",
  "高所作業車 墜落 安全帯 かけ忘れ 労働災害 イラスト",
  "高所作業車 作業床 墜落 はみ出し 安全帯未使用 災害事例 イラスト",
];
const { ctx, page } = await launchBrowser("anzen",{viewport:{width:1500,height:1200}});
const all=[];
try{
  for(const q of QUERIES){
    const url=`https://www.bing.com/images/search?q=${encodeURIComponent(q)}`;
    try{ await page.goto(url,{waitUntil:"domcontentloaded",timeout:60000}); await page.waitForTimeout(2200);
      const items=await page.evaluate(()=>Array.from(document.querySelectorAll("a.iusc")).slice(0,30).map(a=>{try{return JSON.parse(a.getAttribute("m"));}catch{return null;}}).filter(Boolean).map(m=>({murl:m.murl,purl:m.purl,t:m.t||""})));
      console.log(`[Q] ${q} -> ${items.length}`); items.forEach(it=>all.push({q,...it}));
    }catch(e){ console.log("  query err",q,e.message); }
  }
  const seen=new Set(); const uniq=[];
  for(const it of all){ if(it.murl && !seen.has(it.murl)){ seen.add(it.murl); uniq.push(it); } }
  console.log(`UNIQUE: ${uniq.length}`);
  let n=0;
  for(const it of uniq.slice(0,48)){
    try{
      const resp=await page.goto(it.murl,{waitUntil:"commit",timeout:25000}).catch(()=>null);
      if(!resp || !resp.ok()) continue;
      const ct=(resp.headers()["content-type"]||""); if(!/image\//.test(ct)) continue;
      const buf=await resp.body().catch(()=>null);
      if(!buf || buf.length<4000) continue;
      let ext=(ct.split("/")[1]||"jpg").split(";")[0].toLowerCase(); if(!/^(jpg|jpeg|png|gif|webp)$/.test(ext))ext="jpg";
      const f=path.join(OUT,`z${String(++n).padStart(2,"0")}.${ext}`); fs.writeFileSync(f,buf);
      saved.push({file:path.basename(f),size:buf.length,murl:it.murl,purl:it.purl,t:it.t,q:it.q}); flush();
      console.log(`  saved ${path.basename(f)} ${buf.length}b <- ${it.purl}`);
    }catch(e){ console.log("  dl err",e.message); }
  }
  console.log(`SAVED ${saved.length} to ${OUT}`);
} finally{ try{await ctx.close();}catch{} console.log("SEARCH DONE"); }
