import re, sys
path = sys.argv[1]
needle = sys.argv[2]
before = int(sys.argv[3]) if len(sys.argv) > 3 else 60
after = int(sys.argv[4]) if len(sys.argv) > 4 else 260
t = open(path, encoding='utf-8').read()
t = re.sub(r'<[^>]*>', '', t).replace('　', ' ')
start = 0
for _ in range(int(sys.argv[5]) if len(sys.argv) > 5 else 1):
    m = t.find(needle, start)
    if m < 0:
        break
    seg = re.sub(r'\s+', ' ', t[max(0, m - before):m + after]).strip()
    sys.stdout.buffer.write(('--- match ---\n' + seg + '\n').encode('utf-8'))
    start = m + 1
