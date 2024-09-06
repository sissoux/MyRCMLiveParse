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

def generateMainRankingImage(RankingList:Round, backgroundImagePath:Path, buggyImagePath:Path, outputPath:Path, resize_dimensions=(1920, 1080), buggySize=(230,130)):
    backgroundImg = Image.open(backgroundImagePath)
    backgroundImg = backgroundImg.resize(resize_dimensions, Image.LANCZOS)

    buggyImg = Image.open(buggyImagePath)
    buggyImg =  buggyImg.resize(buggySize, Image.LANCZOS)

    drawImg = ImageDraw.Draw(backgroundImg)

    drawImg.text((90,127), RankingList.category_pretty, font=CategoryStyle.font, fill=CategoryStyle.color)
    drawImg.text((90,213), RankingList.serie_pretty, font=SerieStyle.font, fill=SerieStyle.color)

    for index, pilot in enumerate(RankingList.pilotList):
        if index>=len(coordinatesDict["buggy"]):
            break
        try:
            backgroundImg.paste(buggyImg, coordinatesDict["buggy"][index], buggyImg)
        except IndexError:
            print(f"Error adding buggy image for pilot {index}")

        drawImg.text(coordinatesDict["Position"][index], f"{index+1}", font=PositionStyle.font, fill=PositionStyle.color, anchor="rt")
        
        try:
            pilotName = pilot.pilot.split(" ")
            drawImg.text(coordinatesDict["Name"][index], pilotName[0][:12].upper(), font=NameStyle.font, fill=NameStyle.color)
            if len(pilotName)>1:
                drawImg.text(coordinatesDict["LastName"][index], pilotName[1][:18], font=LastNameStyle.font, fill=LastNameStyle.color)
        except Exception as e:
            print(e)
        
    backgroundImg.save(outputPath)

StartGridCoordinates=[
    (50,800),#1
    (150,650),#2
    (325,500),#3
    (550,300),#4
    (775,375),#5
    (950,475),#6
    (1250,600),#7
    (1425,500),#8
    (1525,425),#9
    (1625,350),#10
    (1750,375),#11
    (1700,150)#12
 ]


def generateStartGridImage(RankingList, outputPath, resize_dimensions=(1920, 1080)):
    backgroundImg = Image.new('RGBA', resize_dimensions, (255, 255, 255, 0))
    drawImg = ImageDraw.Draw(backgroundImg)

    # # Draw category and series text
    # drawImg.text((90,127), RankingList.category_pretty, font=CategoryStyle.font, fill=CategoryStyle.color)
    # drawImg.text((90,213), RankingList.serie_pretty, font=SerieStyle.font, fill=SerieStyle.color)

    margin = 10

    for index, pilot in enumerate(RankingList.pilotList):
        x, y = StartGridCoordinates[index]
        try:
            full_name = pilot.pilot.strip()  # Strips any leading/trailing whitespace
            FirstName, LastName = full_name.split(maxsplit=1) if " " in full_name else (full_name, "")
            FirstName = f"{index+1} {FirstName[:12].upper()}"
            LastName = f"    {LastName[:18]}" if LastName != "" else ""

            # Get the bounding box for the first and second lines of text
            first_line_bbox = drawImg.textbbox((x, y), FirstName, font=NameStyle.font)
            second_line_bbox = drawImg.textbbox((x, y), LastName, font=LastNameStyle.font)

            # Calculate the width and height of the enclosing rectangle
            rect_width = max(first_line_bbox[2] - first_line_bbox[0], second_line_bbox[2] - second_line_bbox[0]) + 2 * margin
            rect_height = (first_line_bbox[3] - first_line_bbox[1]) + (second_line_bbox[3] - second_line_bbox[1]) + margin * 2

            # Draw a rounded rectangle with a 15px corner radius
            drawImg.rounded_rectangle([x - margin, y - margin, x + rect_width, y + rect_height],
                                      fill=ImageColor.getrgb("#1a3459"), outline=ImageColor.getrgb("#60c5c7"), width=2, radius=10)


            # Draw the first and second lines of text inside the rectangle
            drawImg.text((x, y), FirstName, font=NameStyle.font, fill=NameStyle.color)
            drawImg.text((x, y + (first_line_bbox[3] - first_line_bbox[1]) + margin), LastName, font=LastNameStyle.font, fill=LastNameStyle.color)

        except Exception as e:
            print(e)
    
    # Save the image
    backgroundImg.save(outputPath)

