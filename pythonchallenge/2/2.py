# http://www.pythonchallenge.com/pc/def/ocr.html

import re

f = open("2.txt", "r")
q = f.read()
f.close()

ans = re.findall("[a-zA-Z]", q)
print("".join(ans))

# http://www.pythonchallenge.com/pc/def/equality.html