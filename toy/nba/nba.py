from nba_api.stats.endpoints import leaguegamelog
import pickle
import time

for i in range(46, 99):
    year = i
    season = "19{}-{}".format(year, year+1)

    logs = leaguegamelog.LeagueGameLog(season=season) #season="ALLTIME"
    datadict = logs.get_dict()
    with open("regular.pickle", "wb") as f:
        pickle.dump(datadict["resultSets"], f, pickle.HIGHEST_PROTOCOL)

    logs = leaguegamelog.LeagueGameLog(season=season, season_type_all_star="Playoffs")
    datadict = logs.get_dict()
    with open("playoff.pickle", "wb") as f:
        pickle.dump(datadict["resultSets"], f, pickle.HIGHEST_PROTOCOL)

    with open("regular.pickle", "rb") as f:
        data = pickle.load(f)

    tmp = data[0]["rowSet"]
    info = "============ Start of Season ============\n"

    for i in tmp:
        if i[7] == "W":
            info += i[5]
            info += " | "
            info += "w: {} | ".format(i[6].split()[0])
            info += "L: {}\n".format(i[6].split()[-1])

    info += "============ End of Regular Season ============\n"

    f = open("{}.txt".format(season), "w")
    f.write(info)
    f.close()

    with open("playoff.pickle", "rb") as f:
        data = pickle.load(f)

    tmp = data[0]["rowSet"]
    info = ""

    for i in tmp:
        if i[7] == "W":
            info += i[5]
            info += " | "
            info += "w: {} | ".format(i[6].split()[0])
            info += "L: {}\n".format(i[6].split()[-1])

    info += "============ End of Playoffs ============\n"

    f = open("{}.txt".format(season), "a")
    f.write(info)
    f.close()

    time.sleep(0.1)
