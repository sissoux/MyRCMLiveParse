from machine import SPI, Pin
from time import sleep
import re

spi = SPI(0, mosi=Pin(7), sck=Pin(6) , baudrate=400000)           # Create SPI peripheral 0 at frequency of 400kHz.
                                        # Depending on the use case, extra parameters may be required
                                        # to select the bus characteristics and/or pins to use.

def validateString(string, target_length):
    # regex = r"\d{2}[-.']\d{2}[-.']\d{2}[-.']\d{2}"
    regex = r"[0-9]"
    return bool(re.match(regex, string)) and len(string) == target_length


print("start")



class LED:
    def __init__(self,R:int,G:int,B:int,id=0):
        self.r = R
        self.g = G
        self.b = B

class Strip:
    def __init__(self, size:int, interface:SPI, default=LED(0,0,0)):
        self.LEDs = [LED(default.r, default.g, default.b, x) for x in range(size)]
        self.size = size
        self.brightness = 0x01
    
    def update(self):
        buffer = [0,0,0,0] #Start frame
        for val in range(0,self.size):
            buffer.append(0xe0+0x08)
            buffer.append(self.LEDs[val].b)#B
            buffer.append(self.LEDs[val].g)#B
            buffer.append(self.LEDs[val].r)#B
        buffer.append(0xff) #Let enough clock pulses to reach end of strip
        spi.write(bytearray(buffer))
        
    def write(self, id, R,G,B):
        self.LEDs[id].r = R
        self.LEDs[id].g = G
        self.LEDs[id].b = B
    
    def setLED(self, id, Led):
        self.LEDs[id].r = Led.r
        self.LEDs[id].g = Led.g
        self.LEDs[id].b = Led.b

toPrint = "1"
charLen = 1
ledPerSegment = 2
NOfLEDs = ledPerSegment*7*charLen
strip = Strip(NOfLEDs,spi)
stripStateBuffer = list(range(NOfLEDs))
char = [0x3f, 0x03, 0x5b, 0x73, 0x65, 0x76, 0x7e, 0x63, 0x7f, 0x77]

color = [LED(0,0,0), LED(0xff,0,0), LED(0, 0xff, 0)]

strip.update()

offset = 0

if validateString(toPrint, charLen):
    print("filling buffer.")
    for i,c in enumerate(toPrint):
        print(f"Char {i}:{c} ==> ", end="")
        if c =="'":
            stripStateBuffer[offset:offset+4] = [2,0,0,0]
            offset+=4
        elif c =="-":
            stripStateBuffer[offset:offset+4] = [0,2,2,0]
            offset+=4
        elif c ==".":
            stripStateBuffer[offset:offset+4] = [0,0,0,2]
            offset+=4
        else:
            for j,bit in enumerate(f"{char[int(c)]:07b}"):
                for led in range(ledPerSegment):
                    stripStateBuffer[offset+j*ledPerSegment+led] = int(bit)
                print(bit, end="")
            offset += 7*ledPerSegment
        print(f"  {offset}")
    print(stripStateBuffer)
    
    # print(f"length of buffer {len(stripStateBuffer)}, ")

    for i in range(NOfLEDs):
        # print(f"LED {i} color {color[stripStateBuffer[i]]}")
        strip.setLED(NOfLEDs-(i+1),color[stripStateBuffer[i]])


    strip.update()

# while True:
#     number = input("LED to turn red ?")
#     try:
#         strip.write(int(number),0xff,0,0)
#         strip.update()
#     except ValueError:
#         print("Enter an 8 Bit integer")
#     sleep(0.1)
