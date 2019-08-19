# http://www.wechall.net/challenge/training/prime_factory/index.php

ans = []

def find_prime(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

for i in range(1000001, 2000000, 2):
    if find_prime(i) == True:
        tmp = 0
        for j in str(i):
            tmp += int(j)
        if find_prime(tmp) == True:
            ans.append(i)
    if(len(ans) == 2):
        break

print(ans)

# 10000331000037