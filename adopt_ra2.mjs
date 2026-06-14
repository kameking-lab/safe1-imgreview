/** adopt_ra2.mjs : RA2採用画像を refs2/RA2/01..02.png として確定（白背景フラット化のみ・内容無改変）。画像生成なし・追記専用。*/
import fs from "node:fs"; import path from "node:path";
const SH="C:/Users/kanet/20260522/instagram-automation/node_modules/sharp";
const sharp=(await import(`file:///${SH}/lib/index.js`)).default;
const CAND="C:/Users/kanet/20260522/safe1/refs2/RA2/_cand";
const DST="C:/Users/kanet/20260522/safe1/refs2/RA2";
const MAP=[
  ["d107.jpg","01.png"],   // ブーム式高所作業車 作業床と上方の鉄骨梁で挟まれ（3D教材レンダ）
  ["e86_01.png","02.png"], // 労働新聞社 災害事例: 高所作業車を上昇させPC梁/バーに挟まれた
];
for(const [src,dst] of MAP){
  const o=path.join(DST,dst);
  if(fs.existsSync(o)){ console.log("skip exists",dst); continue; }
  await sharp(path.join(CAND,src),{animated:false}).flatten({background:{r:255,g:255,b:255}}).png().toFile(o);
  console.log("wrote",o,"<-",src);
}
console.log("DONE adopt");
