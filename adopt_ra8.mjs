/** adopt_ra8.mjs : RA8採用画像を refs2/RA8/01..02.png として確定（白背景フラット化のみ・内容無改変）。画像生成なし・追記専用・上書きしない。*/
import fs from "node:fs"; import path from "node:path";
const SH="C:/Users/kanet/20260522/instagram-automation/node_modules/sharp";
const sharp=(await import(`file:///${SH}/lib/index.js`)).default;
const CAND="C:/Users/kanet/20260522/safe1/refs2/RA8/_cand";
const DST="C:/Users/kanet/20260522/safe1/refs2/RA8";
const MAP=[
  ["d116.png","01.png"],   // 穴: 自走式高所作業車(シザース)の車輪が地面の穴に落ち機体が傾き転倒、作業床の搭乗者が振られ投げ出され・救護者が駆け寄る。機械○/事象=転倒○/被災者=投げ出され○
  ["d144.webp","02.png"],  // 段差: "TIP OVER RISK" 自走式高所作業車(シザース)が後輪を段差(縁石/床端)から踏み外し転倒、搭乗者が作業床から投げ出され墜落。機械○/事象=転倒○/被災者=投げ出され○
];
for(const [src,dst] of MAP){
  const o=path.join(DST,dst);
  if(fs.existsSync(o)){ console.log("skip exists",dst); continue; }
  await sharp(path.join(CAND,src),{animated:false}).flatten({background:{r:255,g:255,b:255}}).png().toFile(o);
  console.log("wrote",o,"<-",src);
}
console.log("DONE adopt");
