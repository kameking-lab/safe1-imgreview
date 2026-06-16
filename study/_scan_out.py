# -*- coding: utf-8 -*-
import re
raw = open(r'C:\Users\kanet\AppData\Local\Temp\tsutatsu.htm','rb').read()
t = raw.decode('cp932', errors='replace')
t = re.sub(r'<[^>]+>', ' ', t)
t = t.replace('&nbsp;',' ').replace('&#9312;','(1)').replace('&#9313;','(2)').replace('&#9314;','(3)').replace('&#9315;','(4)').replace('&#9316;','(5)')
t = re.sub(r'\s+', ' ', t)
open(r'C:\Users\kanet\20260522\safe1\study\_scan_result.txt','w',encoding='utf-8').write(t[4600:6200])
print('len',len(t))
