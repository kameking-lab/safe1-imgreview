from PIL import Image
for kind in ("illust_v5_clean","photo_v5_clean"):
    im=Image.open(fr"images\{kind}\gen01.png")
    W,H=im.size
    im.crop((W-170,H-150,W,H)).resize((340,300)).save(fr"render\_cc_{kind}.png")
print("ok")
