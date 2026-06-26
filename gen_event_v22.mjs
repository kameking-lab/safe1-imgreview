// gen_event_v22.mjs — aerial2 元絵を参照画像にして「危険姿勢で作業 → 事故への流れを赤/橙の湾曲矢印で図示」する
//   KYT(危険予知)教材イラストを Google gemini-3-pro-image-preview のみで2枚生成（OpenAI 不使用）。
// 使い方: node gen_event_v22.mjs <baseNum> [strong]
//   元の事故の型/原因シナリオは gen_event_v21/event_index_v21.csv 由来（本ファイル内 SCENARIO_BY_NUM に継承）。
//   参照画像は collect_aerial2/aerial2_index.csv の 通し番号→ファイル名 を引き collect_aerial2/img/<file>。
//   出力: gen_event_v22/<baseNum>/{google_1,google_2}.png （既存>4KBは skip＝再開安全・非破壊）。
//   strong を付けると矢印を強調した再生成用プロンプトで google_1b/google_2b.png（新ファイル名・上書きしない）に出力。
//   index(event_index_v22.csv) はこのスクリプトでは追記しない（自己点検後に採用ファイルを別途追記する）。
// 【最重要】各イラストは (1)作業員の不安全な作業姿勢 と (2)そこからどう動いて事故になるか
//   （重心移動／転落・転倒・挟まれの方向）を表す赤/橙の湾曲矢印 を1枚に描く。完全に落下しきった絵にしない。
//   矢印のみ可・他の文字/数字/キャプション/吹き出し/記号なし・流血なし・実在ロゴなし・PPE適切・シザース型のみ。
// キー値は出力しない(.env から読む)。削除/上書き/Chrome killしない。OpenAI 経路は持たない。
import fs from "node:fs";
import path from "node:path";

const BASE = "C:/Users/kanet/20260522/safe1";
const baseNum = String(process.argv[2]||"").trim();
const STRONG = String(process.argv[3]||"").trim().toLowerCase()==="strong";
if(!baseNum){console.error("usage: node gen_event_v22.mjs <baseNum> [strong]");process.exit(2);}

function readEnv(){const o={};const p=path.join(BASE,".env");if(!fs.existsSync(p))return o;
  for(const ln of fs.readFileSync(p,"utf8").split(/\r?\n/)){const m=ln.match(/^([A-Z0-9_]+)=(.*)$/);if(m)o[m[1]]=m[2];}return o;}
const ENV=readEnv();
const GEMINI=ENV.GEMINI_API_KEY||process.env.GEMINI_API_KEY||"";
if(!GEMINI){console.error("GEMINI_API_KEY 未設定(.env)");process.exit(3);}
const sleep=ms=>new Promise(r=>setTimeout(r,ms));

// ---- CSV パース（ダブルクオート対応・最小実装） ----
function parseCsvLine(line){const out=[];let cur="",q=false;
  for(let i=0;i<line.length;i++){const c=line[i];
    if(q){ if(c==='"'){ if(line[i+1]==='"'){cur+='"';i++;} else q=false; } else cur+=c; }
    else { if(c===','){out.push(cur);cur="";} else if(c==='"'){q=true;} else cur+=c; } }
  out.push(cur);return out;}
const csvPath=path.join(BASE,"collect_aerial2/aerial2_index.csv");
const lines=fs.readFileSync(csvPath,"utf8").split(/\r?\n/).filter(Boolean);
const header=parseCsvLine(lines[0]);
const idx=k=>header.indexOf(k);
let row=null;
for(let i=1;i<lines.length;i++){const c=parseCsvLine(lines[i]);if(String(c[idx("通し番号")]).trim()===baseNum){row=c;break;}}
if(!row){console.error(`該当なし: 通し番号 ${baseNum} は CSV に存在しません`);process.exit(4);}
const refFile=row[idx("ファイル名")].trim();
const accType=row[idx("カテゴリ")].trim();
const refPath=path.join(BASE,"collect_aerial2/img",refFile);
if(!fs.existsSync(refPath)){console.error(`該当なし: 参照画像 ${refFile} が見つかりません`);process.exit(4);}

