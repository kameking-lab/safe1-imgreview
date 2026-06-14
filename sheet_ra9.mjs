/** sheet_ra9.mjs : RA9候補のコンタクトシート生成（目視判定用）。画像生成なし・追記専用。*/
import fs from "node:fs"; import path from "node:path";
const SH="C:/Users/kanet/20260522/instagram-automation/node_modules/sharp";
const sharp=(await import(`file:///${SH}/lib/index.js`)).default;
const DIR="C:/Users/kanet/20260522/safe1/refs2/RA9/_cand";
const files=fs.readdirSync(DIR).filter(f=>/^d\d+\.(jpg|png|gif|webp)$/i.test(f)).sort((a,b)=>(+/d(\d+)/.exec(a)[1])-(+/d(\d+)/.exec(b)[1]));
const CELL=320, COLS=6, PAD=6, LBL=22;
const per=COLS*5;
let sheet=0;
for(let s=0;s<files.length;s+=per){
  const batch=files.slice(s,s+per);
  const rows=Math.ceil(batch.length/COLS);
  const W=COLS*(CELL+PAD)+PAD, H=rows*(CELL+LBL+PAD)+PAD;
  const comps=[];
  for(let i=0;i<batch.length;i++){
    const f=batch[i]; const col=i%COLS, row=Math.floor(i/COLS);
    const x=PAD+col*(CELL+PAD), y=PAD+row*(CELL+LBL+PAD);
    try{
      const img=await sharp(path.join(DIR,f),{animated:false}).resize(CELL,CELL,{fit:"contain",background:{r:240,g:240,b:240}}).flatten({background:{r:255,g:255,b:255}}).png().toBuffer();
      comps.push({input:img,left:x,top:y+LBL});
    }catch(e){ /* skip */ }
    const label=Buffer.from(`<svg width="${CELL}" height="${LBL}"><rect width="100%" height="100%" fill="#222"/><text x="4" y="16" font-family="sans-serif" font-size="15" fill="#fff">${f}</text></svg>`);
    comps.push({input:label,left:x,top:y});
  }
  const out=path.join(DIR,`_sheet_${sheet}.png`);
  await sharp({create:{width:W,height:H,channels:3,background:{r:255,g:255,b:255}}}).composite(comps).png().toFile(out);
  console.log("wrote",out,`(${batch.length} imgs)`);
  sheet++;
}
console.log("DONE sheets:",sheet);
