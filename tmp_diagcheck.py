import unicodedata
def w(s):
    return sum(2 if unicodedata.east_asian_width(c) in ('W','F') else 1 for c in s)
BS = chr(92)
orig = {
 2215: ' 良さ↑                                  /' + BS,
 2216: '     |                                 /  ' + BS + '   ← 本物の頂上',
 2217: '     |        ニセ頂上                /    ' + BS,
 2218: '  中 |         /' + BS + '         谷         /      ' + BS,
 2220: '  低 |____/                                  ' + BS,
 2221: '     +----------------------------------------→ 設計の選び方',
 2222: '          ↑ニセ頂上で素朴な山登りは停止 (谷を下れない)',
}
new = {
 2215: 'Quality↑                                /' + BS,
 2216: '     |                                 /  ' + BS + '   ← the true peak',
 2217: '     |        false pk                /    ' + BS,
 2218: '  Md |         /' + BS + '         vy         /      ' + BS,
 2220: '  Lo |____/                                  ' + BS,
 2221: '     +----------------------------------------→ how you pick the design',
 2222: '          ↑ naive hill-climbing gets stuck at the false peak (it cannot descend valleys)',
}
for n in orig:
    o=orig[n]; x=new[n]
    oi=o.find('/'); xi=x.find('/')
    oc = w(o[:oi]) if oi>=0 else None
    xc = w(x[:xi]) if xi>=0 else None
    print(n, 'first/ col orig=%s new=%s'%(oc,xc), 'MATCH' if oc==xc else 'DIFF')
    if oi>=0 and xi>=0:
        oi2=o.find('/',oi+1); xi2=x.find('/',xi+1)
        if oi2>=0:
            print('     second/ col orig=%d new=%d'%(w(o[:oi2]),w(x[:xi2])), 'MATCH' if w(o[:oi2])==w(x[:xi2]) else 'DIFF')