// ---- 番号ごとに「危険姿勢」と「矢印が示す事故への流れ」（gen_event_v21 のシナリオを継承して再構成） ----
//   posture=不安全な作業姿勢/状況（英語=生成用・日本語=記録用） arrow=矢印が示す遷移（英語=生成用・日本語=記録用）
const SCENARIO_BY_NUM={
 "1":{p_ja:"高所作業車(シザースリフト)を上昇させたまま走行させ、組みかけブースのアルミトラスに激突しかけている、手すり際で作業中の不安全状態",
      a_ja:"激突の衝撃で手すり際の作業員がバランスを崩し、手すりを越えて外側・下方へ転落していく向き",
      p_en:"the scissor lift is being DRIVEN/TRAVELLED while still fully elevated and its raised platform is about to SLAM into a half-built aluminium booth truss/signage frame; the worker is standing at the platform edge by the guardrail",
      a_en:"a bold curved red/orange PREDICTION ARROW sweeping from the impact point, over the guardrail and DOWNWARD to show that the collision will throw the edge worker off balance and over the rail toward the floor"},
 "2":{p_ja:"高い看板パネルを取付けようとシザースリフトの手すりに片足を掛けて乗り上がり、身を大きく乗り出した不安全姿勢",
      a_ja:"重心が手すりの外側へ移り、頭から手すりを越えて転落していく向き",
      p_en:"to reach a high signage panel the worker has PUT ONE FOOT UP ONTO THE GUARDRAIL of the scissor-lift platform and is leaning far out over the rail toward the booth panel in a clearly unsafe posture (NOT yet fallen)",
      a_en:"a bold curved red/orange PREDICTION ARROW showing the centre of gravity moving OUTSIDE the rail and the body tipping head-first OVER the guardrail downward"},
 "3":{p_ja:"乗降口の安全チェーン(開閉バー)を掛け忘れ、開いた乗降口の側で高所作業している不安全状態",
      a_ja:"開いた乗降口側へ後退り→ガードのない開口部からそのまま落下していく向き",
      p_en:"the platform ENTRY GATE / safety chain is LEFT UNFASTENED (the entry gap in the guardrail is wide OPEN, the chain dangling unhooked) and the worker is working with his back toward that open gap",
      a_en:"a bold curved red/orange PREDICTION ARROW showing the worker stepping/stumbling BACKWARD toward the open unguarded gate and dropping out through the OPEN gap"},
 "45":{p_ja:"作業床から組みかけブースの未固定トラスへ直接乗り移ろうと跨いでいる(フルハーネスのフック未接続)不安全姿勢",
      a_ja:"機体と未固定トラスの隙間で足を踏み外し、隙間へ転落していく向き",
      p_en:"the worker is CLIMBING ACROSS / STEPPING OVER directly from the scissor-lift platform onto a half-built booth truss to reach a sign, his harness LANYARD HOOK clearly UNCONNECTED and dangling, the unsecured truss shifting (NOT yet fallen)",
      a_en:"a bold curved red/orange PREDICTION ARROW showing his footing slipping and his body dropping into the GAP between the lift and the booth structure"},
 "64":{p_ja:"作業床が届かず、手すりの外へ上半身を大きく乗り出して両腕で背伸び・過伸展している不安全姿勢",
      a_ja:"重心が手すりの外へ出て、頭から手すりを越えて転落していく向き",
      p_en:"the platform was not driven close enough, so the worker LEANS HIS UPPER BODY FAR OUT past the guardrail and over-reaches with both arms toward a tall signage panel beyond arm's reach, feet lifting off the deck (NOT yet fallen)",
      a_en:"a bold curved red/orange PREDICTION ARROW showing the centre of gravity going OUTSIDE the rail and the body pitching head-first OVER the guardrail downward"},
 "91":{p_ja:"作業床の上に脚立/裏返した運搬コンテナを載せ、その上に立ってさらにかさ上げしている不安定な不安全姿勢",
      a_ja:"踏み台がぐらつき重心が崩れ、手すりを越えて頭から転落していく向き",
      p_en:"a SEPARATE STEP-STOOL / small stepladder (or an UPTURNED crate) is placed ON TOP OF the scissor-lift platform deck and the worker is STANDING ON THAT improvised stack to gain extra height, the stool wobbling (NOT yet fallen)",
      a_en:"a bold curved red/orange PREDICTION ARROW showing the wobbly stool tipping and the worker pitching head-first OVER the guardrail downward"},
 "93":{p_ja:"大判で重い看板パネルを一人で抱え上げ、手すり越しに高い位置へ取り付けようとしている過負荷の不安全姿勢",
      a_ja:"重い荷の重量に引かれ重心が手すり外へ→パネルごと手すりを越えて転落していく向き",
      p_en:"a single worker is hoisting a LARGE, HEAVY rigid signage panel up and OUT OVER the guardrail to mount it high on the booth, overbalanced by its weight, arms extended past the rail (NOT yet fallen)",
      a_en:"a bold curved red/orange PREDICTION ARROW showing the heavy load dragging his centre of gravity OUTSIDE the rail and pulling him, still gripping the panel, head-first OVER the guardrail"},
 "94":{p_ja:"スライド式の延長デッキの固定ロックを掛け忘れたまま、その延長部分に乗って看板へ近づこうとしている不安全状態",
      a_ja:"未ロックのスライドデッキがずれて開いた隙間から踏み外し、外側へ転落していく向き",
      p_en:"the SLIDE-OUT DECK EXTENSION of the lift was pushed out but its LOCK PIN LEFT UNSECURED; the worker stands on that unlatched extension and the deck has SHIFTED, opening a gap at the platform edge (NOT yet fallen)",
      a_en:"a bold curved red/orange PREDICTION ARROW showing the worker missing his footing through the opened gap and dropping outside the guardrail"},
 "97":{p_ja:"キャスター(車輪)ブレーキを掛けないまま上昇し、ブースのトラスを手前へ強く引き寄せている不安全状態",
      a_ja:"反動で機体が後方へ動き出し、その揺れで手すり際の作業員が手すりを越えて転落していく向き",
      p_en:"the scissor lift is raised with its base CASTER/WHEEL BRAKES clearly LEFT UNLOCKED (brake levers up, wheels free) while the elevated worker pulls a booth truss strongly toward himself, the unbraked machine starting to roll (NOT yet fallen)",
      a_en:"a bold curved red/orange PREDICTION ARROW at the base showing the unbraked lift rolling/skidding backward, and a second arrow up top showing the abrupt lurch throwing the worker over the guardrail"},
 "100":{p_ja:"組み立て途中でまだブレース固定していない自立壁パネルに、作業床から体重をかけて寄りかかって作業している不安全姿勢",
      a_ja:"支えのない壁パネルが外側へ倒れ、寄りかかった作業員が一緒に引かれて手すりを越えていく向き",
      p_en:"the worker LEANS HIS WEIGHT ON / pushes against a tall FREESTANDING booth wall panel that is NOT YET BRACED OR FIXED (no diagonal braces, base lifting), the panel beginning to topple away (NOT yet fallen)",
      a_en:"a bold curved red/orange PREDICTION ARROW showing the unbraced panel toppling away and the worker being dragged OVER the guardrail together with it"},
 "104":{p_ja:"資材受け渡しのため側面ガードレール(中桟)を倒した/外したまま再固定せず、開いた側で高所作業している不安全状態",
      a_ja:"手すりの無い開いた側面へ後ずさり、ガードのない側面開口部から外へ転落していく向き",
      p_en:"a SIDE SECTION OF THE GUARDRAIL was FOLDED DOWN / removed and LEFT UNSECURED, leaving one side of the platform an OPEN, UNGUARDED EDGE (rails up on the other sides); the worker works near that open side (NOT yet fallen)",
      a_en:"a bold curved red/orange PREDICTION ARROW showing the worker backing toward the open side and dropping OUT THROUGH the missing-rail gap at the side of the platform"},
 "112":{p_ja:"上昇したまま降ろす手間を惜しみ、手すりを乗り越えシザース機構(X字フレーム)に足を掛けて外側からよじ降りようとしている不安全姿勢",
      a_ja:"手すりにまたがった不安定な体勢で足を滑らせ、機体外側を伝って床まで転落していく向き",
      p_en:"instead of lowering the lift the worker is DISMOUNTING AT HEIGHT — climbing OUT OVER the intact top guardrail and putting a foot onto the X-shaped SCISSOR ARMS to climb down the outside of the still-elevated machine (NOT yet fallen)",
      a_en:"a bold curved red/orange PREDICTION ARROW showing his foot slipping off the scissor frame and his body peeling off the OUTSIDE of the lift down toward the floor"},
 "114":{p_ja:"フルハーネスは着用しているが命綱(ランヤード)のフックをアンカーへ接続しないまま、手すり際で看板取付けしている不安全状態",
      a_ja:"体勢を崩し手すりを越えるが、未接続のフックが宙ぶらりんで落下を止められず床まで落ちていく向き",
      p_en:"the worker IS wearing a full-body harness BUT his fall-arrest LANYARD HOOK is NEVER CLIPPED — it hangs FREE and dangling, the anchor rail clearly bare — while he works overbalanced at the platform edge (NOT yet fallen)",
      a_en:"a bold curved red/orange PREDICTION ARROW showing him going OVER the guardrail with the useless dangling lanyard trailing, dropping uninterrupted toward the floor"},
 "137":{p_ja:"作業床に工具・電動ドライバー・とぐろを巻いた延長コード・端材を散乱させたまま高所作業している不安全状態",
      a_ja:"後ずさりした足が散乱物に取られてつまずき、その勢いで手すりを越えて転落していく向き",
      p_en:"the platform DECK IS CLUTTERED — power tools, a coiled extension cord, leftover offcuts LEFT LYING LOOSE all over the floor — and the worker, absorbed in fixing a panel, steps backward with his foot catching on them (NOT yet fallen)",
      a_en:"a bold curved red/orange PREDICTION ARROW showing the trip pitching him backward OVER the guardrail toward the floor"},
 "138":{p_ja:"こぼした塗料/水で濡れて滑りやすい床面を放置したまま、踏ん張って看板取付けしている不安全状態",
      a_ja:"濡れた床で足が前へ滑り、踏ん張りが利かず手すり下/外へ滑り落ちていく向き",
      p_en:"the platform DECK IS WET AND SLIPPERY — a spilled glossy puddle from a tipped paint can/bottle pooled on the deck — and the worker plants his feet to fit a panel, his boot beginning to skid (NOT yet fallen)",
      a_en:"a bold curved red/orange PREDICTION ARROW showing his boot sliding forward and his body sliding OUT and DOWN under/over the guardrail toward the floor"},
 "196":{p_ja:"届かない最上部に手を伸ばすため、上部手すりの最上段に両足で立ち上がって背伸びしている極めて不安定な不安全姿勢",
      a_ja:"不安定な体勢でバランスを崩し、手すりの外側へ落下していく向き",
      p_en:"the worker has CLIMBED UP AND IS STANDING WITH BOTH FEET ON TOP OF THE GUARDRAIL itself, balanced on the narrow top rail well above the deck, over-reaching for the top of a booth truss (NOT yet fallen)",
      a_en:"a bold curved red/orange PREDICTION ARROW showing him overbalancing and toppling OUTWARD off the outside of the platform toward the floor"},
 "215":{p_ja:"定員/積載を超えて複数(3〜4人)の作業員と看板パネル・工具を狭い作業床に詰め込んで同時作業している過密の不安全状態",
      a_ja:"混み合いで押し合い、端の作業員が他の作業員/パネルに押されて手すりの外側へ押し出されていく向き",
      p_en:"the small platform is OVERCROWDED beyond rated capacity — three or four workers crammed on the deck together with bulky panels and tool boxes, shoulder-to-shoulder and jostling (NOT yet fallen)",
      a_en:"a bold curved red/orange PREDICTION ARROW showing the crowding shoving the edge worker against and OVER the guardrail outward toward the floor"},
 "372":{p_ja:"見上げ作業中、操作盤の上昇レバーを腹/身体で押したまま気づかず連続上昇させている挟まれの不安全状態(意図しない連続操作)",
      a_ja:"前かがみの頭・首・胸が上部トラス/天井梁と手すりの間に入り込み、上昇する機体に挟まれ押し潰される向き",
      p_en:"ACCIDENT TYPE IS A CRUSH (nobody falls). The worker is looking UP to fit a high truss while his TORSO/BELLY is UNINTENTIONALLY pressing the UP joystick/lever on the control panel, so the lift KEEPS RISING; his bent-forward head/neck nears the OVERHEAD aluminium booth truss / ceiling beam (NOT yet crushed)",
      a_en:"a bold curved red/orange PREDICTION ARROW showing the platform still rising UPWARD and the narrowing gap, indicating his head/upper body about to be PINNED/CRUSHED between the top guardrail and the overhead truss"},
 "379":{p_ja:"上昇しながら、すぐ脇の固定アルミトラス支柱へ手を伸ばして身を横に乗り出している挟まれの不安全姿勢",
      a_ja:"上昇する作業床の手すりと固定トラス支柱との隙間が狭まり、乗り出した腕/胴が横方向から挟まれる向き",
      p_en:"ACCIDENT TYPE IS A CRUSH (nobody falls). The worker LEANS/REACHES SIDEWAYS toward a FIXED free-standing aluminium booth TRUSS COLUMN beside the platform while the lift KEEPS RISING, his arm/torso in the narrowing SIDE gap (NOT yet crushed)",
      a_en:"a bold curved red/orange PREDICTION ARROW showing the platform rising UPWARD and the side gap closing, indicating his arm/upper body about to be PINNED LATERALLY between the top guardrail and the fixed truss column"},
 "497":{p_ja:"上昇させたままのシザースリフトを搬入口の床ケーブル/段差の上を走行させ、片側のキャスターが乗り上げて機体が傾いている横転の不安全状態",
      a_ja:"重心の高いまま片輪が浮き、支えを失った機体全体が横方向へ倒れていく(横転)向き",
      p_en:"ACCIDENT TYPE IS A TIP-OVER of the whole machine. The fully-elevated scissor lift was DRIVEN over an obstruction and ONE base CASTER HAS RIDDEN UP onto a thick run of FLOOR CABLES / a cable-cover ramp / a floor step, the base now tilted off level (NOT yet fully overturned)",
      a_en:"a bold curved red/orange PREDICTION ARROW arcing sideways to show the high-CG machine losing stability and the ENTIRE LIFT tipping/overturning SIDEWAYS, the elevated platform swinging over"},
 "518":{p_ja:"平らな床で上昇したまま、ずれた重いブース壁パネル/自立トラスを手で強く手前へ引き寄せ、高所で大きな水平力を機体にかけている横転の不安全状態",
      a_ja:"水平方向の反力で重心が支点を越え、床は平らなのに機体全体が押した向きへ横転していく向き",
      p_en:"ACCIDENT TYPE IS A TIP-OVER of the whole machine on FLAT level floor. The fully-elevated worker is HAULING/PULLING a heavy mis-aligned booth panel/truss strongly toward the platform (large HORIZONTAL force at height), far-side base wheels just starting to lift (NOT yet fully overturned)",
      a_en:"a bold curved red/orange PREDICTION ARROW arcing in the direction of the pull to show the high-CG machine overturning SIDEWAYS on the flat floor, the far-side wheels lifting clear"},
 "519":{p_ja:"平床ではなく搬入口のスロープ/傾斜路の上に据えたまま作業床を高く上昇させて作業している横転の不安全状態",
      a_ja:"地面が傾いているため上昇で重心が高くなり、わずかな反動で機体全体が勾配の下り方向へ横転していく向き",
      p_en:"ACCIDENT TYPE IS A TIP-OVER of the whole machine. The scissor lift is FULLY ELEVATED while standing on a SLOPED/INCLINED loading-dock ramp (the ground itself tilted), the whole base already leaning down-slope (NOT yet fully overturned)",
      a_en:"a bold curved red/orange PREDICTION ARROW arcing DOWN-SLOPE to show the high-CG machine toppling SIDEWAYS down the incline, the elevated platform swinging over"},
 "520":{p_ja:"平床で正しく上昇させた機体の基部へ、資材を積んだフォークリフトが前方確認不足で走行してきて側面衝突しかけている横転の不安全状態",
      a_ja:"重心の高い機体が下から突かれて支点を越え、機体全体が衝突方向へ突き倒され横転していく向き",
      p_en:"ACCIDENT TYPE IS A TIP-OVER of the whole machine on FLAT floor. A FORKLIFT carrying a pallet of booth panels, driver's view blocked, is about to RAM the BASE of the fully-elevated scissor lift from the side (NOT yet fully overturned)",
      a_en:"a bold curved red/orange PREDICTION ARROW arcing away from the forklift to show the top-heavy machine being shoved past its stability point and overturning SIDEWAYS in the impact direction"},
 "597":{p_ja:"一見平らな床の床下ピット蓋/グレーチング/軟弱な箇所に片側のベースキャスターを乗せたまま据えて高く上昇させている横転の不安全状態",
      a_ja:"高荷重に床蓋/軟弱地盤が耐えられず陥没・沈み込み、片側のベースが床面より下へ落ち込んで沈んだ側へ横転していく向き",
      p_en:"ACCIDENT TYPE IS A TIP-OVER of the whole machine. One base CASTER rests on UNSTABLE ground — a REMOVABLE FLOOR-PIT LID / cable-trench cover / thin grating — which is CAVING IN under the raised top-heavy load so that wheel is DROPPING DOWN below floor level (NOT yet fully overturned)",
      a_en:"a bold curved red/orange PREDICTION ARROW arcing toward the sunken corner to show the high-CG machine overturning SIDEWAYS as that base wheel sinks into the collapsing floor opening"},
 "914":{p_ja:"上昇した機体の真下/基部で地上作業員が落とした工具を拾おうとX字機構の下へ侵入し、上では確認せず下降操作している挟まれの不安全状態",
      a_ja:"降りてくる作業床の底面と閉じていくX字リンク機構・基部フレームとの間に、下の作業員が挟まれ押し潰される向き",
      p_en:"ACCIDENT TYPE IS A CAUGHT-BETWEEN/CRUSH at GROUND LEVEL (nobody falls from height). A GROUND-LEVEL worker has crouched/reached IN UNDER the raised platform and into the open X-shaped SCISSOR LINKAGE to grab a dropped tool, with NO barricade and NO spotter, while the operator above is LOWERING the lift without checking below (NOT yet crushed)",
      a_en:"a bold curved red/orange PREDICTION ARROW pointing DOWNWARD with the descending platform / closing scissor X-arms, indicating the ground worker about to be PINNED/CRUSHED between the lowering deck and the floor"},
};
// 型ごとのフォールバック（番号未定義時のみ）
const SCEN_BY_TYPE={
 "墜落・転落":{p_ja:"手すりに足を掛け/身を乗り出した不安全姿勢で看板を取付け",a_ja:"重心が手すり外へ移り手すりを越えて転落していく向き",
   p_en:"a worker on the scissor-lift platform overreaches / puts a foot on or leans over the guardrail to fix a signage panel in an unsafe posture (NOT yet fallen)",
   a_en:"a bold curved red/orange PREDICTION ARROW showing the centre of gravity moving outside the rail and the body tipping OVER the guardrail downward"},
 "転倒・横転":{p_ja:"接地不良/段差・ケーブルに片輪が乗り上げ上昇したまま作業",a_ja:"機体全体が傾いて横転していく向き",
   p_en:"the fully-elevated scissor lift has one wheel ridden up on a floor step/cable or stands on uneven ground, the base tilting (NOT yet fully overturned)",
   a_en:"a bold curved red/orange PREDICTION ARROW arcing sideways to show the whole machine overturning"},
 "挟まれ":{p_ja:"下降操作中に身体/手を機構の隙間や什器との間に入れている不安全状態",a_ja:"閉じる機構/降下する床との間に挟まれていく向き",
   p_en:"a body part is inside the closing scissor linkage or between a heavy panel and a fixture while the mechanism moves (NOT yet crushed)",
   a_en:"a bold curved red/orange PREDICTION ARROW along the closing mechanism showing the pinch about to happen"},
 "その他":{p_ja:"ブース設営中の不安全な作業姿勢/状態",a_ja:"そのまま事故になる方向",
   p_en:"a clear unsafe act/condition on a scissor lift during booth setup (NOT yet an accident)",
   a_en:"a bold curved red/orange PREDICTION ARROW showing the direction it becomes an accident"},
};
const typeKey=SCEN_BY_TYPE[accType]?accType:(Object.keys(SCEN_BY_TYPE).find(k=>k!=="その他"&&(accType.startsWith(k)||accType.includes(k)))||"その他");
const scen=SCENARIO_BY_NUM[baseNum]||SCEN_BY_TYPE[typeKey];

