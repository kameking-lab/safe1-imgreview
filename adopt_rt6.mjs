/** adopt_rt6.mjs : RT6採用画像を _cand から refs2/RT6/01..03.png へ変換保存。
 *  画像生成なし（フォーマット変換のみ・白背景フラット化、内容無改変）・追記専用。*/
import fs from "node:fs"; import path from "node:path";
const SH="C:/Users/kanet/20260522/instagram-automation/node_modules/sharp";
const sharp=(await import(`file:///${SH}/lib/index.js`)).default;
const DIR="C:/Users/kanet/20260522/safe1/refs2/RT6/_cand";
const OUT="C:/Users/kanet/20260522/safe1/refs2/RT6";
const map=[["d01.jpg","01.png"],["d03.jpg","02.png"],["d64.png","03.png"]];
for(const [src,dst] of map){
  const buf=await sharp(path.join(DIR,src),{animated:false}).flatten({background:{r:255,g:255,b:255}}).png().toBuffer();
  fs.writeFileSync(path.join(OUT,dst),buf);
  console.log("wrote",dst,buf.length,"b <-",src);
}
console.log("DONE");
