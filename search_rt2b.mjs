/** search_rt2b.mjs : RT2 2巡目。職場のあんぜんサイト/陸災防/JNIOSH 等の災害事例イラストを狙い、
 *  clipartフィルタ無し(photo含む)でも収集。instagram-automation方式・別プロファイル(anzen)・
 *  Chromeはkillしない・画像生成はしない・追記専用(d番号は続き)。*/
import fs from "node:fs"; import path from "node:path";
const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);
const OUT="C:/Users/kanet/20260522/safe1/refs2/RT2/_cand"; fs.mkdirSync(OUT,{recursive:true});

// 既存 d番号の続きから採番
const exist=fs.readdirSync(OUT).map(f=>/^d(\d+)\./.exec(f)).filter(Boolean).map(m=>+m[1]);
let n=exist.length?Math.max(...exist):0;

const QUERIES=[
  // clipart寄り
  ["テールゲートリフター 昇降板 荷台 はさまれ 死亡 災害事例 イラスト",true],
  ["テールゲートリフター 上半身 はさまれ 事故 イラスト",true],
  ["陸上貨物運送 はさまれ 荷台 昇降装置 災害事例 イラスト",true],
  ["パワーゲート はさまれ 災害 イラスト",true],
  // photo含む(災害事例DBの図はphoto判定されがち)
  ["テールゲートリフター 災害事例 はさまれ",false],
  ["職場のあんぜんサイト テールゲートリフター はさまれ 事例",false],
  ["テールゲートリフター 死亡災害 はさまれ 荷台",false],
  ["tail lift trapped between platform and truck body accident",false],
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

// 既存meta(_all_meta+_dl)の murl を除外
let prev=new Set();
for(const f of ["_all_meta.json","_dl.json"]){
  try{ JSON.parse(fs.readFileSync(path.join(OUT,f))).forEach(x=>x.murl&&prev.add(x.murl)); }catch{}
}
const seen=new Set(); const uniq=[];
for(const it of all){ if(it.murl && !prev.has(it.murl) && !seen.has(it.murl)){ seen.add(it.murl); uniq.push(it); } }
fs.writeFileSync(path.join(OUT,"_all_meta2.json"),JSON.stringify(uniq,null,2));
console.log(`NEW UNIQUE: ${uniq.length}  -> _all_meta2.json`);

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
fs.writeFileSync(path.join(OUT,"_dl2.json"),JSON.stringify(saved,null,2));
console.log(`DL2 DONE: ${saved.length} files (next d=${n})`);
