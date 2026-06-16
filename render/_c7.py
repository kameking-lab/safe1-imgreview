from PIL import Image
specs=[("illust_v7","gen01",0.0,0.0,0.55,0.7),
       ("illust_v7","gen03",0.45,0.2,1.0,0.9),
       ("illust_v7","gen04",0.3,0.1,0.95,0.8),
       ("photo_v7","gen01",0.25,0.0,0.85,0.7),
       ("photo_v7","gen04",0.2,0.0,0.85,0.75)]
for k,f,a,b,c,d in specs:
    im=Image.open(fr"images\{k}\{f}.png"); W,H=im.size
    im.crop((int(W*a),int(H*b),int(W*c),int(H*d))).save(fr"render\_c_{k}_{f}.png")
print("ok")
