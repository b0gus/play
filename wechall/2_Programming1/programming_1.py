# http://www.wechall.net/challenge/training/programming1/index.php

import requests

url = "https://www.wechall.net/challenge/training/programming1/index.php?action=request"
dest = "https://www.wechall.net/challenge/training/programming1/index.php?answer="
hdr = {"Cookie" : "WC=your_cookie_here"}

response = requests.get(url, headers=hdr).text
dest += response
ans = requests.get(dest, headers=hdr).text

print(ans)
