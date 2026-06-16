import re, io, sys
raw = open(r'C:/Users/kanet/AppData/Local/Temp/aerial_law.txt', encoding='utf-8').read()
t = re.sub(r'<[^>]*>', '', raw)
t = t.replace('　', ' ')
heads = sorted(set(re.findall(r'第百九十四条の[一二三四五六七八九十]+', t)), key=lambda x: t.find(x))
positions = sorted([(t.find(h), h) for h in set(re.findall(r'第百九十四条の[一二三四五六七八九十]+', t)) if t.find(h) >= 0])

def block(a, lim=900):
    s = t.find(a)
    if s < 0:
        return '(not found)'
    nxt = len(t)
    for pos, h in positions:
        if pos > s and pos < nxt:
            nxt = pos
    seg = re.sub(r'\s+', ' ', t[s:nxt]).strip()
    return seg[:lim]

out = io.StringIO()
for a in ['第百九十四条の八','第百九十四条の九','第百九十四条の十','第百九十四条の十一','第百九十四条の十五','第百九十四条の二十','第百九十四条の二十二','第百九十四条の二十三','第百九十四条の二十七','第百九十四条の二十八']:
    out.write('\n### ' + a + '\n')
    out.write(block(a) + '\n')
sys.stdout.buffer.write(out.getvalue().encode('utf-8'))
