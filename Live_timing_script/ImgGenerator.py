from PIL import Image, ImageDraw, ImageFont, ImageColor
from pathlib import Path
from PilotClasses import Round, Pilot

Montserrat_Black_file = Path("./fonts/Montserrat","Montserrat-Black.ttf")
Montserrat_Italic_file = Path("./fonts/Montserrat","Montserrat-BoldItalic.ttf")
Franchise_bold_file = Path("./fonts","Franchise-Bold.ttf")


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

def draw_centered_text(drawImg: ImageDraw.Draw,  center_top_coords: tuple, text: str,font, fill):
    """
    Draw text centered at a specified top-center position.

    :param drawImg: The ImageDraw object to draw on.
    :param center_top_coords: A tuple (center_x, top_y) where the text should be centered.
    :param text: The text to be drawn.
    :param font: The font object to be used for the text.
    :param fill: The color of the text.
    """
    baseX, baseY = center_top_coords

    # Calculate the bounding box of the text (left, top, right, bottom)
    text_bbox = drawImg.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]  # width = right - left
    text_height = text_bbox[3] - text_bbox[1]  # height = bottom - top
    
    # Calculate the new X position to center the text horizontally
    center_top_x = baseX - text_width / 2

    # Draw the text at the calculated position
    drawImg.text((center_top_x, baseY), text, font=font, fill=fill)

def draw_center_bottom_text(drawImg: ImageDraw.Draw, center_bottom_coords: tuple, text: str, font, fill):
    """
    Draw text centered at a specified center-bottom position.

    :param drawImg: The ImageDraw object to draw on.
    :param text: The text to be drawn.
    :param center_bottom_coords: A tuple (center_x, bottom_y) where the text should be centered and aligned at the bottom.
    :param font: The font object to be used for the text.
    :param fill: The color of the text.
    """
    baseX, baseY = center_bottom_coords

    # Calculate the bounding box of the text (left, top, right, bottom)
    text_bbox = drawImg.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]  # width = right - left
    text_height = text_bbox[3] - text_bbox[1]  # height = bottom - top

    # Calculate the new X position to center the text horizontally
    center_bottom_x = baseX - text_width / 2

    # Calculate the Y position to align the text at the bottom
    center_bottom_y = baseY - text_height

    # Draw the text at the calculated position
    drawImg.text((center_bottom_x, center_bottom_y), text, font=font, fill=fill)

def draw_right_middle_text(drawImg: ImageDraw.Draw, right_middle_coords: tuple, text: str, font, fill):
    """
    Draw text aligned at a specified right-middle position.

    :param drawImg: The ImageDraw object to draw on.
    :param text: The text to be drawn.
    :param right_middle_coords: A tuple (right_x, middle_y) where the text should be aligned from the right.
    :param font: The font object to be used for the text.
    :param fill: The color of the text.
    """
    rightX, middleY = right_middle_coords

    # Calculate the bounding box of the text (left, top, right, bottom)
    text_bbox = drawImg.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]  # width = right - left
    text_height = text_bbox[3] - text_bbox[1]  # height = bottom - top

    # Calculate the new X and Y positions to align the text to the right and vertically in the middle
    right_middle_x = rightX - text_width
    right_middle_y = middleY - text_height / 2

    # Draw the text at the right and middle Y position
    drawImg.text((right_middle_x, right_middle_y), text, font=font, fill=fill)

def draw_left_middle_text(drawImg: ImageDraw.Draw, left_middle_coords: tuple, text: str, font, fill):
    """
    Draw text aligned at a specified left-middle position.

    :param drawImg: The ImageDraw object to draw on.
    :param text: The text to be drawn.
    :param left_middle_coords: A tuple (left_x, middle_y) where the text should be aligned from the left.
    :param font: The font object to be used for the text.
    :param fill: The color of the text.
    """
    leftX, middleY = left_middle_coords

    # Calculate the bounding box of the text (left, top, right, bottom)
    text_bbox = drawImg.textbbox((0, 0), text, font=font)
    text_height = text_bbox[3] - text_bbox[1]  # height = bottom - top
    
    # Calculate the new Y position to align the text vertically in the middle
    left_middle_y = middleY - text_height / 2

    # Draw the text at the left and middle Y position
    drawImg.text((leftX, left_middle_y), text, font=font, fill=fill)

def trim_text(input, maxLength):
    return input if len(input)<=maxLength else input[:maxLength]+"..."

# ResultRankingCoordinates = {
#     "Buggy" : [(282,466),
#                (325,636),
#                (544,466),
#                (587,636),
#                (806,466),
#                (849,636),
#                (1068,466),
#                (1111,636),
#                (1330,466),
#                (1373,636),
#                (1592,466),
#                (1635,636)
#                 ]
# }

## Generate grid and series image for new serie screen

def generateGridRankingCoordinates():
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

