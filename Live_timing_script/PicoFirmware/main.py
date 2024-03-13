from machine import Pin, SPI
from time import sleep
import re
from neopixel import NeoPixel
from color import *
from time import sleep
#import pio_spi
#SPI Daisy chain is not wired properly yet. To be tested later.

def refreshStrip(buffer, strip:NeoPixel):
    # Convert colorbuffer to strip bytearray and update strip
    for i in range(len(buffer)):
        strip[i] = colors_d[stripStateBuffer[i]]
    strip.write()

def flushStrip(strip:NeoPixel):
    strip.fill(colors_d[colors.Black])
    strip.write()


def validateString(string, target_length):
    regex = r"\d\d[-.']\d\d[-.']\d\d[-.']\d\d"
    #regex = r"\d\d[-.']"
    return True#bool(re.match(regex, string)) and len(string) == target_length



print("start")

toPrint = "00-00'00-00"

ledPerSegment = 2
NumberOfDigits = 8
NumberOfFiller = 3
FillerLength = 2+ledPerSegment
Digitlength = 7*ledPerSegment


NumberOfLEDs = NumberOfDigits*Digitlength+NumberOfFiller*FillerLength

print(f"{NumberOfDigits=},{NumberOfFiller=},{NumberOfLEDs=}")

ws2812_pin_2 = Pin(0, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
ws2812_pin_1 = Pin(11, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
ws2812_pin_0 = Pin(13, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
strip_0 = NeoPixel(ws2812_pin_0, NumberOfLEDs)   # create NeoPixel driver
strip_1 = NeoPixel(ws2812_pin_1, NumberOfLEDs)   # create NeoPixel driver
strip_2 = NeoPixel(ws2812_pin_2, NumberOfLEDs)   # create NeoPixel driver

# char = [0x3f, 0x03, 0x5b, 0x73, 0x65, 0x76, 0x7e, 0x63, 0x7f, 0x77]♣
char = [0x7e, 0x18, 0x6d, 0x3d, 0x1b, 0x37, 0x77, 0x1c, 0x7f, 0x3f]


flushStrip(strip_0)
flushStrip(strip_1)
flushStrip(strip_2)

stripStateBuffer = [colors.Black for x in range(NumberOfLEDs)] # Init bufferList, needed to 

signColor = colors.Green
digitColor = colors.Red


def Display(toPrint, strip:NeoPixel):
    offset = 0
    print(toPrint)
    if validateString(toPrint, NumberOfDigits+NumberOfFiller):
        print("filling buffer.")

        for i,c in enumerate(toPrint):
            print(f"Char {i}:{c} ==> ")
            if c ==".":
                stripStateBuffer[offset:offset+FillerLength] = [signColor,colors.Black,colors.Black,colors.Black]
                offset+=FillerLength
            elif c =="-":
                stripStateBuffer[offset:offset+FillerLength] = [colors.Black,signColor,signColor,colors.Black]
                offset+=FillerLength
            elif c =="'":
                stripStateBuffer[offset:offset+FillerLength] = [colors.Black,colors.Black,colors.Black,signColor]
                offset+=FillerLength
            elif c=="_":
                stripStateBuffer[offset:offset+Digitlength] = [colors.Black for x in range(Digitlength)]
                offset += Digitlength
            else:
                for j,bit in enumerate(f"{char[int(c)]:07b}"):
                    print(int(bit))
                    for led in range(ledPerSegment):
                        if bit == '1':
                            stripStateBuffer[offset+j*ledPerSegment+led] = digitColor
                        else:
                            stripStateBuffer[offset+j*ledPerSegment+led] = colors.Black
                offset += Digitlength
            # print(f"  {offset}")
        print(stripStateBuffer)
        
        # print(f"length of buffer {len(stripStateBuffer)}, ")

        refreshStrip(stripStateBuffer, strip)
    else:
        raise ValueError("String not compatible with display length")
    

car = 5
time =21.85
lap = 1

Display(f"{car:02d}-{time:02.02f}-{lap:02d}", strip_0)
Display(f"81-19.65-10", strip_1)
Display(f"01-19.65-09", strip_2)

while True:
    sleep(0.25)
    ans = input("Waiting")
    try:
        Display(ans,strip_0)
    except ValueError as e:
        print(e)



