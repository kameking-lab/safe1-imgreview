/** search_t2b.mjs : I-T2 元絵 追加探索（TGL 昇降板と荷台の間に頭部はさまれ）
 *  robust DL = page.goto(murl) のレスポンスbodyを使用。別プロファイル(anzen)・Chrome killしない・新ファイル名(refs/cand_T2b)。 */
import fs from "node:fs"; import path from "node:path";
const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);
const OUT="C:/Users/kanet/20260522/safe1/refs/cand_T2b"; fs.mkdirSync(OUT,{recursive:true});
const META=path.join(OUT,"_candidates.json");
const saved=[]; const flush=()=>fs.writeFileSync(META,JSON.stringify(saved,null,2));
const QUERIES=[
  "テールゲートリフター 挟まれ 災害事例 昇降板 荷台 すき間",
  "テールゲートリフター 上昇 挟まれ 頭部 注意 イラスト",
  "貨物自動車 昇降設備 挟まれ 災害 厚生労働省 STOP",
  "テールゲートリフター 危険ポイント はさまれ KY 図解",
  "tail lift gate platform pinch point crush between bed warning illustration",
  "陸災防 テールゲートリフター 安全 ポイント 挟まれ 墜落",
];
const { ctx, page } = await launchBrowser("anzen",{viewport:{width:1500,height:1200}});
const all=[];
try{
  for(const q of QUERIES){
    const url=`https://www.bing.com/images/search?q=${encodeURIComponent(q)}&qft=+filterui:photo-clipart`;
    try{ await page.goto(url,{waitUntil:"domcontentloaded",timeout:60000}); await page.waitForTimeout(2200);
      const items=await page.evaluate(()=>Array.from(document.querySelectorAll("a.iusc")).slice(0,28).map(a=>{try{return JSON.parse(a.getAttribute("m"));}catch{return null;}}).filter(Boolean).map(m=>({murl:m.murl,purl:m.purl,t:m.t||""})));
      console.log(`[Q] ${q} -> ${items.length}`); items.forEach(it=>all.push({q,...it}));
    }catch(e){ console.log("  query err",q,e.message); }
  }
  const seen=new Set(); const uniq=[];
  for(const it of all){ if(it.murl && !seen.has(it.murl)){ seen.add(it.murl); uniq.push(it); } }
  console.log(`UNIQUE: ${uniq.length}`);
  let n=0;
  for(const it of uniq.slice(0,40)){
    try{
      const resp=await page.goto(it.murl,{waitUntil:"commit",timeout:25000}).catch(()=>null);
      if(!resp || !resp.ok()){ console.log("  skip(noresp)",it.murl.slice(0,60)); continue; }
      const ct=(resp.headers()["content-type"]||""); if(!/image\//.test(ct)){ console.log("  skip(notimg)",ct,it.murl.slice(0,60)); continue; }
      const buf=await resp.body().catch(()=>null);
      if(!buf || buf.length<3000){ console.log("  skip(small)"); continue; }
      let ext=(ct.split("/")[1]||"jpg").split(";")[0].toLowerCase(); if(!/^(jpg|jpeg|png|gif|webp)$/.test(ext))ext="jpg";
      const f=path.join(OUT,`u${String(++n).padStart(2,"0")}.${ext}`); fs.writeFileSync(f,buf); const sz=buf.length;
      saved.push({file:path.basename(f),size:sz,murl:it.murl,purl:it.purl,t:it.t,q:it.q}); flush();
      console.log(`  saved ${path.basename(f)} ${sz}b <- ${it.purl}`);
    }catch(e){ console.log("  dl err",e.message); }
  }
  console.log(`SAVED ${saved.length} to ${OUT}`);
} finally{ try{await ctx.close();}catch{} console.log("SEARCH DONE"); }
