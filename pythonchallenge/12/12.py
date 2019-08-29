# http://www.pythonchallenge.com/pc/return/evil.html

from PIL import Image
import io

f = open("evil2.gfx", "rb") # not jpg, gfx
content = f.read()
f.close()

for i in range(5):
    data = content[i::5]
    img = Image.open(io.BytesIO(data))
    f = open(("%d.%s" %(i, img.format)), "wb")
    f.write(data)
    f.close()

# http://www.pythonchallenge.com/pc/return/disproportional.html