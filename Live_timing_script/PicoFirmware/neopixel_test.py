from machine import Pin
from neopixel import NeoPixel
import time 

numLED = 32

pin = Pin(0, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
np = NeoPixel(pin, numLED)   # create NeoPixel driver on GPIO0 for 8 pixels
np[0] = (255, 0, 0) # set the first pixel to white
np.write()              # write data to all pixels
r, g, b = np[0]         # get first pixel colour

while True:

    for i in range(numLED):

        print(f"Writing LED {i} to red, {i-1} to black")
        # if i>0:
        #     np[i-1] = (0,0,0)
        # else:
        #     np[numLED-1] = (0,0,0)

        np[i] = (255,0,0)

        np.write()
        time.sleep(0.025)
    for i in range(numLED):

        print(f"Writing LED {i} to red, {i-1} to black")
        # if i>0:
        #     np[i-1] = (0,0,0)
        # else:
        #     np[numLED-1] = (0,0,0)

        np[i] = (0,255,0)

        np.write()
        time.sleep(0.025)
    for i in range(numLED):

        print(f"Writing LED {i} to red, {i-1} to black")
        # if i>0:
        #     np[i-1] = (0,0,0)
        # else:
        #     np[numLED-1] = (0,0,0)

        np[i] = (255,255,255)

        np.write()
        time.sleep(0.025)
    time.sleep(2)