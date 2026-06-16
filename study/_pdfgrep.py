import sys, re
import fitz
path = sys.argv[1]
needles = sys.argv[2].split('|')
doc = fitz.open(path)
full = []
for pg in doc:
    full.append(pg.get_text())
t = '\n'.join(full)
t2 = re.sub(r'[ \t]+', ' ', t)
for nd in needles:
    idxs = [m.start() for m in re.finditer(re.escape(nd), t2)]
    sys.stdout.buffer.write(('\n=== %s (count=%d) ===\n' % (nd, len(idxs))).encode('utf-8'))
    for i in idxs[:3]:
        seg = re.sub(r'\s+', ' ', t2[max(0, i - 90):i + 140]).strip()
        sys.stdout.buffer.write(('--- ' + seg + '\n').encode('utf-8'))
