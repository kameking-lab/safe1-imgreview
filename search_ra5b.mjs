/** search_ra5b.mjs : RA5 追加探索（反動/カタパルト/急旋回/振り出され 寄り）。追記専用・別プロファイル(anzen)・Chrome kill無し・画像生成なし。*/
import fs from "node:fs"; import path from "node:path";
const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);
const OUT="C:/Users/kanet/20260522/safe1/refs2/RA5/_cand"; fs.mkdirSync(OUT,{recursive:true});
const exist=fs.readdirSync(OUT).map(f=>/^d(\d+)\./.exec(f)).filter(Boolean).map(m=>+m[1]);
let n=exist.length?Math.max(...exist):0;

const QUERIES=[
  ["高所作業車 反動 はね返り 作業床 搭乗者 投げ出され 墜落 イラスト",true],
  ["高所作業車 急旋回 ブーム 旋回 作業者 振り出され 墜落 災害 イラスト",true],
  ["アイチ 高所作業車 急発進 急停止 作業床 揺れ バランス 墜落 イラスト",true],
  ["高所作業車 走行中 急操作 作業床 揺れ 搭乗者 振られ 転落 KYT",true],
  ["MEWP catapult effect operator thrown over guardrail boom lift accident",false],
  ["aerial platform sudden movement worker catapulted ejected fall illustration safety",false],
  ["boom lift snagging recoil whiplash operator ejected fall accident diagram",false],
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

// 既存murlを除外
const prev=JSON.parse(fs.readFileSync(path.join(OUT,"_all_meta.json"),"utf8"));
const seen=new Set(prev.map(x=>x.murl)); const uniq=[];
for(const it of all){ if(it.murl && !seen.has(it.murl)){ seen.add(it.murl); uniq.push(it); } }
fs.writeFileSync(path.join(OUT,"_all_meta_b.json"),JSON.stringify(uniq,null,2));
console.log(`NEW UNIQUE (b): ${uniq.length}`);

const saved=[];
for(const it of uniq){
  try{
    const ref=it.purl||"https://www.bing.com/";
    const r=await fetch(it.murl,{headers:{"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36","Referer":ref,"Accept":"image/avif,image/webp,image/*,*/*"},signal:AbortSignal.timeout(20000)});
    if(!r.ok) continue;
    const ab=await r.arrayBuffer(); const buf=Buffer.from(ab);
    if(buf.length<5000) continue;
    const sig=buf.subarray(0,4).toString("hex");
    let ext="jpg";
    if(sig.startsWith("89504e47"))ext="png"; else if(sig.startsWith("ffd8"))ext="jpg"; else if(buf.subarray(0,6).toString("ascii").startsWith("GIF8"))ext="gif"; else if(buf.subarray(8,12).toString("ascii")==="WEBP")ext="webp"; else continue;
    const f=path.join(OUT,`d${String(++n).padStart(2,"0")}.${ext}`);
    fs.writeFileSync(f,buf);
    saved.push({file:path.basename(f),size:buf.length,murl:it.murl,purl:it.purl,t:it.t,q:it.q});
    console.log(`  saved ${path.basename(f)} <- ${it.purl}`);
  }catch(e){}
}
fs.writeFileSync(path.join(OUT,"_dl_b.json"),JSON.stringify(saved,null,2));
console.log(`DL DONE (b): ${saved.length} (next d=${n})`);
