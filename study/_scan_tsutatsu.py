# -*- coding: utf-8 -*-
import re
raw = open(r'C:\Users\kanet\AppData\Local\Temp\tsutatsu.htm','rb').read()
t = raw.decode('cp932', errors='replace')
t = re.sub(r'<[^>]+>', ' ', t)
t = t.replace('&nbsp;', ' ')
t = re.sub(r'[ \t　]+', ' ', t)
kws = ['第三十六条','第百五十一条の六十七','第百五十一条の七十四','第五号の四',
       '令和五年','第三十三号','令和六年二月一日','令和五年十月一日',
       'テールゲートリフター','動力','昇降設備','保護帽','経過措置','四時間','二時間']
for kw in kws:
    i = t.find(kw)
    if i >= 0:
        print('### FOUND', kw, '@', i)
        print('   ', t[max(0,i-60):i+120].replace('\n',' '))
    else:
        print('### MISS ', kw)
