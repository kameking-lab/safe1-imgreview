from PIL import Image
for n in (4,8,10):
    im=Image.open(fr"render\photo_v5\slide{n:02d}.png")
    W,H=im.size
    crop=im.crop((int(W*0.02), int(H*0.16), int(W*0.63), int(H*0.92)))
    crop.save(fr"render\_ph{n}_crop.png")
print("ok")
