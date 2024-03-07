import re
import serial

class DisplayLine:
    def __init__(self, id:int, size=11, pattern="\d{2}[-.']\d{2}[-.']\d{2}[-.']\d{2}") -> None:
        self.pattern = re.compile(pattern)
        self.displaySize = size
        self._value = self.checkFormat("00-00.00-00")

    def checkFormat(self, string):
        if (self.pattern.match(string) is not None) and (len(string) == self.displaySize):
            return string
        raise ValueError('Value is not compatible with display format')
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, string):
        self._value = self.checkFormat(string)

class color:
    def __init__(self, r, g, b) -> None:
        self.r = r
        self.g = g
        self.b = b

class Display:
    def __init__(self, numberOfLines:int, Port=None, TextColor=color(1,0,0)) -> None:
        self.numberOfLines = numberOfLines
        self.Port = Port
        try:
            self.serial = serial.Serial(self.Port, 115200)
        except FileNotFoundError:
            print("Cannot open serial connection")
            self.serial = None
        
        self.TextColor = TextColor
        self.content = [DisplayLine(lineID) for lineID in range(numberOfLines)]
    
    def setLines(self, stringList:list):
        for i in range(self.numberOfLines):
            self.content[i].value = stringList[i]

    def updateDisplay(self):
        if self.serial is not None:
            data = ''
            for i,line in enumerate(self.content):
                data += f"\t{i}:{line.value}"
            data = bytearray(data+'\n', encoding='ascii')
        else:
            raise ConnectionError("Display is not connected.")
        print(f"sending ==> {data}")
        
        #Send content data for each line to display.
