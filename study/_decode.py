import sys, re
src, needle = sys.argv[1], sys.argv[2]
before = int(sys.argv[3]) if len(sys.argv) > 3 else 60
after = int(sys.argv[4]) if len(sys.argv) > 4 else 120
n = int(sys.argv[5]) if len(sys.argv) > 5 else 3
raw = open(src, 'rb').read()
for enc in ('cp932', 'shift_jis', 'euc_jp', 'utf-8'):
    try:
        t = raw.decode(enc, errors='replace')
    except Exception:
        continue
    t2 = re.sub(r'<[^>]*>', '', t).replace('　', ' ')
    if needle in t2:
        start = 0
        cnt = 0
        out = []
        while cnt < n:
            m = t2.find(needle, start)
            if m < 0:
                break
            seg = re.sub(r'\s+', ' ', t2[max(0, m - before):m + after]).strip()
            out.append(seg)
            start = m + 1
            cnt += 1
        sys.stdout.buffer.write(('[enc=%s found=%d]\n' % (enc, t2.count(needle))).encode('utf-8'))
        for s in out:
            sys.stdout.buffer.write(('--- ' + s + '\n').encode('utf-8'))
        break
else:
    sys.stdout.buffer.write(('NOT FOUND in any encoding: ' + needle + '\n').encode('utf-8'))
