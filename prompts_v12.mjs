// v12 候補出し用プロンプト：物理整合・日本ローカライズ・5アプローチ
export const STYLE = {
  illust:
    "Professional Japanese occupational-safety training ILLUSTRATION, realistic semi-painterly FULL COLOUR, soft cel-shading, real depth and perspective. " +
    "Setting unmistakably in JAPAN (domestic logistics warehouse / construction site / event hall; Japanese fixtures, signage feel, floor-protection). " +
    "Worker = a JAPANESE man; Japanese PPE: safety helmet WITH CHIN STRAP, work jacket or hi-vis, safety boots (full-body fall-arrest harness for aerial work). " +
    "Equipment = Japanese-spec: a folding/retractable tail-lift on the truck rear, or a Japanese self-propelled / truck-mounted aerial work platform. " +
    "Worker and equipment fully integrated in the same light (never a flat cut-out). The CAUSE object must be clearly visible in frame. " +
    "The victim's posture, centre of gravity and direction of motion must MATCH the physics of the accident. " +
    "NO Japanese text, NO letters, NO numbers, NO logos, NO watermark. No blood, no gore, no injury detail — show only the dangerous moment.",
  photo:
    "Photorealistic DOCUMENTARY PHOTOGRAPH taken in JAPAN (domestic warehouse / construction site / event hall, Japanese signage and fixtures). " +
    "Worker = a JAPANESE man in Japanese site PPE: helmet WITH CHIN STRAP, hi-vis or work jacket, safety boots (full-body harness for aerial work). " +
    "Realistic colours, natural light, candid photojournalism. The CAUSE object clearly visible. " +
    "The victim's posture, centre of gravity and direction of motion must MATCH the physics of the accident. " +
    "Show the worker so the face is not a close-up. NO text overlays, NO logos, NO watermark, no blood, no injury — only the dangerous moment.",
};

export const APPROACH = [
  "Camera: a TRUE SIDE view (side elevation), composed like a mechanics/section diagram so the force directions and the gap/contact point are clearly readable.",
  "Camera: an elevated view from diagonally BEHIND the scene (high three-quarter aerial), looking down.",
  "Camera: a LOW angle very close to the victim (near point-of-view), emphasising the immediate danger; wide lens feel.",
  "Moment: JUST BEFORE the accident — the precursor instant (machine/load only beginning to tilt, foot about to slip, a tilt/warning sign), tension building.",
  "Moment: THE INSTANT of the accident — peak motion and the causal climax (the pinch closing / the topple striking / the fall beginning), maximum dynamism.",
];

export const SCN = {
  1: "Scenario (TGL pinch): At the rear of a Japanese 2-ton truck fitted with a folding tail-lift. The worker stands right beside the platform pressing the control switch mounted on the truck-bed rear (NOT using the remote control) to raise the loaded platform; tall boxes leaning against the truck-bed rear catch on already-loaded boxes, and as the worker leans in to check while still pressing the switch, his head and upper body are caught and PINCHED in the closing gap between the rising platform edge and the truck-bed rear edge. Focus on the pinch point (head between platform and bed). He is leaning in / upright, NOT falling.",
  2: "Scenario (load fall): At the rear of a Japanese truck whose folding tail-lift carries a heavy machine (~1.2t, over the 1t limit). The truck is parked on ground sloping DOWN toward a warehouse entrance, so the truck rear sinks and the heavy machine tips BACKWARD and DOWN off the platform; the worker beside/behind is crushed underneath as the machine falls the same backward-down direction. Show the overloaded high machine and the sloped ground as the causes.",
  3: "Scenario (cart topple): At the rear of a Japanese truck, a tail-lift is lowering light empty carts (~30kg). As the lift stopper is released, a heavy loaded roll-cart (~200kg) on the truck bed topples sideways, strikes the empty cart on the platform, and the whole mass leans and falls toward the worker on the platform, knocking him the same direction. Show the heavy 200kg cart toppling onto the lighter cart; the worker is struck, not falling from height.",
  4: "Scenario (machine tip-over): A Japanese self-propelled aerial work platform (~12m) set on an uneven temporary path on a slope (about 6-8 degrees) with NO steel base plates underneath, doing tree-branch cutting. The ground subsides unevenly and the WHOLE machine tips over BACKWARD; the boom, basket and the worker inside all fall the same backward direction toward the ground. Show the rough sloped ground, the absence of steel base plates, and the machine tilting past balance.",
  5: "Scenario (overhead pinch): A Japanese aerial work platform (~14.8m) working under a concrete bridge girder. After formwork removal the operator mis-operates the deck retraction and the boom extends the wrong way (upward), so the worker is PINCHED between the deck console guardrail and the underside of the bridge girder directly above him. Show the very narrow closing gap between the platform rail and the overhead girder; the worker squeezed upward against the girder.",
  6: "Scenario (runaway pinch): A Japanese aerial work platform on a residential road slope (about 11.5 degrees) rolling away downhill (brake not set). The worker tries to stop it by hand and goes down the slope with the machine; at the bottom his foot is caught in an uncovered roadside ditch and his abdomen is pinched between the machine's outrigger base and the edge of the ditch. Show the slope, the rolling machine and the ditch as the causes.",
};
