# http://www.pythonchallenge.com/pc/return/brightness.html

import gzip, difflib

q = gzip.open("deltas.gz")

left = []
right = []

for line in q:
    left.append(line[:53].decode()+"\n")
    right.append(line[56:].decode()) # line[53:56] : blank

q.close()

diff = difflib.Differ().compare(left, right)

f1 = open("f_+.png", "wb")
f2 = open("f_-.png", "wb")
f3 = open("f_x.png", "wb")

for line in diff:
    tmp = bytes([int(i, 16) for i in line[2:].split() if i])
    if line[0] == "+": # only in left
        f1.write(tmp) # butter
    elif line[0] == "-": # only in right
        f2.write(tmp) # fly
    else: # in both
        f3.write(tmp) # ../hex/bin.html

f1.close()
f2.close() 
f3.close()

# http://www.pythonchallenge.com/pc/hex/bin.html