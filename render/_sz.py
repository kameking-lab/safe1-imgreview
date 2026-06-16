from PIL import Image
import os
d=r"images\gen"
for i in range(1,7):
    im=Image.open(os.path.join(d,f"gen0{i}.png"))
    print(f"gen0{i}", im.size, round(im.size[0]/im.size[1],3))
