from machine import Pin
from time import sleep
import re
from neopixel import NeoPixel
from color import *
from time import sleep


def validateString(string, target_length):
    # regex = r"\d\d[-.']\d\d[-.']\d\d[-.']\d\d"
    regex = r"\d\d[-.']"
    return bool(re.match(regex, string)) and len(string) == target_length


print("start")

toPrint = "02-"

ledPerSegment = 2
NumberOfDigits = 2
NumberOfFiller = 1
FillerLength = 2+ledPerSegment
Digitlength = 7*ledPerSegment


NumberOfLEDs = NumberOfDigits*Digitlength+NumberOfFiller*FillerLength

print(f"{NumberOfDigits=},{NumberOfFiller=},{NumberOfLEDs=}")

ws2812_pin = Pin(0, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
strip = NeoPixel(ws2812_pin, NumberOfLEDs)   # create NeoPixel driver

# char = [0x3f, 0x03, 0x5b, 0x73, 0x65, 0x76, 0x7e, 0x63, 0x7f, 0x77]♣
char = [0x7e, 0x18, 0x6d, 0x3d, 0x1b, 0x37, 0x77, 0x1c, 0x7f, 0x3f]


strip.fill(colors_d[colors.Black])

strip.write()

stripStateBuffer = [colors.Black for x in range(NumberOfLEDs)] # Init bufferList, needed to 

signColor = colors.Black
digitColor = colors.Red

for val in range(99):
    offset = 0
    toPrint = f"{val:02d}-"
    print(toPrint)
    if validateString(toPrint, NumberOfDigits+NumberOfFiller):
        print("filling buffer.")

        for i,c in enumerate(toPrint):
            print(f"Char {i}:{c} ==> ")
            if c =="'":
                stripStateBuffer[offset:offset+FillerLength] = [signColor,colors.Black,colors.Black,colors.Black]
                offset+=FillerLength
            elif c =="-":
                stripStateBuffer[offset:offset+FillerLength] = [colors.Black,signColor,signColor,colors.Black]
                offset+=FillerLength
            elif c ==".":
                stripStateBuffer[offset:offset+FillerLength] = [colors.Black,colors.Black,colors.Black,signColor]
                offset+=FillerLength
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

        for i in range(NumberOfLEDs):
            # print(f"LED {i} color {color[stripStateBuffer[i]]}")
            strip[i] = colors_d[stripStateBuffer[i]]

        strip.write()
    else:
        raise ValueError("String not compatible with display length")
    sleep(0.25)

