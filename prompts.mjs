// v6+ 画像プロンプト（日本ローカライズ・物理整合・TGL3事例の描き分け）。版ごとに編集して使う。
export const STYLE = {
  illust:
    "Professional Japanese occupational-safety training ILLUSTRATION, realistic semi-painterly style with full colour, soft cel-shading, real depth and perspective, a dynamic cinematic angle that freezes the dangerous split-second with clear motion. " +
    "The setting is unmistakably in JAPAN — a Japanese logistics warehouse or a Japanese exhibition-hall / convention-centre build-out (展示会場設営), with Japanese fixtures, floor protection sheets and signage feel. " +
    "The worker is a JAPANESE (East-Asian) man with Japanese build and features, wearing typical Japanese site gear: a safety helmet WITH CHIN STRAP, a Japanese work jacket / tobi work clothes, safety boots, and a full-body fall-arrest harness for aerial work. " +
    "Worker and equipment are rendered in the SAME painterly tone and the SAME light, fully integrated — never a flat pasted cut-out, never a black silhouette. The main subject fills the frame edge to edge. Landscape 3:2. " +
    "NO text, NO letters, NO numbers, NO logos, NO watermark. No blood, no gore, no injury detail — show only the dangerous moment.",
  photo:
    "Photorealistic DOCUMENTARY PHOTOGRAPH taken in JAPAN — a Japanese logistics warehouse or a Japanese exhibition-hall build-out (展示会場設営), with Japanese signage, fixtures and floor-protection sheets. " +
    "A JAPANESE (East-Asian) male worker with Japanese build, wearing Japanese site PPE: safety helmet WITH CHIN STRAP, hi-vis or Japanese work jacket, safety boots, and a full-body fall-arrest harness for aerial work. " +
    "Natural light, realistic colours, shallow depth of field, candid 35mm photojournalism. Show the worker from the SIDE or BEHIND at mid-distance, helmet clearly visible, face never a close-up (to keep it natural). The subject fills the frame. Landscape 3:2. " +
    "NO text overlays, NO logos, NO watermark, no blood, no injury — capture only the dangerous near-miss moment.",
};

// 6シーン。①人のみ墜落 / ②足のはさまれ(落ちない) / ③荷の転倒(人は落ちない) を明確に別物に。物理整合を明記。
export const SCENES = {
  illust: [
    // ① 墜落（人のみ）
    "Scene ①: At the rear of a Japanese flat-bed cargo truck fitted with a folding tail-lift platform (テールゲートリフター), a Japanese worker steps backward and misses the edge of the raised platform that has NO guardrail. He is falling backward off the rear edge toward the ground, head and back tilting down in a natural gravity-driven arc — ONLY THE MAN FALLS. A few boxes sit neatly on the truck bed and are NOT falling. No load is dropped, nothing is crushing him. Emphasis: a person-only fall from the platform edge.",
    // ② はさまれ（落ちない・転ばない）— 挟まれた瞬間を明確・動的に
    "Scene ②: Dramatic tight side view at the rear of a Japanese truck. The folding tail-lift platform has closed onto the worker's safety BOOT, and the foot is clearly VISIBLE, WEDGED and STUCK in the narrow gap between the steel platform edge and the truck-bed floor — he cannot pull it free. The Japanese worker twists and reacts in pain (one hand thrown out, body recoiling) but the trapped foot keeps him standing in place; he does NOT fall and does NOT topple, no load involved. Compose at a low side angle so the pinched boot in the gap is large and unmistakable in the foreground.",
    // ③ 荷の転倒（人は落ちない）
    "Scene ③: On a Japanese truck's tail-lift platform, a tall wheeled roll-cage cart (ロールボックスパレット — a steel mesh cage on casters loaded with boxes) tips over sideways because of a step/edge and an unlocked caster, and TOPPLES DOWN onto the Japanese worker standing beside it on the platform. The cage and the man move the SAME direction (toward the viewer's left): the cage leans left and falls, the man is pushed/struck and crouches left under it. The man does NOT fall from height — the heavy cage falls onto him. Physically consistent topple.",
    // ④ バケット墜落（手すり越し・フック未掛け）
    "Scene ④: A Japanese self-propelled articulating-boom aerial work platform (高所作業車), basket raised high inside a venue. A Japanese worker in helmet (chin strap) and full-body harness leans his upper body far out over the basket guardrail and is losing balance, tipping head-first OUTWARD and DOWNWARD over the rail (gravity-natural fall direction). His harness lanyard hook hangs UNCLIPPED and loose. Emphasis: fall outward over the guardrail.",
    // ⑤ 車両転倒（不整地・アウトリガー未設置）
    "Scene ⑤: The WHOLE Japanese self-propelled boom aerial work platform VEHICLE is TIPPING OVER. On uneven/sloping ground with outrigger legs NOT deployed, the wheels on one side LIFT OFF the ground and the entire machine — chassis, boom and raised basket — topples steeply to one side. The Japanese worker stays INSIDE the basket and is carried sideways-and-down together WITH the machine, gripping the rail. The MACHINE itself is falling over (not a man leaning out). Wide view showing the tilted chassis and lifted wheels.",
    // ⑥ 上方はさまれ
    "Scene ⑥: Inside a Japanese exhibition hall, a Japanese aerial work platform basket has been raised TOO HIGH, so the Japanese worker's helmet and upper back are being PINCHED between the basket's top guardrail and a steel ceiling beam directly above him. He CROUCHES and ducks LOW INSIDE the basket, pressing down to avoid the beam squeezing him from above. He stays inside the basket (does NOT lean out). Show the heavy overhead steel beam pressing close down onto the basket rail — a clear overhead squeeze/pinch.",
  ],
  get photo() { return this.illust; }, // 同一の状況・物理。スタイルだけ STYLE.photo で差し替え
};