// ---- 統一スタイル（矢印のみ可・他の文字は一切なし） ----
const STYLE=[
 "High-quality, realistic Japanese workplace-safety educational illustration (clean professional art with rich shading, depth and a sense of presence). Do NOT imitate the source picture's drawing style; only inherit its accident TYPE. The source image is a reference for the hazard type only.",
 "Setting: a JAPANESE EXHIBITION HALL / trade-show booth SETUP site (half-built exhibition booths, aluminium truss frames, large blank signage panels, display fixtures, cardboard crates, floor cable runs and small floor steps, a loading dock in the background).",
 "Workers: Japanese exhibition crew wearing chin-strap helmets, hi-vis vests, work gloves and safety boots; when at height they wear a full-body safety harness.",
 "Any aerial work platform MUST be a SCISSOR LIFT only (vertical scissor-type elevating platform). Never a boom lift or truck-mounted boom.",
 "The ONLY graphic mark allowed is the bold curved red/orange PREDICTION ARROW(S). There must be NO text, NO letters, NO numbers, NO captions, NO speech bubbles, NO other symbols anywhere. No blood/gore. No real brand names or real logos. Proper PPE on workers.",
].join(" ");
const MOST_IMPORTANT="MOST IMPORTANT: this is a KYT HAZARD-PREDICTION diagram. Draw the worker STILL IN THE UNSAFE POSTURE at the moment JUST BEFORE the accident — do NOT draw a person already fully fallen, already crushed, or already lying on the ground. Instead, clearly add the bold curved red/orange PREDICTION ARROW(S) that show how the worker will move / how the centre of gravity shifts / the direction of the resulting fall, tip-over or crush. A viewer must instantly read from the arrow what is about to happen. The arrow must be large, vivid red-to-orange, curved, and unmistakably the focal directional cue.";
const STRONG_EXTRA=STRONG?" EXTRA EMPHASIS: the previous attempt's PREDICTION ARROW was missing or unclear. Make ONE or TWO big, thick, glowing red/orange CURVED arrows the most prominent element, starting at the unsafe posture and sweeping in the exact direction of the fall/tip-over/crush, with a clear arrowHEAD. Keep the worker NOT-yet-fallen. Still absolutely no text or numbers.":"";
const VARIANTS=[
 "Composition A: wide angle showing the whole scissor lift, the half-built booth and the unsafe posture clearly, with one large sweeping red/orange prediction arrow tracing the path to the accident.",
 "Composition B: closer dramatic angle on the unsafe posture, with the red/orange curved prediction arrow(s) prominent and the direction of motion unmistakable.",
];
const buildPrompt=(vi)=>`Unsafe posture/condition to depict: ${scen.p_en}. Prediction arrow to draw: ${scen.a_en}. ${MOST_IMPORTANT}${STRONG_EXTRA} ${STYLE} ${VARIANTS[vi%VARIANTS.length]}`;

