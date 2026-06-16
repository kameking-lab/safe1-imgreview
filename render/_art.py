from PIL import Image
# 破綻が出やすい人物(手/顔)を拡大: illust gen04, photo gen04, photo gen01
specs=[("illust_v5_clean","gen04",0.45,0.05,0.95,0.55),
       ("photo_v5_clean","gen04",0.25,0.05,0.75,0.6),
       ("photo_v5_clean","gen01",0.40,0.20,0.80,0.75)]
for k,f,a,b,c,d in specs:
    im=Image.open(fr"images\{k}\{f}.png"); W,H=im.size
    im.crop((int(W*a),int(H*b),int(W*c),int(H*d))).save(fr"render\_art_{k}_{f}.png")
print("ok")
