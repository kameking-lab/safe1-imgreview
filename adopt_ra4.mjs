/** adopt_ra4.mjs : RA4採用画像を refs2/RA4/01..03.png として確定（白背景フラット化のみ・内容無改変）。画像生成なし・追記専用。*/
import fs from "node:fs"; import path from "node:path";
const SH="C:/Users/kanet/20260522/instagram-automation/node_modules/sharp";
const sharp=(await import(`file:///${SH}/lib/index.js`)).default;
const CAND="C:/Users/kanet/20260522/safe1/refs2/RA4/_cand";
const DST="C:/Users/kanet/20260522/safe1/refs2/RA4";
const MAP=[
  ["d154.jpg","01.png"],  // 建荷協 高0015: シザース式高所作業車の作業床から手摺越しに身を乗り出し墜落
  ["d99.webp","02.png"],  // dreamstime: ブーム式高所作業車のバケットから墜落し建物端にぶら下がる作業者
  ["d103.webp","03.png"], // stockphotos: シザース式高所作業車の作業床から頭から墜落(FALL FROM WORK PLATFORM)
];
for(const [src,dst] of MAP){
  const o=path.join(DST,dst);
  if(fs.existsSync(o)){ console.log("skip exists",dst); continue; }
  await sharp(path.join(CAND,src),{animated:false}).flatten({background:{r:255,g:255,b:255}}).png().toFile(o);
  console.log("wrote",o,"<-",src);
}
console.log("DONE adopt");
