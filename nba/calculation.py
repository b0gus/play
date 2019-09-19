import sqlite3
import operator
from pprint import pprint as pp

def cal_elo(w, l):
    K = 16
    Ew = 1 / (1 + 10**((l-w)/400))
    El = 1 / (1 + 10**((w-l)/400))
    w = w + K*(1-Ew)
    l = l + K*(0-El)
    return w, l

conn = sqlite3.connect("nba.db")

c = conn.cursor()
start = '1946-10-01' # 10~
end = '2019-07-01' # ~7

tmp = {}

res = c.execute("select * from game where date between '{}' and '{}';".format(start, end))
for i in res:
    i = list(i)
    tmp.setdefault(i[1], 1500)

res = c.execute("select * from game where date between '{}' and '{}';".format(start, end))
for i in res:
    i = list(i)
    w, l = i[1], i[2]
    w_elo, l_elo = cal_elo(tmp[w], tmp[l])
    tmp[w] = w_elo
    tmp[l] = l_elo

nba = sorted(tmp.items(), key=operator.itemgetter(1), reverse=True)

pp(nba)