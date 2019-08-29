# http://www.pythonchallenge.com/pc/return/italy.html

from PIL import Image

im = Image.open("wire.png") # 10000 * 1
new = Image.new(im.mode, [100, 100])

directions = [(1,0), (0,1), (-1,0), (0,-1)] # walk around

x, y, tmp = -1, 0, 0

double_size = 200
while double_size//2 > 0:
    for i in directions:
        size = double_size//2

        for s in range(size):
            x += i[0]
            y += i[1]
            new.putpixel((x,y), im.getpixel((tmp,0)))
            tmp += 1
        
        double_size -= 1

new.show()

# http://www.pythonchallenge.com/pc/return/uzi.html