/** adopt_rt8.mjs : RT8採用候補(d06,d11)を白背景フラット化でpng採用化（内容無改変・追記専用・画像生成なし）。*/
import fs from "node:fs"; import path from "node:path";
const SH="C:/Users/kanet/20260522/instagram-automation/node_modules/sharp";
const sharp=(await import(`file:///${SH}/lib/index.js`)).default;
const CAND="C:/Users/kanet/20260522/safe1/refs2/RT8/_cand";
const DST="C:/Users/kanet/20260522/safe1/refs2/RT8";
const MAP=[["d06.webp","01.png"],["d11.webp","02.png"]];
for(const [src,dst] of MAP){
  const o=path.join(DST,dst);
  if(fs.existsSync(o)){ console.log("exists, skip",dst); continue; }
  const buf=await sharp(path.join(CAND,src)).flatten({background:{r:255,g:255,b:255}}).png().toBuffer();
  fs.writeFileSync(o,buf);
  console.log("wrote",dst,buf.length,"b <-",src);
}
console.log("DONE");
