# -*- coding: utf-8 -*-
"""proto_compare.pdf : 診断要約→手法ごとの試作(大判)＋ねらい/弱点→比較＋CLI推奨。"""
import os, textwrap
from PIL import Image, ImageDraw, ImageFont
BASE=r"C:\Users\kanet\20260522\safe1"; PR=os.path.join(BASE,"images","proto")
PW,PH=1240,1754; M=60
def font(sz,b=True):
    for p in ([r"C:\Windows\Fonts\YuGothB.ttc",r"C:\Windows\Fonts\meiryob.ttc"] if b else [r"C:\Windows\Fonts\YuGothR.ttc",r"C:\Windows\Fonts\meiryo.ttc"]):
        if os.path.exists(p):
            try: return ImageFont.truetype(p,sz)
            except: pass
    return ImageFont.load_default()
FT=font(44); FH=font(34); FM=font(26,False); FS=font(22,False); FB2=font(28)
pages=[]
def wrap(d,t,f,maxw):
    out=[]; cur=""
    for ch in t:
        if ch=="\n": out.append(cur); cur=""; continue
        if d.textlength(cur+ch,font=f)<=maxw: cur+=ch
        else: out.append(cur); cur=ch
    if cur: out.append(cur)
    return out
def textpage(title, body, head_col=(192,57,43)):
    im=Image.new("RGB",(PW,PH),"white"); d=ImageDraw.Draw(im)
    d.rectangle([0,0,PW,96],fill=head_col); d.text((M,26),title,font=FT,fill="white")
    y=140
    for para in body:
        col=para.get("c",(20,20,20)); f=para.get("f",FM); t=para.get("t","")
        for ln in wrap(d,t,f,PW-2*M):
            d.text((M,y),ln,font=f,fill=col); y+=f.size+10
        y+=para.get("sp",8)
    pages.append(im)
