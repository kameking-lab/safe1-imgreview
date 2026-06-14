/** adopt_ra10.mjs : RA10「その他 高所作業車起因の死傷（見つかったもの）」採用画像を確定。
 *  画像生成なし・追記専用・上書きしない（既存ファイルがあればskip）。
 *  01.png ← d161（iStock イラスト：ブーム式高所作業車のバスケットから搭乗者が機外へ振り出され/ぶら下がり建物端へ墜落＝作業床からの墜落。白背景フラット化のみ・内容無改変）
 *  02.jpg ← d94（Daiichi TV 報道写真：高所作業車（トラック搭載型）が公道走行/作業中に信号柱へ衝突・柱折れトラック押しつぶす＝走行/衝突事故。コピーのみ・無改変） */
import fs from "node:fs"; import path from "node:path";
const SH="C:/Users/kanet/20260522/instagram-automation/node_modules/sharp";
const sharp=(await import(`file:///${SH}/lib/index.js`)).default;
const CAND="C:/Users/kanet/20260522/safe1/refs2/RA10/_cand";
const DST="C:/Users/kanet/20260522/safe1/refs2/RA10";

// 01: イラスト → 白背景フラット化のみ
const o1=path.join(DST,"01.png");
if(fs.existsSync(o1)){ console.log("skip exists 01.png"); }
else { await sharp(path.join(CAND,"d161.jpg"),{animated:false}).flatten({background:{r:255,g:255,b:255}}).png().toFile(o1); console.log("wrote",o1,"<- d161.jpg"); }

// 02: 報道写真 → コピーのみ（無改変）
const o2=path.join(DST,"02.jpg");
if(fs.existsSync(o2)){ console.log("skip exists 02.jpg"); }
else { fs.copyFileSync(path.join(CAND,"d94.jpg"),o2); console.log("copied",o2,"<- d94.jpg"); }

console.log("DONE adopt RA10");
