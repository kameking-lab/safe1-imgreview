import csv, os
from PIL import Image
base=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
idx=os.path.join(base,'img_index.csv')
imgdir=os.path.join(base,'img')
rows=list(csv.DictReader(open(idx,encoding='utf-8')))

def dhash(path, hs=8):
    im=Image.open(path)
    try:
        im.seek(0)  # first frame for gif
    except Exception:
        pass
    im=im.convert('L').resize((hs+1, hs), Image.LANCZOS)
    px=list(im.getdata())
    bits=0; i=0
    for r in range(hs):
        row=px[r*(hs+1):(r+1)*(hs+1)]
        for c in range(hs):
            bits = (bits<<1) | (1 if row[c] < row[c+1] else 0)
            i+=1
    return bits

def ham(a,b):
    return bin(a^b).count('1')

h={}
for r in rows:
    fn=r['ファイル名']
    h[fn]=dhash(os.path.join(imgdir,fn))

items=list(h.items())
near=[]
for i in range(len(items)):
    for j in range(i+1,len(items)):
        d=ham(items[i][1],items[j][1])
        if d<=5:
            near.append((items[i][0],items[j][0],d))
print("near-duplicate pairs (dHash hamming<=5):", len(near))
for a,b,d in sorted(near,key=lambda x:x[2]):
    print(f"  {a} <-> {b}  dist={d}")
