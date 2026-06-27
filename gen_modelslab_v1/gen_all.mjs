/** gen_all.mjs — ModelsLabで転落事故イラストを3方式30枚生成。resumable・5枚ごとgit push・上限/エラーで安全停止。
 *  A=text2img(イラストモデル) B=img2img(本物イラストベース) C1/C2=img2img(自作下書きベース・強度比較)。
 *  keyは .secrets/modelslab.key（mllib経由・値出力なし）。 */
import fs from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { text2img, img2img, download, KEY_TAIL } from "./mllib.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const IMGDIR = path.join(__dirname, "img");
const CSV = path.join(__dirname, "index.csv");
const LOG = path.join(__dirname, "gen_all.log");
fs.mkdirSync(IMGDIR, { recursive: true });
const log = (m) => { const l = `[${new Date().toISOString()}] ${m}`; console.log(l); fs.appendFileSync(LOG, l + "\n"); };
const RAW = "https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/master/gen_modelslab_v1";

const ILLUST = "flat-2d-animerge";   // 採用イラストモデル
const STYLE_T2I = "flat 2D anime style safety education illustration, KYT training poster, clean bold line art and cel shading, full body wide shot of the whole scene, detailed background";
const STYLE_I2I = "clean flat illustration, safety education KYT poster art style, anime cel shading, keep the original composition and pose, detailed";
const SCENE = "a Japanese male construction worker wearing a chin-strap helmet, high-visibility vest, safety shoes and a full-body harness, on the platform of a vertical scissor lift (machine upright and stable) inside a Japanese exhibition hall booth construction site with aluminum truss pillars, fixtures and blank signboards, not a photograph";
const FALL = "the dangerous posture is the trigger of the fall, center of mass already past the support range, can't recover, the very moment of starting to fall, arms grabbing back toward the rail, alarmed face, no motion lines";

const CAUSES = [
  "putting his right foot up on the top guardrail and leaning out to reach an overhead signboard, losing balance over the rail",
  "leaning his upper body far out over the top guardrail reaching a signboard with both hands, pitching forward",
  "standing up on top of the guardrail to gain height while working, becoming unstable and toppling over",
  "straddling the top guardrail to move to the other side, his straddling foot slips and he slides off the rail",
  "stepping toward an adjacent truss structure to transfer over, missing his footing in the gap and falling into it",
  "sitting on the top guardrail during a break, leaning back and losing balance backward",
  "leaning forward over the guardrail with his fall-arrest hook left unconnected, collapsing forward as the hook cannot stop him",
  "holding a heavy signboard panel alone over the guardrail, pulled forward by its weight and falling with the load",
  "standing on a stepladder placed on the platform to gain extra height, the stepladder wobbles and he topples over the rail",
  "slipping on a wet platform floor, unable to brace, his body sliding under the mid-rail through the gap",
];
const CAUSE_JP = [
  "右足を上部手すりに乗せ身を乗り出し看板へ手→重心が手すり外へ",
  "上半身を手すり外へ大きく乗り出し看板に両手→前のめり",
  "高さを稼ごうと手すりの上に立って作業→不安定で転落",
  "手すりを跨いで反対側へ→跨いだ足が滑り抜けて転落",
  "隣のトラスへ乗り移ろうと踏み出し→隙間で踏み外し転落",
  "手すりに腰掛け休憩→後ろへ体重をかけ背中から転落",
  "フック未接続のまま前傾作業→崩れてもフックが効かず転落",
  "重い看板を抱え手すり越し→重量に前方へ引かれ荷ごと転落",
  "作業床に脚立でかさ上げ→ぐらつき手すり外へ転落",
  "濡れ床で足を滑らせ→手すり下の隙間から滑り落ち転落",
];
const BASES = ["0002","0045","0091","0093","0100","0112","0114","0137","0138","0215"];
const BASE_EXT = { "0002":"jpg","0045":"png","0091":"jpg","0093":"jpg","0100":"jpg","0112":"jpg","0114":"jpg","0137":"jpg","0138":"png","0215":"jpg" };

// 生成タスク定義
const TASKS = [];
for (let i = 0; i < 10; i++) TASKS.push({ method:"A", n:i+1, kind:"t2i", model:ILLUST, cause:i,
  prompt:`${STYLE_T2I}, ${SCENE}, ${CAUSES[i]}, ${FALL}` });
for (let i = 0; i < 10; i++) TASKS.push({ method:"B", n:i+1, kind:"i2i", endpoint:"realtime", strength:0.55, cause:i,
  init:`${RAW}/base/${BASES[i]}.${BASE_EXT[BASES[i]]}`, baseId:BASES[i],
  prompt:`${STYLE_I2I}, ${SCENE}, a worker falling from a scissor lift, ${CAUSES[i]}, ${FALL}` });