def imgpage(title, imgpath, note):
    im=Image.new("RGB",(PW,PH),"white"); d=ImageDraw.Draw(im)
    d.rectangle([0,0,PW,70],fill=(35,35,35)); d.text((M,14),title,font=FH,fill="white")
    pic=Image.open(imgpath).convert("RGB")
    maxw=PW-2*M; maxh=PH-360
    r=min(maxw/pic.width,maxh/pic.height); pic=pic.resize((int(pic.width*r),int(pic.height*r)),Image.LANCZOS)
    im.paste(pic,((PW-pic.width)//2,100))
    y=100+pic.height+24
    d.line([(M,y),(PW-M,y)],fill=(200,200,200),width=2); y+=14
    for para in note:
        for ln in wrap(d,para["t"],FS,PW-2*M):
            d.text((M,y),ln,font=FS,fill=para.get("c",(40,40,40))); y+=FS.size+8
        y+=6
    pages.append(im)

# 表紙＋診断要約
textpage("AI画像 失敗の診断 と 複数手法の試作（停止用・比較）",[
 {"t":"対象事例：② テールゲートリフターでの『荷の落下・下敷き』(厚労省あんぜんサイト No.101281)","f":FB2,"sp":14},
 {"t":"選定理由：過積載1.2t→入口へ下る傾斜→後方が沈み後傾→機械が滑落→下敷き、という4段の『因果連鎖』を持ち、各手法が“因果・力の向き・危険点”をどれだけ正確に伝えられるかを最もよく試せるため。","sp":18},
 {"t":"■ 診断（要約）","f":FB2,"c":(192,57,43),"sp":6},
 {"t":"・v4〜v12が失敗した根本：写実/作画の“見た目”を最適化したが、本資料が要るのは“因果の正しさ”で別物。AIは多体の力学(向き・接触・重心)を持たず、もっともらしいが向きの誤った絵を出す（例:荷は右へ・人は左へ）。"},
 {"t":"・本資料が要るもの：何が・どちらに・なぜ(因果・力の向き・危険点)が一目で正しく伝わること。写実は不要どころか、誤った力学を“本物そっくりの嘘”に見せて有害＝負債。"},
 {"t":"・改善方針：向き/接触/危険点/要因を“コードで制御”し、AIには制御可能な範囲(背景・素材の絵柄)だけ担わせる。優先1=M1模式図、2=M3ハイブリッド、3=M2パーツ合成。","sp":14},
 {"t":"※ 本PDFは比較用。最終手法の決定は人間が行う前提（自己判定で『完成』とはしない）。","c":(120,120,120)},
])
# M1
textpage("手法M1：純・模式図（コードで作画）",[
 {"t":"ねらい：幾何・向き・接触点・危険点・要因ラベルを全て作者がコードで指定。AI破綻ゼロ・商標ゼロ・向きの誤りが原理的に出ない。連鎖図で『因果』を明示。","sp":10},
 {"t":"次ページ：単一シーン図 と 4コマ連鎖図。","c":(120,120,120)},
])
imgpage("M1-a：単一シーン図", os.path.join(PR,"m1_scene.png"),
 [{"t":"ねらい：傾斜→後傾→機械が右下へ滑落→人が同方向に下敷き、を矢印と！で明示。"},
  {"t":"残る弱点：意匠が素朴（教材的）。写真の臨場感は無い（が本用途では不要）。"}])
imgpage("M1-b：因果の連鎖図（4コマ）", os.path.join(PR,"m1_chain.png"),
 [{"t":"ねらい：①過積載→②傾斜で後傾→③滑落→④下敷き、の向きを全コマで一致させ“なぜ”を伝える。"},
  {"t":"残る弱点：コマ数ぶん紙幅を取る。"}])
# M2
imgpage("手法M2：パーツ合成（AI素材＋座標制御）", os.path.join(PR,"m2_composite.png"),
 [{"t":"ねらい：トラック/機械/作業者をAIで別々生成→白キー切抜き→作者が座標で配置し、荷の倒れる向きと人の倒れる向き・接触点を一致させる。"},
  {"t":"達成：荷(右下へ後傾)・人(左向きで受け)・赤矢印が同方向で一致＝向きの制御は実現。"},
  {"t":"残る弱点：3素材の絵柄・線の太さ・光が不統一（トラックは無彩色、機械は多色、人は別タッチ）。切抜き縁や接触の精度も中程度。AI素材依存ゆえ生成・DLが不安定（今回もDL失敗をスクショ救済）。"}])
# M3
imgpage("手法M3：ハイブリッド（AI背景＋コード上乗せ）", os.path.join(PR,"m3_hybrid.png"),
 [{"t":"ねらい：AIで“事故でない”素のトラックだけ綺麗に出し（向きの責任を負わせない）、人・荷・赤矢印・危険点はコードで制御して上乗せ。"},
  {"t":"達成：見栄え(AIの綺麗なトラック)と因果の正確さ(コードの向き制御)を両立。"},
  {"t":"残る弱点：AIトラックの写実度とコード図形の素朴さに段差。背景AIの生成・DLは不安定。"}])
# 比較＋推奨
textpage("比較 と CLIの推奨（決定は人間）",[
 {"t":"評価軸：因果の正確さ／向きの一致／危険点の明示／作り物っぽさ(低いほど良)","f":FB2,"sp":12},
 {"t":"M1 純模式図 ： 因果=◎  向き一致=◎  危険点=◎  作り物っぽさ=無（記号図）  → 最も確実・再現可能・量産容易。","sp":6},
 {"t":"M3 ハイブリッド： 因果=◎  向き一致=◎  危険点=◎  作り物っぽさ=小（AI背景に段差）  → 見栄えと正確さの両立。","sp":6},
 {"t":"M2 パーツ合成 ： 因果=○  向き一致=◎  危険点=◎  作り物っぽさ=中（素材の不統一）  → 向き制御は可能だが絵柄統一と工数・AI依存が課題。","sp":16},
 {"t":"■ CLIの推奨","f":FB2,"c":(192,57,43),"sp":6},
 {"t":"主：M1（純・模式図）。本資料の核心要件“因果・向き・危険点が一目で正しく”を最も確実に満たし、6事例の量産・改訂も容易。連鎖図で“なぜ”まで伝わる。"},
 {"t":"副：見栄えを上げたい表紙級カットのみ M3（AI背景＋コード上乗せ）。M2は『向きはコードで一致できる』証明として価値はあるが、絵柄統一とAI依存のコストが高く主力には推さない。"},
 {"t":"M2の向き一致：達成（座標制御で荷・人・矢印を同方向にできた）。ただし素材の絵柄・光の不統一は未解決。","c":(192,57,43),"sp":14},
 {"t":"※ 最終決定は人間が行う前提。ここで停止（6事例の量産はしない）。","c":(120,120,120)},
])
out=os.path.join(BASE,"proto_compare.pdf")
pages[0].save(out,save_all=True,append_images=pages[1:],resolution=150.0)
print(f"saved {out} ({len(pages)} pages)")
