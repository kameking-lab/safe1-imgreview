/** fetch_refs.mjs : あんぜんサイト各事例ページのイラスト図(img)を抽出・ダウンロード */
import fs from "node:fs"; import path from "node:path";
const LIB="C:/Users/kanet/20260522/instagram-automation/scripts/lib";
const { launchBrowser } = await import(`file:///${LIB}/browser-helpers.mjs`);
const OUT="C:/Users/kanet/20260522/safe1/refs/anzen"; fs.mkdirSync(OUT,{recursive:true});
const CASES={1:"38",2:"101281",3:"101534",4:"101377",5:"101270",6:"101412"};
const { ctx, page } = await launchBrowser("anzen",{viewport:{width:1400,height:1100}});
const report={};
try{
  for(const [cn,id] of Object.entries(CASES)){
    const url=`https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_DET.aspx?joho_no=${id}`;
    await page.goto(url,{waitUntil:"domcontentloaded",timeout:60000}); await page.waitForTimeout(1500);
    const imgs=await page.evaluate(()=>Array.from(document.querySelectorAll("img")).map(i=>({src:i.src,w:i.naturalWidth,h:i.naturalHeight,alt:i.alt||""})));
    // ナビ/ロゴ/小アイコンを除外し、事故図候補(ある程度の大きさ・コンテンツ領域)を抽出
    const cand=imgs.filter(i=>i.w>=120 && i.h>=90 && !/logo|header|footer|icon|btn|banner|common|spacer/i.test(i.src));
    report[cn]={id,url,allImgs:imgs.length,cand};
    console.log(`\n[case${cn}] No.${id} imgs=${imgs.length} cand=${cand.length}`);
    cand.forEach(c=>console.log(`  ${c.w}x${c.h} ${c.src}`));
    // ダウンロード(最大2)
    let n=0;
    for(const c of cand.slice(0,2)){
      try{ const b=await page.evaluate(async(src)=>{const r=await fetch(src,{credentials:"include"});const bl=await r.blob();return await new Promise(res=>{const rd=new FileReader();rd.onload=()=>res(rd.result.split(",")[1]);rd.onerror=()=>res(null);rd.readAsDataURL(bl);});},c.src);
        if(b){ const ext=(c.src.split(".").pop()||"png").split("?")[0].slice(0,4); const f=path.join(OUT,`case${cn}_${++n}.${ext}`); fs.writeFileSync(f,Buffer.from(b,"base64")); console.log(`   saved ${f} (${fs.statSync(f).size}b)`); } }
      catch(e){ console.log("   dl err",e.message); }
    }
  }
  fs.writeFileSync(path.join(OUT,"_report.json"),JSON.stringify(report,null,2));
} finally{ try{await ctx.close();}catch{} console.log("\nREFS DONE"); }
