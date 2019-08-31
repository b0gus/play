# http://www.wechall.net/challenge/training/crypto/digraph/index.php

import operator

q = "tarignfldohfrmpptthfrmdhrignepyq qmripp zzoczbdozlztrmoczz rmnedhep eaocepephffloc epppzbzbocepeppeppttttzlyq bwhfep gnrirm rmriri zzdhpepedhzbppttrm ocdhrmneocdozu oahfep dhrmox bwocttttzu flririzz hwriptyq sugnrmocdo rmnedhep baoczloaridozz hfep eprittpprmdhrignmu oceadodohfzzdonettocgngnyq"

tmp = q.replace(" ", "  ")

a = []
count = {}
ans = ""

for i in range(0, len(tmp)-1, 2):
    d = tmp[i] + tmp[i+1]
    a.append(d)
    ans = ans + d + " " 

for i in a:
    try: count[i] += 1
    except: count[i] = 1

print(sorted(count.items(), key=operator.itemgetter(1), reverse=True))

for i in range(len(tmp)):

ans = ans.replace("hf", "A")
ans = ans.replace("pt", "B")
ans = ans.replace("ta", "C")
ans = ans.replace("zb", "C")
ans = ans.replace("zz", "D")
ans = ans.replace("oc", "E")
ans = ans.replace("su", "E")
ans = ans.replace("pe", "F")
ans = ans.replace("fl", "G")
ans = ans.replace("ne", "H")
ans = ans.replace("dh", "I")
ans = ans.replace("hw", "J")
ans = ans.replace("ba", "K")
ans = ans.replace("tt", "L")
ans = ans.replace("zl", "Y")
ans = ans.replace("ea", "M")
ans = ans.replace("gn", "N")
ans = ans.replace("ri", "O")
ans = ans.replace("zt", "P")
ans = ans.replace("do", "R")
ans = ans.replace("ep", "S")
ans = ans.replace("rm", "T")
ans = ans.replace("pp", "U")
ans = ans.replace("oa", "W")
ans = ans.replace("bw", "W")
ans = ans.replace("qm", "Y")
ans = ans.replace("yq", "!")
ans = ans.replace("mu", ":")
ans = ans.replace("ox", "?")
ans = ans.replace("zu", ",")

print(ans)

# emrradrhlenn