for (let i = 0; i < 5; i++) TASKS.push({ method:"C1", n:i+1, kind:"i2i", endpoint:"images", model:ILLUST, strength:0.72, cause:i,
  init:`${RAW}/draft/${String(i+1).padStart(2,"0")}.png`, draftId:String(i+1).padStart(2,"0"),
  prompt:`${STYLE_I2I}, follow the pose of the sketch but redraw as a polished illustration, ${SCENE}, ${CAUSES[i]}, ${FALL}, do not draw any numbers letters arrows or guide lines` });
for (let i = 0; i < 5; i++) TASKS.push({ method:"C2", n:i+1, kind:"i2i", endpoint:"images", model:ILLUST, strength:0.5, cause:i,
  init:`${RAW}/draft/${String(i+1).padStart(2,"0")}.png`, draftId:String(i+1).padStart(2,"0"),
  prompt:`${STYLE_I2I}, keep the sketch composition closely, ${SCENE}, ${CAUSES[i]}, ${FALL}, do not draw any numbers letters arrows or guide lines` });

if (!fs.existsSync(CSV)) fs.writeFileSync(CSV, "方式,連番,使用モデルID,手法,ベース下書き,prompt_strength,原因状況,プロンプト要約,画像ファイル\n");

function gitPush(msg) {
  try {
    execSync(`git -C "${ROOT}" add gen_modelslab_v1/img gen_modelslab_v1/index.csv`, { stdio: "ignore" });
    execSync(`git -C "${ROOT}" commit -q -m "${msg}"`, { stdio: "ignore" });
    try { execSync(`git -C "${ROOT}" pull --rebase origin master`, { stdio: "ignore" }); } catch {}
    execSync(`git -C "${ROOT}" push origin master`, { stdio: "ignore" });
    log(`  git pushed: ${msg}`);
  } catch (e) { log(`  git push skipped/err: ${String(e.message).slice(0,80)}`); }
}

log(`START key=${KEY_TAIL} tasks=${TASKS.length}`);
let made = 0, sinceCommit = 0;
const CREDIT_RE = /credit|insufficient|balance|quota|exceeded|unauthor|invalid api key|limit reached|subscription|plan/i;

for (const t of TASKS) {
  const fname = `${t.method}_${String(t.n).padStart(2,"0")}.png`;
  const outPath = path.join(IMGDIR, fname);
  if (fs.existsSync(outPath) && fs.statSync(outPath).size > 3000) { log(`${fname} skip(exists)`); continue; }
  const model = t.model || (t.endpoint==="realtime" ? "realtime-default(SDXL)" : ILLUST);
  let r;
  try {
    if (t.kind === "t2i") r = await text2img({ prompt:t.prompt, width:768, height:1024, steps:30, guidance:7.5, seed:1000+t.n, model_id:t.model, endpoint:"images" });
    else r = await img2img({ prompt:t.prompt, init_image:t.init, prompt_strength:t.strength, width:768, height:1024, steps:30, guidance:8, seed:1000+t.n, model_id:t.model, endpoint:t.endpoint });
  } catch (e) { r = { ok:false, err:"exception:"+e.message }; }
  if (!r.ok) {
    log(`${fname} FAIL err=${JSON.stringify(r.err||r).slice(0,200)}`);
    if (CREDIT_RE.test(JSON.stringify(r.err||""))) { log(`CREDIT/AUTH LIMIT — stop. saved=${made}`); fs.writeFileSync(path.join(__dirname,"captured_stop.txt"), `stop_local=${new Date().toString()}\nreason=${JSON.stringify(r.err).slice(0,300)}\nsaved=${made}\n`); break; }
    continue;
  }
  const ok = await download(r.urls[0], outPath);
  if (!ok) { log(`${fname} download FAIL url=${r.urls[0]}`); continue; }
  const baseDraft = t.baseId ? `base/${t.baseId}` : (t.draftId ? `draft/${t.draftId}` : "-");
  const row = [t.method, String(t.n).padStart(2,"0"), model, (t.kind==="t2i"?"text2img":`img2img(${t.endpoint})`), baseDraft, (t.strength??"-"), `"${CAUSE_JP[t.cause]}"`, `"${t.kind}/${model}/${baseDraft}"`, fname].join(",");
  fs.appendFileSync(CSV, row + "\n");
  made++; sinceCommit++;
  log(`${fname} OK model=${model} ${(t.strength!=null?("str="+t.strength):"")} (${made} made)`);
  if (sinceCommit >= 5) { gitPush(`ModelsLab gen: ${made}枚保存 (方式A/B/C1/C2・5枚ごとpush・非破壊)`); sinceCommit = 0; }
}
if (sinceCommit > 0) gitPush(`ModelsLab gen: 計${made}枚 最終保存 (非破壊)`);
log(`DONE made_this_run=${made} total=${fs.readdirSync(IMGDIR).filter(f=>/\.png$/.test(f)).length}`);
