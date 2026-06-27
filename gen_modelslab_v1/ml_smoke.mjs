/** ml_smoke.mjs — ModelsLab text2img を1回叩いて疎通/レスポンス形式/モデル挙動を確認（keyは末尾4桁のみ表示）。 */
import path from "node:path";
import { fileURLToPath } from "node:url";
import { text2img, download, KEY_TAIL } from "./mllib.mjs";
const __dirname = path.dirname(fileURLToPath(import.meta.url));
console.log("KEY_TAIL", KEY_TAIL);
const prompt = "flat 2D safety education illustration, KYT training poster style, clean line art and cel shading, a Japanese male worker with chin-strap helmet, high-visibility vest, safety shoes and full-body harness on the platform of a vertical scissor lift inside a Japanese exhibition hall booth construction site with aluminum truss pillars, the worker leaning out over the guardrail reaching to a blank signboard and losing balance, center of mass past the support, the moment of starting to fall, alarmed face, not a photograph";
const t0 = Date.now();
const r = await text2img({ prompt, steps: 25, guidance: 7.5, seed: 12345 });
console.log("RESULT", JSON.stringify({ http: r.http, ok: r.ok, rawStatus: r.rawStatus, err: r.err, urls: r.urls ? r.urls.length : 0 }));
if (r.ok) {
  console.log("URL0", r.urls[0]);
  const ok = await download(r.urls[0], path.join(__dirname, "_smoke.png"));
  console.log("download", ok, `${((Date.now()-t0)/1000).toFixed(1)}s`);
} else {
  console.log("FAIL meta/err:", JSON.stringify(r.err || r).slice(0,500));
}
