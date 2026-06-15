import unicodedata, sys

def dispcol(s, charidx):
    col = 0
    for c in s[:charidx]:
        col += 2 if unicodedata.east_asian_width(c) in ('W', 'F') else 1
    return col

lines = open('QIITA_evo_zh.md', encoding='utf-8').read().splitlines()
for n in range(2147, 2155):
    l = lines[n - 1]
    fwd = [i for i, c in enumerate(l) if c == '/']
    bwd = [i for i, c in enumerate(l) if c == '\\']
    info = ''
    if fwd:
        info += ' firstFwd@' + str(dispcol(l, fwd[0])) + ' lastFwd@' + str(dispcol(l, fwd[-1]))
    if bwd:
        info += ' lastBwd@' + str(dispcol(l, bwd[-1]))
    print(n, info, '|', l)
