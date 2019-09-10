# http://www.pythonchallenge.com/pc/hex/bin.html

import base64
import soundfile

f = open("19.txt", "rb")
q = f.read()
f.close()

f = open("indian.wav", "wb")
f.write(base64.b64decode(q[:len(q)-1]))
f.close()

indian = soundfile.SoundFile("indian.wav")

soundfile.write("endian.wav", indian.read(), indian.samplerate, indian.subtype, "BIG", indian.format)

# http://www.pythonchallenge.com/pc/hex/idiot2.html