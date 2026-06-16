/** search_t1.mjs : I-T1 元絵候補(テールゲートリフター 昇降板から墜落)をブラウザ画像検索で収集
 *  instagram-automation方式・別プロファイル(anzen)・Chromeはkillしない。
 *  Bing画像検索を使い、フルサイズ画像URL(murl)と出所ページ(purl)を収集→上位を保存。 */
import fs from "node:fs"; import path from "node:path";
const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);
const OUT="C:/Users/kanet/20260522/safe1/refs/cand_T1"; fs.mkdirSync(OUT,{recursive:true});

const QUERIES=[
  "テールゲートリフター 墜落 災害 イラスト",
  "テールゲートリフター 昇降板 転落 災害事例 図",
  "陸災防 テールゲートリフター 安全 イラスト 墜落",
  "tail gate lift fall accident illustration warning",
];
const { ctx, page } = await launchBrowser("anzen",{viewport:{width:1500,height:1200}});
const all=[];
try{
  for(const q of QUERIES){
    const url=`https://www.bing.com/images/search?q=${encodeURIComponent(q)}&qft=+filterui:photo-clipart`;
    try{
      await page.goto(url,{waitUntil:"domcontentloaded",timeout:60000}); await page.waitForTimeout(2500);
      // 結果のメタJSONは a.iusc の m 属性に入っている
      const items=await page.evaluate(()=>Array.from(document.querySelectorAll("a.iusc")).slice(0,20).map(a=>{try{return JSON.parse(a.getAttribute("m"));}catch{return null;}}).filter(Boolean).map(m=>({murl:m.murl,purl:m.purl,t:m.t||""})));
      console.log(`\n[Q] ${q}  -> ${items.length} items`);
      items.forEach(it=>{ all.push({q,...it}); });
    }catch(e){ console.log("  query err",q,e.message); }
  }
  // 重複URL除去
  const seen=new Set(); const uniq=[];
  for(const it of all){ if(it.murl && !seen.has(it.murl)){ seen.add(it.murl); uniq.push(it); } }
  console.log(`\nUNIQUE candidates: ${uniq.length}`);
  // 上位~16をダウンロード(ページコンテキストfetchで参照元/CORS回避)
  let n=0; const saved=[];
  for(const it of uniq.slice(0,16)){
    try{
      const b=await page.evaluate(async(src)=>{try{const r=await fetch(src);if(!r.ok)return null;const bl=await r.blob();if(bl.size<3000)return null;return await new Promise(res=>{const rd=new FileReader();rd.onload=()=>res(rd.result.split(",")[1]);rd.onerror=()=>res(null);rd.readAsDataURL(bl);});}catch{return null;}}, it.murl);
      if(b){ let ext=(it.murl.split("?")[0].split(".").pop()||"jpg").toLowerCase(); if(ext.length>4||!/^(jpg|jpeg|png|gif|webp)$/.test(ext))ext="jpg"; const f=path.join(OUT,`c${String(++n).padStart(2,"0")}.${ext}`); fs.writeFileSync(f,Buffer.from(b,"base64")); const sz=fs.statSync(f).size; saved.push({file:path.basename(f),size:sz,murl:it.murl,purl:it.purl,t:it.t,q:it.q}); console.log(`  saved ${path.basename(f)} ${sz}b  <- ${it.purl}`); }
    }catch(e){ console.log("  dl err",e.message); }
  }
  fs.writeFileSync(path.join(OUT,"_candidates.json"),JSON.stringify(saved,null,2));
  console.log(`\nSAVED ${saved.length} candidate files to ${OUT}`);
} finally{ try{await ctx.close();}catch{} console.log("SEARCH DONE"); }
