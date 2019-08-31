# http://www.wechall.net/challenge/training/crypto/simplesub1/index.php

q = "OY ZVJ LNEBAVZY ARQ YRU DLM SJLQ ZVBK EY HSBJMQ B LE BEISJKKJQ PJSY FJNN QRMJ YRUS KRNUZBRM CJY BK VJKJNIOMVNAI ZVBK NBZZNJ DVLNNJMAJ FLK MRZ ZRR VLSQ FLK BZ"

az = list(map(chr, range(65, 91)))

tmp = [[0 for col in range(1)] for row in range(26)]

for i in q:
    if i in az:
        tmp[ord(i)-65][0] += 1

print(tmp)

ans = q.replace("A", "g")
ans = ans.replace("C", "k")
ans = ans.replace("D", "c")
ans = ans.replace("F", "w")
ans = ans.replace("H", "f")
ans = ans.replace("I", "p")
ans = ans.replace("L", "a")
ans = ans.replace("P", "v")
ans = ans.replace("Q", "d")
ans = ans.replace("S", "r")
ans = ans.replace("E", "m")
ans = ans.replace("U", "u")
ans = ans.replace("Y", "y")
ans = ans.replace("Z", "t")
ans = ans.replace("J", "e")
ans = ans.replace("K", "s")
ans = ans.replace("V", "h")
ans = ans.replace("B", "i")
ans = ans.replace("O", "b")
ans = ans.replace("R", "o")
ans = ans.replace("N", "l")
ans = ans.replace("M", "n")

print(ans)

# heselpbnhlgp