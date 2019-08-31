# http://www.wechall.net/challenge/training/crypto/caesar2/index.php

import time

q = "5C 04 04 79 20 7F 04 77 41 20 0E 04 0A 20 08 04 \
01 0B 7A 79 20 04 03 7A 20 02 04 07 7A 20 78 7D \
76 01 01 7A 03 7C 7A 20 7E 03 20 0E 04 0A 07 20 \
7F 04 0A 07 03 7A 0E 43 20 69 7D 7E 08 20 04 03 \
7A 20 0C 76 08 20 7B 76 7E 07 01 0E 20 7A 76 08 \
0E 20 09 04 20 78 07 76 78 00 43 20 6C 76 08 03 \
3C 09 20 7E 09 54 20 46 47 4D 20 00 7A 0E 08 20 \
7E 08 20 76 20 06 0A 7E 09 7A 20 08 02 76 01 01 \
20 00 7A 0E 08 05 76 78 7A 41 20 08 04 20 7E 09 \
20 08 7D 04 0A 01 79 03 3C 09 20 7D 76 0B 7A 20 \
09 76 00 7A 03 20 0E 04 0A 20 09 04 04 20 01 04 \
03 7C 20 09 04 20 79 7A 78 07 0E 05 09 20 09 7D \
7E 08 20 02 7A 08 08 76 7C 7A 43 20 6C 7A 01 01 \
20 79 04 03 7A 41 20 0E 04 0A 07 20 08 04 01 0A \
09 7E 04 03 20 7E 08 20 77 7B 78 76 7A 04 01 7E \
07 05 08 08 43"

q = q.split()

# for key in range(128):
#     ans = ""
#     for i in q:
#         i = (int(i, 16) + key) % 128
#         ans += chr(i)
#     print(key, " : ", ans)
#     time.sleep(1)

key = 107

for i in q:
    i = (int(i, 16) + key) % 128
    ans += chr(i)
print(key, " : ", ans)

# bfcaeolirpss