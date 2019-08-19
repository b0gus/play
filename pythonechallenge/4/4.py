# http://www.pythonchallenge.com/pc/def/linkedlist.php

import requests

# tmp = 12345
tmp = 8022 # In 16044, "Yes. Divide by two and keep going."

for i in range(400): # 400 times is more than enough.
    try:
        url = "http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=" + str(tmp)
        data = requests.get(url).text
        print(data)
        tmp = int(data.split()[-1])
    except:
        print(i)
        break

# http://www.pythonchallenge.com/pc/def/peak.html