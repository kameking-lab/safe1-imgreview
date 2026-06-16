from PIL import Image
im = Image.open("IMG_9864.png")
W,H = im.size
# crop two slide bands (full width), based on visual proportions
s1 = im.crop((0, int(H*0.30), W, int(H*0.50)))
s2 = im.crop((0, int(H*0.50), W, int(H*0.70)))
s1.save("render/_slide1_crop.png")
s2.save("render/_slide2_crop.png")
# upscale for readability
for name,img in [("s1",s1),("s2",s2)]:
    img.resize((img.width*2, img.height*2), Image.LANCZOS).save(f"render/_{name}_big.png")
print("saved", s1.size, s2.size)
