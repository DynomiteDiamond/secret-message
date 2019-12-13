from PIL import Image
import sys
import re
import binascii

if len(sys.argv) < 2:
  raise Exception("Not enough arguments please try \"python3 secret.py help\"")

if sys.argv[1] == 'encode': #secret.py encode file message output
  if len(sys.argv) < 5:
    raise Exception("Not enough arguments")
  im = Image.open(sys.argv[2])
  message = sys.argv[3]
  bMessage = ''.join(format(ord(x), 'b') for x in message) + "0"
  if len(bMessage) > im.size[0]:
    raise Exception("String is too long to fit in image. Try a shorter one")
  for bit in range(len(bMessage)):
    pixel = im.getpixel((int(bit),0))
    red = pixel[0]
    green = pixel[1]
    blue = pixel[2] + 1
    if bMessage[bit] == "0":
      blue -= 1
    im.putpixel((int(bit),0),(red,green,blue))
    print('Encoding, '+str(bit*100/len(bMessage))+'% done')
  im.save(sys.argv[4])
elif sys.argv[1] == "decode": #secret.py decode file original
  file = Image.open(sys.argv[2])
  original = Image.open(sys.argv[3])
  binString = ''
  for pixel in range(file.size[0]):
    nPixel = file.getpixel((int(pixel),0))
    oPixel = original.getpixel((int(pixel),0))
    blue = nPixel[2]
    oBlue = oPixel[2]
    if (oBlue - (blue-1)) == 1:
      binString += "0"
    else:
      binString += "1"
  seperated = re.sub(r'([01]{7})',r'\1-',binString,len(binString)).split('-')
  output = ""
  for x in seperated:
    v = int("0"+x,2)
    b = bytearray()
    while v:
      b.append(v & 0xff)
      v >>= 8
    output += str(bytes(b[::-1]))[2:]
  print('Message is: '+re.sub(r'\'', '',output,999))
else:
  print('Usage: python3 secret.py encode INPUT TEXT OUTPUT\npython3 secret.py decode INPUT ORIGINAL')