coordinatesDict = generateGridRankingCoordinates()

def generateMainPreRaceGridImage(RankingList:Round, backgroundImagePath:Path, buggyImagePath:Path, outputPath:Path, resize_dimensions=(1920, 1080), buggySize=(230,130)):
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



### Result image generation

def generateMainResultImage(RankingList:Round, backgroundImagePath:Path, outputPath:Path, resize_dimensions=(1920, 1080), buggySize=(230,130)):
    
    NameCoord = [
    (1280, 135),
    (955, 195),
    (1595, 230),
    (935, 500)
]
    yOffset=54

    ResultCategoryStyle = TextStyle(font=Montserrat_Black_file, color=ImageColor.getrgb("white"), size=55)
    ResultSerieStyle = TextStyle(font=Montserrat_Black_file, color=ImageColor.getrgb("#dfdfdf"), size=22)
    
    PodiumNameStyle = TextStyle(font=Montserrat_Black_file, color=ImageColor.getrgb("white"), size=40)
    PodiumLastNameStyle = TextStyle(font=Montserrat_Black_file, color=ImageColor.getrgb("#dfdfdf"), size=30)
    PodiumStatsStyle = TextStyle(font=Montserrat_Italic_file, color=ImageColor.getrgb("#dfdfdf"), size=25)

    ListNameStyle = TextStyle(font=Montserrat_Black_file, color=ImageColor.getrgb("white"), size=25)
    ListLastNameStyle = TextStyle(font=Montserrat_Black_file, color=ImageColor.getrgb("#dfdfdf"), size=25)
    
    backgroundImg = Image.open(backgroundImagePath)
    backgroundImg = backgroundImg.resize(resize_dimensions, Image.LANCZOS)

    drawImg = ImageDraw.Draw(backgroundImg)

    drawImg.text((100,170), RankingList.category_pretty, font=ResultCategoryStyle.font, fill=ResultCategoryStyle.color)
    drawImg.text((100,240), RankingList.serie_pretty, font=ResultSerieStyle.font, fill=ResultSerieStyle.color)

    for index, pilot in enumerate(RankingList.pilotList[:3]):
        baseX, baseY=NameCoord[index]
        try:
            pilotName = pilot.pilot.split(" ")
            
            if len(pilotName)>1:
                draw_centered_text(drawImg, (baseX, baseY), pilotName[1][:12].upper(), font=PodiumNameStyle.font, fill=PodiumNameStyle.color)
            draw_centered_text(drawImg, (baseX, baseY+42), pilotName[0][:15].upper(), font=PodiumLastNameStyle.font, fill=PodiumLastNameStyle.color)
            draw_centered_text(drawImg, (baseX, baseY+78), f"{pilot.laps} LAPS / BEST : {pilot.besttime_s:0.2f}", font=PodiumStatsStyle.font, fill=PodiumStatsStyle.color)
        except Exception as e:
            print(e)
    
    for index, pilot in enumerate(RankingList.pilotList[3:]):
        baseX, baseY = NameCoord[3]
        baseY += index*yOffset
        
        try:
            draw_left_middle_text(drawImg, (baseX, baseY), trim_text(pilot.pilot, 18).upper(), font=ListNameStyle.font, fill=ListNameStyle.color)
            draw_right_middle_text(drawImg, (1700, baseY), f"{pilot.laps} LAPS / BEST : {pilot.besttime_s:0.2f}", font=PodiumStatsStyle.font, fill=PodiumStatsStyle.color)
        except Exception as e:
            print(e)
        
    backgroundImg.save(outputPath)

## Overlay generation for Grid View camere. Only used in finals

StartGridCoordinates=[
    (250,900),#1
    (320,700),#2
    (550,550),#3
    (775,450),#4
    (1000,350),#5
    (1275,475),#6
    (1525,575),#7
    (1625,450),#8
    (1675,350),#9
    (1775,325),#10
    (1800,200),#11
    (1700,100)#12
 ]


def generateStartGridOverlay(RankingList, outputPath, resize_dimensions=(1920, 1080)):
    backgroundImg = Image.new('RGBA', resize_dimensions, (255, 255, 255, 0))
    drawImg = ImageDraw.Draw(backgroundImg)

    # # Draw category and series text
    # drawImg.text((90,127), RankingList.category_pretty, font=CategoryStyle.font, fill=CategoryStyle.color)
    # drawImg.text((90,213), RankingList.serie_pretty, font=SerieStyle.font, fill=SerieStyle.color)

    margin = 10

    for index, pilot in enumerate(RankingList.pilotList):
        try:
            x, y = StartGridCoordinates[index]
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

        except IndexError as e:
            print(f"Error generating Grid image {e}.")
        except Exception as e:
            print(f"Error generating Grid image {e}.")
    
    # Save the image
    backgroundImg.save(outputPath)

