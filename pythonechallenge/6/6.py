# http://www.pythonchallenge.com/pc/def/channel.html

import zipfile

f = "channel.zip"
z = zipfile.ZipFile(f)

n = "90052" # start from 90052
ans = ""

while(True):
    try:
        print(n)
        tmp = n + ".txt"
        ans += str(z.getinfo(tmp).comment.decode("ascii")) #Collect the comments.
        tmp = z.read(tmp).decode("ascii")
        n = tmp.replace("Next nothing is ", "")
    except:
        z.close
        break

print(ans)

# http://www.pythonchallenge.com/pc/def/oxygen.html