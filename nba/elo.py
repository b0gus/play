import json
import operator
from pprint import pprint as pp

f = open("2018-19.txt") # 1415~ nop
data = f.readlines()
tmp = json.loads("08-19.json")
# tmp = {}

for i in data:
    if i[0] == "2":
        tmp.setdefault(i.split()[3], 1500)

def cal_elo(w, l):
    K = 16
    Ew = 1 / (1 + 10**((l-w)/400))
    El = 1 / (1 + 10**((w-l)/400))
#     print(Ew, El)
    w = w + K*(1-Ew)
    l = l + K*(0-El)
    return w, l

for i in data:
    if len(i) == 29:
        w = i.split()[3]
        l = i.split()[6]
        w_elo, l_elo = cal_elo(tmp[w], tmp[l])
        tmp[w] = w_elo
        tmp[l] = l_elo

nba = sorted(tmp.items(), key=operator.itemgetter(1), reverse=True)

pp(nba)

with open('08-19.json', 'a') as f:
    json.dump(tmp, f)