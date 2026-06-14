/** adopt_ra1.mjs : RA1 採用画像を refs2/RA1/01..02.png として作成（白背景フラット化のみ・内容無改変）。
 *  画像生成なし・削除/上書きなし・新ファイル名のみ。*/
import fs from "node:fs"; import path from "node:path";
const SH="C:/Users/kanet/20260522/instagram-automation/node_modules/sharp";
const sharp=(await import(`file:///${SH}/lib/index.js`)).default;
const CAND="C:/Users/kanet/20260522/safe1/refs2/RA1/_cand";
const OUT="C:/Users/kanet/20260522/safe1/refs2/RA1";
const map=[["d90.jpg","01.png"],["d114.png","02.png"]];
for(const [src,dst] of map){
  const outp=path.join(OUT,dst);
  if(fs.existsSync(outp)){ console.log("exists, skip",dst); continue; }
  const buf=await sharp(path.join(CAND,src)).flatten({background:{r:255,g:255,b:255}}).png().toBuffer();
  fs.writeFileSync(outp,buf);
  console.log("wrote",dst,"from",src,buf.length,"b");
}
console.log("DONE");
