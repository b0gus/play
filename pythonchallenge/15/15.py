# http://www.pythonchallenge.com/pc/return/uzi.html

from calendar import *

for year in range(1006, 2006, 10):
    if isleap(year) and weekday(year, 1, 26) == 0: # if leap year and 1/26 is monday
        print(year) # 1176, (1356), 1576, 1756, 1976, (he ain't the youngest, he is the second)
# todo: buy flowers for tomorrow - 1356/1/27

# http://www.pythonchallenge.com/pc/return/mozart.html