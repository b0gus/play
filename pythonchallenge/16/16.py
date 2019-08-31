# http://www.pythonchallenge.com/pc/return/mozart.html

from PIL import Image, ImageChops
import numpy as np

image = Image.open("mozart.gif")

for x in image.histogram():
    if x % image.height == 0 and x != 0:
        print(x) # 2400

print(image.histogram().index(2400)) # 195
tmp = image.copy()
tmp.frombytes(bytes([195] * (tmp.height * tmp.width)))
tmp.show()

shifted = [bytes(np.roll(row, -row.tolist().index(195)).tolist()) for row in np.array(image)]
Image.frombytes(image.mode, image.size, b"".join(shifted)).show()

# http://www.pythonchallenge.com/pc/return/romance.html