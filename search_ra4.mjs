/** search_ra4.mjs : RA4「高所作業車 安全帯未使用で作業床から墜落」の事故イラスト収集。
 *  3要素必須: (1)機械=高所作業車(ブーム/シザース等) (2)作業床からの墜落が起きている (3)人(搭乗者)が墜落・被災。
 *  instagram-automation方式・別プロファイル(anzen)・Chromeはkillしない・画像生成はしない・追記専用。*/
import fs from "node:fs"; import path from "node:path";
const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);
const OUT="C:/Users/kanet/20260522/safe1/refs2/RA4/_cand"; fs.mkdirSync(OUT,{recursive:true});

const exist=fs.readdirSync(OUT).map(f=>/^d(\d+)\./.exec(f)).filter(Boolean).map(m=>+m[1]);
let n=exist.length?Math.max(...exist):0;

const QUERIES=[
  // clipart寄り(イラスト)
  ["高所作業車 安全帯 未使用 作業床 墜落 災害 イラスト",true],
  ["高所作業車 墜落 転落 作業床 安全帯 注意喚起 イラスト",true],
  ["高所作業車 バケット 身を乗り出し 墜落 KYT イラスト",true],
  ["高所作業車 ブーム 作業床 転落 死亡災害 事例 イラスト",true],
  ["高所作業車 手すり 乗り越え 墜落 安全帯未着用 イラスト",true],
  ["高所作業車 作業床 はみ出し バランス 墜落 災害事例 イラスト",true],
  // photo含む(災害事例DBの図はphoto判定されがち)
  ["建荷協 高所作業車 墜落 災害事例 作業床",false],
  ["職場のあんぜんサイト 高所作業車 墜落 安全帯 災害事例",false],
  ["陸災防 建災防 高所作業車 作業床 墜落 安全帯未使用 災害事例",false],
  ["aerial work platform fall worker no harness boom lift accident illustration",false],
  ["MEWP cherry picker operator fall from basket no fall arrest accident",false],
];
const { ctx, page } = await launchBrowser("anzen",{viewport:{width:1500,height:1200}});
const all=[];
try{
  for(const [q,clip] of QUERIES){
    const filt=clip?"&qft=+filterui:photo-clipart":"";
    const url=`https://www.bing.com/images/search?q=${encodeURIComponent(q)}${filt}`;
    try{
      await page.goto(url,{waitUntil:"domcontentloaded",timeout:60000}); await page.waitForTimeout(2500);
      const items=await page.evaluate(()=>Array.from(document.querySelectorAll("a.iusc")).slice(0,30).map(a=>{try{return JSON.parse(a.getAttribute("m"));}catch{return null;}}).filter(Boolean).map(m=>({murl:m.murl,purl:m.purl,t:m.t||""})));
      console.log(`[Q] ${q} -> ${items.length}`);
      items.forEach(it=>{ all.push({q,...it}); });
    }catch(e){ console.log("  query err",q,e.message); }
  }
}finally{ try{await ctx.close();}catch{} }

const seen=new Set(); const uniq=[];
for(const it of all){ if(it.murl && !seen.has(it.murl)){ seen.add(it.murl); uniq.push(it); } }
fs.writeFileSync(path.join(OUT,"_all_meta.json"),JSON.stringify(uniq,null,2));
console.log(`NEW UNIQUE: ${uniq.length}  -> _all_meta.json`);

const saved=[];
for(const it of uniq){
  try{
    const ref=it.purl||"https://www.bing.com/";
    const r=await fetch(it.murl,{headers:{"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36","Referer":ref,"Accept":"image/avif,image/webp,image/*,*/*"},signal:AbortSignal.timeout(20000)});
    if(!r.ok){ continue; }
    const ab=await r.arrayBuffer(); const buf=Buffer.from(ab);
    if(buf.length<5000) continue;
    const sig=buf.subarray(0,4).toString("hex");
    let ext="jpg";
    if(sig.startsWith("89504e47"))ext="png"; else if(sig.startsWith("ffd8"))ext="jpg"; else if(buf.subarray(0,6).toString("ascii").startsWith("GIF8"))ext="gif"; else if(buf.subarray(8,12).toString("ascii")==="WEBP")ext="webp"; else continue;
    const f=path.join(OUT,`d${String(++n).padStart(2,"0")}.${ext}`);
    fs.writeFileSync(f,buf);
    saved.push({file:path.basename(f),size:buf.length,murl:it.murl,purl:it.purl,t:it.t,q:it.q});
    console.log(`  saved ${path.basename(f)} ${buf.length}b <- ${it.purl}`);
  }catch(e){ /* skip */ }
}
fs.writeFileSync(path.join(OUT,"_dl.json"),JSON.stringify(saved,null,2));
console.log(`DL DONE: ${saved.length} files (next d=${n})`);
