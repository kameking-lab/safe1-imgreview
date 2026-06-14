/** fetch_ra2.mjs : RA2採用候補の高解像度版を記事ページから取得（og:image / 本文img）。画像生成なし・追記専用・kill無し。*/
import fs from "node:fs"; import path from "node:path";
const OUT="C:/Users/kanet/20260522/safe1/refs2/RA2/_cand"; fs.mkdirSync(OUT,{recursive:true});
const UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36";
const PAGES=[
  ["e86","https://www.rodo.co.jp/accident/191784/"],   // 高所作業車を上昇させたときにバーに挟まれた
  ["e107","https://www.theconstructionindex.co.uk/news/view/mewp-controls-finally-standardised"],
];
let n=0;
for(const [tag,url] of PAGES){
  try{
    const r=await fetch(url,{headers:{"User-Agent":UA},signal:AbortSignal.timeout(30000)});
    const html=await r.text();
    const urls=new Set();
    const og=/<meta[^>]+property=["']og:image["'][^>]+content=["']([^"']+)["']/i.exec(html);
    if(og) urls.add(og[1]);
    // 本文の wp-content uploads 画像（rodo）/ 記事内 img
    for(const m of html.matchAll(/<img[^>]+src=["']([^"']+\.(?:png|jpe?g))["']/ig)){ urls.add(m[1]); }
    console.log(`[${tag}] ${url} -> ${urls.size} img urls`);
    let i=0;
    for(let u of urls){
      i++;
      if(u.startsWith("//")) u="https:"+u; else if(u.startsWith("/")){ const o=new URL(url); u=o.origin+u; }
      try{
        const ir=await fetch(u,{headers:{"User-Agent":UA,"Referer":url},signal:AbortSignal.timeout(20000)});
        if(!ir.ok) continue;
        const buf=Buffer.from(await ir.arrayBuffer());
        if(buf.length<4000) continue;
        const sig=buf.subarray(0,4).toString("hex"); let ext="jpg";
        if(sig.startsWith("89504e47"))ext="png"; else if(sig.startsWith("ffd8"))ext="jpg"; else if(buf.subarray(8,12).toString("ascii")==="WEBP")ext="webp"; else continue;
        const f=path.join(OUT,`${tag}_${String(i).padStart(2,"0")}.${ext}`);
        fs.writeFileSync(f,buf); n++;
        console.log(`  saved ${path.basename(f)} ${buf.length}b <- ${u}`);
      }catch(e){}
    }
  }catch(e){ console.log("page err",tag,e.message); }
}
console.log("DONE fetch:",n);
