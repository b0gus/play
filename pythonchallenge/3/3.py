# http://www.pythonchallenge.com/pc/def/equality.html

import re

f = open("3.txt", "r")
q = f.read()

tmp = re.findall("[a-z][A-Z]{3}[a-z][A-Z]{3}[a-z]", q) # One small letter, surrounded by EXACTLY three big bodyguards on each of its sides.
ans = ""

for i in tmp:
    ans += i[4]

print(ans)

# http://www.pythonchallenge.com/pc/def/linkedlist.php