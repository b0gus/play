# http://www.wechall.net/challenge/training/crypto/simplesub2/index.php

import operator

q = """3D 66 F4 76 FA F9 31 B7 FD F9 31 AD 66 F4 96 81
D4 73 38 AD 96 D4 66 F4 43 D4 EB F9 96 D4 38 F9
FA C5 43 FA 83 D4 34 B7 31 D4 C9 66 B7 D4 76 66
31 D4 AD 31 81 D4 F6 43 FA C9 D4 EB 43 FD FD D4
C5 66 F4 43 D4 ED 43 FD FD 66 EB D4 38 F9 4E 32
43 FA 81 D4 73 38 43 D4 39 FA 66 34 FD 43 3A D4
EB AD 31 38 D4 31 38 AD 96 D4 4E AD 39 38 43 FA
D4 AD 96 D4 31 38 F9 31 D4 31 38 43 D4 32 43 C9
D4 AD 96 D4 39 FA 43 31 31 C9 D4 FD 66 F4 76 81
D4 CC D4 EB AD FD FD D4 4E 66 3A 43 D4 B7 39 D4
EB AD 31 38 D4 F9 D4 34 43 31 31 43 FA D4 43 F4
4E FA C9 39 31 AD 66 F4 D4 96 38 43 3A 43 D4 F9
F4 C9 D4 96 66 66 F4 81 D4 5A 66 B7 FA D4 96 66
FD B7 31 AD 66 F4 D4 AD 96 62 D4 AD 39 34 96 4E
AD 96 39 FA F4 F9 38 81"""

q = q.replace("81", ".")
q = q.replace("D4", "/")
q = q.replace("3D", "c")
q = q.replace("66", "o")
q = q.replace("F4", "n")
q = q.replace("76", "g")
q = q.replace("FA", "r")
q = q.replace("F9", "a")
q = q.replace("31", "t")
q = q.replace("B7", "u")
q = q.replace("FD", "l")
q = q.replace("AD", "i")
q = q.replace("96", "s")
q = q.replace("73", "t")
q = q.replace("38", "h")
q = q.replace("EB", "w")
q = q.replace("34", "b")
q = q.replace("C9", "y")
q = q.replace("43", "e")
q = q.replace("39", "p")
q = q.replace("3A", "m")
q = q.replace("F6", "v")
q = q.replace("C5", "d")
q = q.replace("4E", "c")
q = q.replace("32", "k")
q = q.replace("CC", "i")
q = q.replace("5A", "y")
q = q.replace("ED", "f")
q = q.replace("62", ":")

l = q.split()

tmp = {}

for i in l:
    if i in tmp.keys():
        tmp[i] += 1
    else:
        tmp.setdefault(i, 1)

print(sorted(tmp.items(), key=operator.itemgetter(1), reverse=True))

print(" ".join(l))

# ipbscisprnah