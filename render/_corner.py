from PIL import Image
# 右下隅を拡大して透かし/スパークルの有無を確認
for kind in ("illust_v5","photo_v5"):
    im=Image.open(fr"images\{kind}\gen01.png")
    W,H=im.size
    c=im.crop((W-150,H-110,W,H)).resize((300,220))
    c.save(fr"render\_corner_{kind}.png")
print("ok")
