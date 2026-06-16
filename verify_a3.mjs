const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);
import fs from "node:fs";
const urls=[
  "https://anzeninfo.mhlw.go.jp/anzen/sai/image/sai23/sai23-31-55-1-s.jpg",
  "https://anzeninfo.mhlw.go.jp/anzen/sai/image/sai23/sai23-31-55-1.jpg",
];
const { ctx, page } = await launchBrowser("anzen",{viewport:{width:1200,height:900}});
try{
  for(const u of urls){
    try{
      const r=await page.goto(u,{waitUntil:"commit",timeout:25000}).catch(()=>null);
      if(!r){ console.log("NULL",u); continue; }
      const ct=r.headers()["content-type"]||"";
      const buf=r.ok()? await r.body().catch(()=>null):null;
      console.log(r.status(), ct, buf?buf.length:0, u);
      if(r.ok() && buf && /image\//.test(ct)){
        const name=u.endsWith("-s.jpg")?"refs/cand_A3/z04_small.jpg":"refs/cand_A3/z04_full.jpg";
        fs.writeFileSync(name,buf); console.log("  wrote",name);
      }
    }catch(e){ console.log("ERR",u,e.message); }
  }
} finally { try{await ctx.close();}catch{} console.log("DONE"); }