// ---- 参照画像 ----
const refBuf=fs.readFileSync(refPath);
const refMime=refFile.toLowerCase().endsWith(".png")?"image/png":refFile.toLowerCase().endsWith(".webp")?"image/webp":refFile.toLowerCase().endsWith(".gif")?"image/gif":"image/jpeg";

async function genGoogle(prompt){
  const model="gemini-3-pro-image-preview";let last="";
  for(let a=0;a<4;a++){try{
    const body={contents:[{parts:[{inlineData:{mimeType:refMime,data:refBuf.toString("base64")}},{text:prompt}]}],generationConfig:{responseModalities:["IMAGE"]}};
    const r=await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`,{method:"POST",headers:{"Content-Type":"application/json","x-goog-api-key":GEMINI},body:JSON.stringify(body)});
    if(r.status===429||r.status>=500){last=`http ${r.status}`;await sleep(3500*2**a);continue;}
    const j=await r.json();const parts=j?.candidates?.[0]?.content?.parts||[];
    const img=parts.find(p=>p.inlineData?.data||p.inline_data?.data);
    if(img)return(img.inlineData||img.inline_data).data;
    last=j?.error?.message||JSON.stringify(j).slice(0,200);
    if(/RESOURCE_EXHAUSTED|quota|rate/i.test(last)){console.error("RATE/QUOTA:",last.slice(0,120));await sleep(4000*2**a);continue;}
    await sleep(2500*2**a);
  }catch(e){last=e.message;await sleep(2500*2**a);}}
  throw new Error("google: "+last);
}

const outDir=path.join(BASE,"gen_event_v22",baseNum);
fs.mkdirSync(outDir,{recursive:true});
const sfx=STRONG?"b":"";
const jobs=[
  {name:`google_1${sfx}.png`,fn:()=>genGoogle(buildPrompt(0))},
  {name:`google_2${sfx}.png`,fn:()=>genGoogle(buildPrompt(1))},
];
let ok=0,failed=[];
for(const j of jobs){
  const out=path.join(outDir,j.name);
  if(fs.existsSync(out)&&fs.statSync(out).size>4000){console.log("skip(exists)",out);ok++;continue;}
  try{const b64=await j.fn();fs.writeFileSync(out,Buffer.from(b64,"base64"));console.log("saved",out);ok++;}
  catch(e){console.error("FAIL",j.name,"-",String(e.message).slice(0,160));failed.push(j.name);}
}
console.log(`DONE base=${baseNum} type=${accType} ref=${refFile} strong=${STRONG} posture="${scen.p_ja}" arrow="${scen.a_ja}" ok=${ok}/2 failed=${failed.join(",")||"none"}`);
process.exit(failed.length?1:0);
