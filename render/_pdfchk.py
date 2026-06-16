from PIL import Image
import importlib.util, sys
# build_candidates_pdf の pages を流用せず、PDF先頭ページ確認用に簡易再現は重いので、
# 代わりに保存済み候補1枚を実寸確認 + PDFの妥当性(ページ数)を確認
import struct
with open("candidates_v12.pdf","rb") as f: data=f.read()
print("PDF bytes:", len(data), "startsPDF:", data[:5]==b"%PDF-")
# 事例1 illust 01 を実寸表示用に縮小保存
im=Image.open(r"images\cand_v12_clean\case1\illust\01.png")
print("c1 illust01 size:", im.size)
