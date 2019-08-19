# http://www.pythonchallenge.com/pc/def/peak.html

import pickle # pronounce pick hell

f = open("banner.p", "rb")
peak = pickle.load(f)
f.close()

# print(peak) # tuples in lists in a list

for tup in peak:
    res = ""
    for char, num in tup:
        res += char*num
    print(res)

# http://www.pythonchallenge.com/pc/def/channel.html