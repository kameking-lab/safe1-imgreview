from PIL import Image
im=Image.open(r"render\illust_v5\slide04.png")
W,H=im.size
# 左の画像エリア(おおよそ x0-0.62W, y0.18H-0.90H)を拡大
crop=im.crop((int(W*0.02), int(H*0.16), int(W*0.63), int(H*0.92)))
crop.save(r"render\_il4_crop.png")
print(crop.size)
