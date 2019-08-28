# http://www.pythonchallenge.com/pc/return/5808.html

from PIL import Image

img = Image.open("cave.jpg")

print("x = {}, y = {}".format(img.width, img.height))

odd = Image.new('RGB', (640, 480))
even = Image.new('RGB', (640, 480))

for x in range(640):
    for y in range(480):
        if (x+y)%2 == 0:
            even.putpixel((x,y), img.getpixel((x,y)))
        else:
            odd.putpixel((x,y), img.getpixel((x,y)))

img.close()
odd.show()
even.show()

# http://www.pythonchallenge.com/pc/return/evil.html