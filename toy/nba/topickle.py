from nba_api.stats.endpoints import leaguegamelog
import pickle

logs = leaguegamelog.LeagueGameLog(season="ALLTIME") #season="ALLTIME"
datadict = logs.get_dict()
with open("regular.pickle", "wb") as f:
    pickle.dump(datadict["resultSets"], f, pickle.HIGHEST_PROTOCOL)
f.close()

logs = leaguegamelog.LeagueGameLog(season_type_all_star="Playoffs")
datadict = logs.get_dict()
with open("playoff.pickle", "wb") as f:
    pickle.dump(datadict["resultSets"], f, pickle.HIGHEST_PROTOCOL)
f.close()

# 4738329
