from PIL import Image, ImageDraw, ImageFont, ImageColor
from pathlib import Path
from PilotClasses import Round, Pilot

Montserrat_Black_file = Path("./Fonts/Montserrat","Montserrat-Black.ttf")
Franchise_bold_file = Path("./Fonts","Franchise-Bold.ttf")


class TextStyle():
    def __init__(self, font, color=ImageColor.getrgb("black"), size=20) -> None:
        self.color = color
        self.size = size
        try:
            self.font = ImageFont.truetype(font, self.size)  
        except IOError:
            print(f"{font} font not found.")
            self.font=None 

NameStyle = TextStyle(font=Montserrat_Black_file, color=ImageColor.getrgb("white"), size=20)
LastNameStyle = TextStyle(font=Montserrat_Black_file, color=ImageColor.getrgb("#60c5c7"), size=15)
CategoryStyle = TextStyle(font=Montserrat_Black_file, color=ImageColor.getrgb("white"), size=75)
SerieStyle = TextStyle(font=Montserrat_Black_file, color=ImageColor.getrgb("#1a3459"), size=50)
PositionStyle = TextStyle(font=Franchise_bold_file, color=ImageColor.getrgb("white"), size=65)


ResultRankingCoordinates = {
    "Buggy" : [(282,466),
               (325,636),
               (544,466),
               (587,636),
               (806,466),
               (849,636),
               (1068,466),
               (1111,636),
               (1330,466),
               (1373,636),
               (1592,466),
               (1635,636)
                ]
}

def generateResultRankingCoordinates():
    coeffs_x={
        "buggy": [(262, 282), (262, 325)],
        "Name": [(262, 335), (262, 380)],
        "LastName": [(262, 335), (262, 380)],
        "Position": [(262, 295), (262, 337)]
        }
    
    coeffs_y={
        "buggy": [(0, 466), (0, 636)],
        "Name": [(0, 570), (0, 742)],
        "LastName": [(0, 595), (0, 767)],
        "Position": [(0, 485), (0, 655)]
        }
    
    resultDict = dict()
    for key in coeffs_x:
        resultList = list()
        for i in range(0,12):
            ax, bx = coeffs_x[key][i%2]
            ay, by = coeffs_y[key][i%2]
            resultList.append((ax*int(i/2)+bx, ay*int(i/2)+by))
        resultDict[key] = resultList
    return resultDict

coordinatesDict = generateResultRankingCoordinates()

def generateMainRankingImage(RankingList:Round, backgroundImagePath:Path, buggyImagePath:Path, resize_dimensions=(1920, 1080), buggySize=(230,130)):
    backgroundImg = Image.open(backgroundImagePath)
    backgroundImg = backgroundImg.resize(resize_dimensions, Image.LANCZOS)

    buggyImg = Image.open(buggyImagePath)
    buggyImg =  buggyImg.resize(buggySize, Image.LANCZOS)

    drawImg = ImageDraw.Draw(backgroundImg)

    drawImg.text((90,127), RankingList.category_pretty, font=CategoryStyle.font, fill=CategoryStyle.color)
    drawImg.text((90,213), RankingList.serie_pretty, font=SerieStyle.font, fill=SerieStyle.color)

    for index, pilot in enumerate(RankingList.pilotList):
        try:
            backgroundImg.paste(buggyImg, coordinatesDict["buggy"][index], buggyImg)
        except IndexError:
            print(f"Error adding buggy image for pilot {index}")

        drawImg.text(coordinatesDict["Position"][index], f"{index+1}", font=PositionStyle.font, fill=PositionStyle.color, anchor="rt")
        
        try:
            pilotName = pilot.pilot.split(" ")
            drawImg.text(coordinatesDict["Name"][index], pilotName[0][:12].upper(), font=NameStyle.font, fill=NameStyle.color)
            drawImg.text(coordinatesDict["LastName"][index], pilotName[1][:18], font=LastNameStyle.font, fill=LastNameStyle.color)
        except Exception as e:
            print(e)
        
    backgroundImg.save("output.png")
