/** search_ra2.mjs : RA2「高所作業車 作業床と上方構造物(梁/看板/天井)で挟まれ」の事故イラスト収集。
 *  3要素必須: (1)機械=高所作業車(ブーム/シザース等) (2)作業床(バスケット)と上方の梁/看板/天井/構造物との間で挟まれが起きている (3)搭乗者が挟まれ・被災。
 *  instagram-automation方式・別プロファイル(anzen)・Chromeはkillしない・画像生成はしない・追記専用。*/
import fs from "node:fs"; import path from "node:path";
const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);
const OUT="C:/Users/kanet/20260522/safe1/refs2/RA2/_cand"; fs.mkdirSync(OUT,{recursive:true});

const exist=fs.readdirSync(OUT).map(f=>/^d(\d+)\./.exec(f)).filter(Boolean).map(m=>+m[1]);
let n=exist.length?Math.max(...exist):0;

const QUERIES=[
  // clipart寄り(イラスト)
  ["高所作業車 作業床 はさまれ 天井 梁 災害 イラスト",true],
  ["高所作業車 バスケット 上昇 挟まれ 構造物 墜落防止 イラスト",true],
  ["高所作業車 搭乗者 上方 はさまれ 看板 庇 災害事例 イラスト",true],
  ["ブーム式 高所作業車 作業床 上昇 天井 挟まれ KYT イラスト",true],
  ["高所作業車 操作ミス 上昇 はさまれ 死亡災害 注意喚起 イラスト",true],
  ["高所作業車 作業床と梁 挟まれ 首 胸 災害 イラスト",true],
  // photo含む(災害事例DBの図はphoto判定されがち)
  ["陸災防 建災防 高所作業車 はさまれ 上方構造物 災害事例",false],
  ["職場のあんぜんサイト 高所作業車 はさまれ 天井 災害事例",false],
  ["高所作業車 挟まれ 死亡災害 厚生労働省 事例 上昇",false],
  ["aerial work platform mewp crushing overhead beam ceiling worker trapped accident illustration",false],
  ["scissor lift operator crushed overhead obstruction sustained involuntary operation accident",false],
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
