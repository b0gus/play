# http://www.pythonchallenge.com/pc/return/romance.html

import requests
from urllib.parse import unquote_to_bytes
import bz2
import xmlrpc.client

next_nothing = '12345' # you+should+have+followed+busynothing...
data = []
i = 0

# while True:
#     try:
#         url = "http://www.pythonchallenge.com/pc/def/linkedlist.php?busynothing=__bn__"
#         url = url.replace("__bn__", next_nothing)
#         response = requests.get(url)
#         next_nothing = response.text.split()[-1]
#         info = response.cookies['info']
#         print("{} - next_nothing: {}, info: {}".format(i, next_nothing, info))
#         data.append(info)
#         i += 1
#     except:
#         print("".join(data))
#         break

data = "BZh91AY%26SY%94%3A%E2I%00%00%21%19%80P%81%11%00%AFg%9E%A0+%00hE%3DM%B5%23%D0%D4%D1%E2%8D%06%A9%FA%26S%D4%D3%21%A1%EAi7h%9B%9A%2B%BF%60%22%C5WX%E1%ADL%80%E8V%3C%C6%A8%DBH%2632%18%A8x%01%08%21%8DS%0B%C8%AF%96KO%CA2%B0%F1%BD%1Du%A0%86%05%92s%B0%92%C4Bc%F1w%24S%85%09%09C%AE%24%90"
data = unquote_to_bytes(data.replace("+", " "))

print(bz2.decompress(data).decode()) # is it the 26th already? call his father and inform him that "the flowers are on their way". he'll understand.

url = "http://www.pythonchallenge.com/pc/phonebook.php"
conn = xmlrpc.client.ServerProxy(url)
print(conn.phone("Leopold")) # 555-VIOLIN

url = "http://www.pythonchallenge.com/pc/stuff/violin.php"
message = {"info":"the flowers are on their way"}

response = requests.get(url, cookies=message)
print(response.text)

# http://www.pythonchallenge.com/pc/return/balloons.html