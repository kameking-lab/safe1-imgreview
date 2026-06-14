/** adopt_ra5.mjs : RA5採用画像を refs2/RA5/01..03.png として確定（白背景フラット化のみ・内容無改変）。画像生成なし・追記専用。*/
import fs from "node:fs"; import path from "node:path";
const SH="C:/Users/kanet/20260522/instagram-automation/node_modules/sharp";
const sharp=(await import(`file:///${SH}/lib/index.js`)).default;
const CAND="C:/Users/kanet/20260522/safe1/refs2/RA5/_cand";
const DST="C:/Users/kanet/20260522/safe1/refs2/RA5";
const MAP=[
  ["d143.jpg","01.png"],  // IPAF MEWP Catapult Effect: ブーム式作業床が障害物等で急動作→搭乗者が手すり越しにカタパルトされ墜落(3コマ)
  ["d214.jpg","02.png"],  // FPSI Safety Alert#24: ブーム式高所作業車の急動作/反動で搭乗者がバスケットから上方へ投げ出され墜落(ヘルメット・保護メガネ飛散)
  ["d34.gif", "03.png"],  // アイチコーポレーション 自走式高所作業車の運転: シザース作業床が急操作/衝撃で揺れ搭乗者がバランスを崩し振り落とされ
];
for(const [src,dst] of MAP){
  const o=path.join(DST,dst);
  if(fs.existsSync(o)){ console.log("skip exists",dst); continue; }
  await sharp(path.join(CAND,src),{animated:false}).flatten({background:{r:255,g:255,b:255}}).png().toFile(o);
  console.log("wrote",o,"<-",src);
}
console.log("DONE adopt");
