/** adopt_ra7.mjs : RA7採用画像を refs2/RA7/01.png として確定（白背景フラット化のみ・内容無改変）。画像生成なし・追記専用。*/
import fs from "node:fs"; import path from "node:path";
const SH="C:/Users/kanet/20260522/instagram-automation/node_modules/sharp";
const sharp=(await import(`file:///${SH}/lib/index.js`)).default;
const CAND="C:/Users/kanet/20260522/safe1/refs2/RA7/_cand";
const DST="C:/Users/kanet/20260522/safe1/refs2/RA7";
const MAP=[
  ["d112.webp","01.png"],  // "TIP OVER RISK": 自走式高所作業車(シザース式)が傾斜/端部で転倒し、搭乗者(黄ヘル・安全ベスト)が作業床から投げ出され墜落。機械○/事象=転倒○/被災者=投げ出され○
];
for(const [src,dst] of MAP){
  const o=path.join(DST,dst);
  if(fs.existsSync(o)){ console.log("skip exists",dst); continue; }
  await sharp(path.join(CAND,src),{animated:false}).flatten({background:{r:255,g:255,b:255}}).png().toFile(o);
  console.log("wrote",o,"<-",src);
}
console.log("DONE adopt");
