/** adopt_ra6.mjs : RA6採用画像を refs2/RA6/01.png として確定（白背景フラット化のみ・内容無改変）。画像生成なし・追記専用。*/
import fs from "node:fs"; import path from "node:path";
const SH="C:/Users/kanet/20260522/instagram-automation/node_modules/sharp";
const sharp=(await import(`file:///${SH}/lib/index.js`)).default;
const CAND="C:/Users/kanet/20260522/safe1/refs2/RA6/_cand";
const DST="C:/Users/kanet/20260522/safe1/refs2/RA6";
const MAP=[
  ["d171.jpg","01.png"],  // IPAF AndyAccess "KEEP CLEAR OF OVERHEAD CABLES": 自走式ブームリフト(高所作業車)の作業床が架空電線に接触→搭乗者が感電(骨が透ける/ヘルメット飛散)、地上の同僚が救急へ
];
for(const [src,dst] of MAP){
  const o=path.join(DST,dst);
  if(fs.existsSync(o)){ console.log("skip exists",dst); continue; }
  await sharp(path.join(CAND,src),{animated:false}).flatten({background:{r:255,g:255,b:255}}).png().toFile(o);
  console.log("wrote",o,"<-",src);
}
console.log("DONE adopt");
