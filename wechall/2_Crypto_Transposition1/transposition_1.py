# http://www.wechall.net/challenge/training/crypto/transposition1/index.php

q = "oWdnreuf.lY uoc nar ae dht eemssga eaw yebttrew eh nht eelttre sra enic roertco drre . Ihtni koy uowlu dilekt  oes eoyrup sawsro don:wg sbahnoiied.r"
ans = ""
print(len(q)) # 148
idx = 0
while(idx < len(q)):
    ans += q[idx+1]
    ans += q[idx]
    idx += 2

print(ans)

# gbshaoniider