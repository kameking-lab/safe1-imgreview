from PIL import Image
im=Image.open(r"images\photo_v5\gen01.png"); W,H=im.size
# 作業者の頭部付近(中央やや左上)を拡大
im.crop((int(W*0.42),int(H*0.18),int(W*0.66),int(H*0.5))).resize((360,420)).save(r"render\_head01.png")
print("ok")
