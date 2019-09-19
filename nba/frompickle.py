import pickle

with open("regular.pickle", "rb") as f:
    data = pickle.load(f)

tmp = data[0]["rowSet"]
info = "============ Start of Season ============\n"

for i in tmp:
    if i[7] == "W":
        info += i[5]
        info += " | "
        info += "winner: {} | ".format(i[6].split()[0])
        info += "loser: {}\n".format(i[6].split()[-1])

info += "============ End of Regular Season ============\n"

f = open("please.txt", "w")
f.write(info)
f.close()

# 5:date, 6: winner and loser, 7: W

with open("playoff.pickle", "rb") as f:
    data = pickle.load(f)

tmp = data[0]["rowSet"]
info = ""

for i in tmp:
    if i[7] == "W":
        info += i[5]
        info += " | "
        info += "winner: {} | ".format(i[6].split()[0])
        info += "loser: {}\n".format(i[6].split()[-1])

info += "============ End of Playoffs ============\n"

f = open("please.txt", "a")
f.write(info)
f.close()