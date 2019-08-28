# http://www.pythonchallenge.com/pc/def/oxygen.html

from PIL import Image

img = Image.open("oxygen.png")

x = img.width
y = img.height // 2
px = img.load()

img.close()

res = ""

for i in range(0, x, 7):
    if px[i, y][0] == px[i, y][1] == px[i, y][2]:
        res += chr(px[i, y][0])

print(res) # smart guy, you made it. the next level is [105, 110, 116, 101, 103, 114, 105, 116, 121]

ans = [105, 110, 116, 101, 103, 114, 105, 116, 121]

for i in ans:
    print(chr(i), end="")

# http://www.pythonchallenge.com/pc/def/integrity.html