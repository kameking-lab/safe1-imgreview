from PIL import Image
im = Image.open("IMG_9864.png")
# footer strip region (dots + HAKUTEN logo + page number)
foot = im.crop((740, 1008, 1260, 1060))
foot.resize((foot.width*3, foot.height*3), Image.LANCZOS).save("render/_footer_big.png")
foot.save("images/ref/footer_strip_raw.png")
print("footer", foot.size)
