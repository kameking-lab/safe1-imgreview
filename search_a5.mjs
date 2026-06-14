/** search_a5.mjs : I-A5 元絵探索（高所 急動作で振られ墜落）
 *  機序＝高所作業車の作業床上で、ブームの急操作/急停止/反動・突き上げ等の急動作により
 *  作業者が振られて（あおられて）体勢を崩し作業床（バスケット）から墜落する事故イラスト。
 *  Bing画像検索・別プロファイル anzen・Chrome killしない。新ファイル名(refs/cand_A5)。 */
import fs from "node:fs"; import path from "node:path";
const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);
const OUT="C:/Users/kanet/20260522/safe1/refs/cand_A5"; fs.mkdirSync(OUT,{recursive:true});
const META=path.join(OUT,"_candidates.json");
const saved=[]; const flush=()=>fs.writeFileSync(META,JSON.stringify(saved,null,2));
const QUERIES=[
  "高所作業車 ブーム 急操作 振られ 墜落 災害 イラスト",
  "高所作業車 バスケット 反動 あおられ 作業床 墜落 労働災害 イラスト",
  "高所作業車 急停止 衝撃 振られて 転落 KYT イラスト",
  "高所作業車 作業床 揺れ 振動 放り出される 墜落 注意喚起 イラスト",
  "高所作業車 ブーム 操作ミス 急動作 墜落 災害事例 イラスト",
  "スカイマスター 高所作業車 安全 ポイント 振られ 墜落 イラスト",
  "高所作業車 つき上げ 反動 バスケットから 投げ出される イラスト",
  "aerial work platform sudden jolt worker thrown from basket fall illustration",
  "boom lift sudden movement operator ejected from bucket safety illustration",
  "高所作業車 急旋回 急上昇 反動 墜落 労働災害 イラスト",
  "高所作業車 ブーム 接触 はね返り 作業者 振られ 墜落 イラスト",
  "高所作業車 作業床 体勢崩し 振り落とされ 墜落 ポスター イラスト",
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
