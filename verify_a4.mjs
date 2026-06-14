const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);
import fs from "node:fs";
const urls=[
  "https://www.j-bma.or.jp/assets/img/h_s_clinic/img01.jpg",
  "https://www.rodo.co.jp/wp/wp-content/uploads/2019/12/24/kyt2162_01.jpg",
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
        const name=u.includes("j-bma")?"refs/cand_A4/z15_full.jpg":"refs/cand_A4/z02_full.jpg";
        fs.writeFileSync(name,buf); console.log("  wrote",name);
      }
    }catch(e){ console.log("ERR",u,e.message); }
  }
} finally { try{await ctx.close();}catch{} console.log("DONE"); }
