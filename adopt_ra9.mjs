/** adopt_ra9.mjs : RA9採用画像を refs2/RA9/01.png として確定（白背景フラット化のみ・内容無改変）。
 *  画像生成なし・追記専用・上書きしない（既存ファイルがあればskip）。
 *  採用元 d114 は安全ノート(safetynotes.net)のブーム式高所作業車「積載超過→転倒/投げ出し」2コマ図。
 *  RA9の探索(search_ra9.mjs)では同図が再取得されなかったため、出所が同一の既取得バイト(refs2/RA7/_cand/d114.png)を
 *  RA9/_cand へ新ファイル名 d177.png として複製(コピーのみ・元は無改変)し、RA9自身の候補として記録した上で採用する。*/
import fs from "node:fs"; import path from "node:path";
const SH="C:/Users/kanet/20260522/instagram-automation/node_modules/sharp";
const sharp=(await import(`file:///${SH}/lib/index.js`)).default;
const RA9CAND="C:/Users/kanet/20260522/safe1/refs2/RA9/_cand";
const DST="C:/Users/kanet/20260522/safe1/refs2/RA9";
const SRC="C:/Users/kanet/20260522/safe1/refs2/RA7/_cand/d114.png";

// 1) 出所同一の既取得画像を RA9/_cand へ新ファイルとして複製（コピーのみ）
const candCopy=path.join(RA9CAND,"d177.png");
if(!fs.existsSync(candCopy)){ fs.copyFileSync(SRC,candCopy); console.log("copied cand",candCopy); }
else console.log("skip cand exists",candCopy);

// 2) 採用: 01.png（白背景フラット化のみ・内容無改変）
const MAP=[
  ["d177.png","01.png"], // 積載超過: ブーム式高所作業車のバスケットに定格超過の重量物を載せ、左コマ=物が落下し搭乗者が振り出され(ejection)、右コマ=ブーム折損・機体ごと転倒(tip-over)。機械○/事象=積載超過による転倒・投げ出し○/被災者=搭乗者が投げ出され○
];
for(const [src,dst] of MAP){
  const o=path.join(DST,dst);
  if(fs.existsSync(o)){ console.log("skip exists",dst); continue; }
  await sharp(path.join(RA9CAND,src),{animated:false}).flatten({background:{r:255,g:255,b:255}}).png().toFile(o);
  console.log("wrote",o,"<-",src);
}
console.log("DONE adopt");
