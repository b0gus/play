# http://www.pythonchallenge.com/pc/return/bull.html

import re

q = "1"

for i in range(30):
    q = "".join([str(len(x+y))+x for x, y in re.findall(r"(\d)(\1*)", q)]) # ([0-9])(\\1*)

print(len(q)) # 5808

# http://www.pythonchallenge.com/pc/return/5808.html