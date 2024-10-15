from PIL import Image, ImageDraw, ImageFont, ImageColor
from pathlib import Path
from PilotClasses import Round, Pilot
import shutil

class ScreenGenerator:
    
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

    def __init__(self, live_base_path, gdrive_base_path):
        """
        Initialize the ScreenGenerator with common base paths.
        
        :param live_base_path: Path to the live base directory.
        :param gdrive_base_path: Path to the GDrive base directory.
        """
        if live_base_path is not None:
            self.live_base_path = Path(live_base_path)
        else:
            self.live_base_path = None
        if gdrive_base_path is not None:
            self.gdrive_base_path = Path(gdrive_base_path)
        else:
            self.gdrive_base_path = None
        self.output_image_path = None  # To be defined in child classes

    def generate(self, current_round:Round):
        """
        Generate the image. This method should be implemented in child classes.
        
        :param current_round: Object containing details of the current round.
        """
        raise NotImplementedError("Child classes must implement the generate method.")

    def save(self, current_round:Round, save_directory, suffix=""):
        """
        Save the generated image to a specified directory.
        
        :param current_round: Object containing details of the current round (e.g., category, series, etc.).
        :param save_directory: Path where the generated file should be saved.
        :param suffix: Text to be added to the end of the filename
        """
        # Construct the output path using the round details
        output_file_name = f"{current_round.category_pretty}-{current_round.serie_pretty}-{suffix}.png"
        save_path = Path(save_directory, output_file_name)
        Path(save_directory).mkdir(parents=True, exist_ok=True)
        
        # Copy the generated image to the specified directory
        shutil.copyfile(self.output_image_path, save_path)

    def draw_centered_text(self, drawImg: ImageDraw.Draw,  center_top_coords: tuple, text: str,font, fill):
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

    def draw_center_bottom_text(self, drawImg: ImageDraw.Draw, center_bottom_coords: tuple, text: str, font, fill):
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

    def draw_right_middle_text(self, drawImg: ImageDraw.Draw, right_middle_coords: tuple, text: str, font, fill):
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

    def draw_left_middle_text(self, drawImg: ImageDraw.Draw, left_middle_coords: tuple, text: str, font, fill):
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

    def trim_text(self, input, maxLength):
        return input if len(input)<=maxLength else input[:maxLength]+"..."



class GridOverlayScreenGen(ScreenGenerator):
    NameStyle =     ScreenGenerator.TextStyle(font=ScreenGenerator.Montserrat_Black_file, color=ImageColor.getrgb("white"), size=18)
    LastNameStyle = ScreenGenerator.TextStyle(font=ScreenGenerator.Montserrat_Black_file, color=ImageColor.getrgb("white"), size=15)
    
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
    
    def __init__(self, live_base_path, FileName):
        """
        Initialize the GridOverlay class with specific paths for background and buggy images.
        
        :param live_base_path: Path to the live base directory.
        :param gdrive_base_path: Path to the GDrive base directory.
        :param background_image_name: Name of the background image file.
        :param buggy_image_name: Name of the buggy image file.
        """
        super().__init__(live_base_path, None)
        self.background_image_path = None
        self.buggy_image_path = None
        self.output_image_path = Path(self.live_base_path, FileName)

    def save(self, current_round:Round, save_directory, suffix="GridOverlay"):
        """
        Save the generated image to a specified directory.
        
        :param current_round: Object containing details of the current round (e.g., category, series, etc.).
        :param save_directory: Path where the generated file should be saved.
        """
        super().save(current_round, save_directory, suffix=suffix)

        ## Overlay generation for Grid View camere. Only used in finals

    def generateStartGridOverlay(self, RankingList, outputPath, resize_dimensions=(1920, 1080)):
        backgroundImg = Image.new('RGBA', resize_dimensions, (255, 255, 255, 0))
        drawImg = ImageDraw.Draw(backgroundImg)
        margin = 5

        for index, pilot in enumerate(RankingList.pilotList):
            try:
                x, y = self.StartGridCoordinates[index]

                FirstName = f"{index+1} {pilot.FirstName[:12].upper()}"
                LastName = f"    {pilot.LastName[:18]}"

                # Get the bounding box for the first and second lines of text
                first_line_bbox = drawImg.textbbox((x, y), FirstName, font=self.NameStyle.font)
                second_line_bbox = drawImg.textbbox((x, y), LastName, font=self.LastNameStyle.font)

                # Calculate the width and height of the enclosing rectangle
                rect_width = max(first_line_bbox[2] - first_line_bbox[0], second_line_bbox[2] - second_line_bbox[0]) + 2 * margin
                rect_height = (first_line_bbox[3] - first_line_bbox[1]) + (second_line_bbox[3] - second_line_bbox[1]) + margin * 2

                # Draw a rounded rectangle with a 15px corner radius
                drawImg.rounded_rectangle([x - margin, y - margin, x + rect_width, y + rect_height],
                                        fill=ImageColor.getrgb("#1a3459"), outline=ImageColor.getrgb("#60c5c7"), width=2, radius=10)


                # Draw the first and second lines of text inside the rectangle
                drawImg.text((x, y), FirstName, font=self.NameStyle.font, fill=self.NameStyle.color)
                drawImg.text((x, y + (first_line_bbox[3] - first_line_bbox[1]) + margin), LastName, font=self.LastNameStyle.font, fill=self.LastNameStyle.color)

            except IndexError as e:
                print(f"Error generating Grid image {e}.")
            except Exception as e:
                print(f"Error generating Grid image {e}.")
        
        # Save the image
        backgroundImg.save(outputPath)

    def generate(self, current_round:Round):
        """
        Generate the pre-race grid image using the current round information.
        
        :param current_round: Object containing details of the current round (e.g., category, series, etc.).
        """
        self.generateStartGridOverlay(
            current_round,
            outputPath=self.output_image_path
        )


class PreStartScreenGen(ScreenGenerator):
    NameStyle =     ScreenGenerator.TextStyle(font=ScreenGenerator.Montserrat_Black_file, color=ImageColor.getrgb("white"), size=18)
    LastNameStyle = ScreenGenerator.TextStyle(font=ScreenGenerator.Montserrat_Black_file, color=ImageColor.getrgb("white"), size=15)
    CategoryStyle = ScreenGenerator.TextStyle(font=ScreenGenerator.Montserrat_Black_file, color=ImageColor.getrgb("white"), size=75)
    SerieStyle =    ScreenGenerator.TextStyle(font=ScreenGenerator.Montserrat_Black_file, color=ImageColor.getrgb("#1a3459"), size=50)
    PositionStyle = ScreenGenerator.TextStyle(font=ScreenGenerator.Franchise_bold_file, color=ImageColor.getrgb("white"), size=65)


    def generateGridRankingCoordinates(self):
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
    
    
    def __init__(self, live_base_path, gdrive_base_path, background_image_path, buggy_image_path, FileName):
        """
        Initialize the GridOverlay class with specific paths for background and buggy images.
        
        :param live_base_path: Path to the live base directory.
        :param gdrive_base_path: Path to the GDrive base directory.
        :param background_image_name: Name of the background image file.
        :param buggy_image_name: Name of the buggy image file.
        """
        super().__init__(live_base_path, gdrive_base_path)
        self.background_image_path = Path(self.gdrive_base_path, background_image_path)
        self.buggy_image_path = Path(self.gdrive_base_path, buggy_image_path) 
        self.output_image_path = Path(self.live_base_path, FileName)
        self.coordinatesDict = self.generateGridRankingCoordinates()

    def save(self, current_round:Round, save_directory, suffix="NewRoundScreen"):
        """
        Save the generated image to a specified directory.
        
        :param current_round: Object containing details of the current round (e.g., category, series, etc.).
        :param save_directory: Path where the generated file should be saved.
        """
        super().save(current_round, save_directory, suffix=suffix)

        ## Overlay generation for Grid View camere. Only used in finals


    def generate(self, current_round:Round):
        """
        Generate the pre-race grid image using the current round information.
        
        :param current_round: Object containing details of the current round (e.g., category, series, etc.).
        """
        self.generateMainPreRaceGridImage(
            current_round,
            backgroundImagePath=self.background_image_path,
            buggyImagePath=self.buggy_image_path,
            outputPath=self.output_image_path
        )

    def generateMainPreRaceGridImage(self, RankingList:Round, backgroundImagePath:Path, buggyImagePath:Path, outputPath:Path, resize_dimensions=(1920, 1080), buggySize=(230,130)):
        backgroundImg = Image.open(backgroundImagePath)
        backgroundImg = backgroundImg.resize(resize_dimensions, Image.LANCZOS)

        buggyImg = Image.open(buggyImagePath)
        buggyImg =  buggyImg.resize(buggySize, Image.LANCZOS)

        drawImg = ImageDraw.Draw(backgroundImg)

        drawImg.text((90,127), RankingList.category_pretty, font=self.CategoryStyle.font, fill=self.CategoryStyle.color)
        drawImg.text((90,213), RankingList.serie_pretty, font=self.SerieStyle.font, fill=self.SerieStyle.color)

        for index, pilot in enumerate(RankingList.pilotList):
            if index>=len(self.coordinatesDict["buggy"]):
                break
            try:
                backgroundImg.paste(buggyImg, self.coordinatesDict["buggy"][index], buggyImg)
            except IndexError:
                print(f"Error adding buggy image for pilot {index}")

            drawImg.text(self.coordinatesDict["Position"][index], f"{index+1}", font=self.PositionStyle.font, fill=self.PositionStyle.color, anchor="rt")
            
            try:
                drawImg.text(self.coordinatesDict["Name"][index], pilot.LastName[:12].upper(), font=self.NameStyle.font, fill=self.NameStyle.color)
                drawImg.text(self.coordinatesDict["LastName"][index], pilot.FirstName[:18], font=self.LastNameStyle.font, fill=self.LastNameStyle.color)
            except Exception as e:
                print(e)
            
        backgroundImg.save(outputPath)


class ResultScreenGen(ScreenGenerator):
    
    ResultCategoryStyle =   ScreenGenerator.TextStyle(font=ScreenGenerator.Montserrat_Black_file, color=ImageColor.getrgb("white"), size=55)
    ResultSerieStyle =      ScreenGenerator.TextStyle(font=ScreenGenerator.Montserrat_Black_file, color=ImageColor.getrgb("#dfdfdf"), size=22)

    PodiumNameStyle =       ScreenGenerator.TextStyle(font=ScreenGenerator.Montserrat_Black_file, color=ImageColor.getrgb("white"), size=36)
    PodiumLastNameStyle =   ScreenGenerator.TextStyle(font=ScreenGenerator.Montserrat_Black_file, color=ImageColor.getrgb("#dfdfdf"), size=30)
    PodiumStatsStyle =      ScreenGenerator.TextStyle(font=ScreenGenerator.Montserrat_Italic_file, color=ImageColor.getrgb("#dfdfdf"), size=25)

    ListNameStyle =         ScreenGenerator.TextStyle(font=ScreenGenerator.Montserrat_Black_file, color=ImageColor.getrgb("white"), size=25)
    ListLastNameStyle =     ScreenGenerator.TextStyle(font=ScreenGenerator.Montserrat_Black_file, color=ImageColor.getrgb("#dfdfdf"), size=25)

    NameCoord = [
        (1280, 155),
        (955, 195),
        (1595, 235),
        (935, 500)
    ]
    yOffset=54
    
    def __init__(self, live_base_path, gdrive_base_path, background_image_path, FileName):
        """
        Initialize the GridOverlay class with specific paths for background and buggy images.
        
        :param live_base_path: Path to the live base directory.
        :param gdrive_base_path: Path to the GDrive base directory.
        :param background_image_name: Name of the background image file.
        :param buggy_image_name: Name of the buggy image file.
        """
        super().__init__(live_base_path, gdrive_base_path)
        self.background_image_path = Path(self.gdrive_base_path, background_image_path)
        self.buggy_image_path = None
        self.output_image_path = Path(self.live_base_path, FileName)

    def save(self, current_round:Round, save_directory, suffix="Results"):
        """
        Save the generated image to a specified directory.
        
        :param current_round: Object containing details of the current round (e.g., category, series, etc.).
        :param save_directory: Path where the generated file should be saved.
        """
        super().save(current_round, save_directory, suffix=suffix)

        ## Overlay generation for Grid View camere. Only used in finals


    def generate(self, current_round:Round):
        """
        Generate the pre-race grid image using the current round information.
        
        :param current_round: Object containing details of the current round (e.g., category, series, etc.).
        """
        self.generateMainResultImage(
            current_round,
            backgroundImagePath=self.background_image_path,
            outputPath=self.output_image_path
        )

    ### Result image generation

    def generateMainResultImage(self, RankingList:Round, backgroundImagePath:Path, outputPath:Path, resize_dimensions=(1920, 1080)):
        backgroundImg = Image.open(backgroundImagePath)
        backgroundImg = backgroundImg.resize(resize_dimensions, Image.LANCZOS)

        drawImg = ImageDraw.Draw(backgroundImg)

        drawImg.text((100,170), RankingList.category_pretty, font=self.ResultCategoryStyle.font, fill=self.ResultCategoryStyle.color)
        drawImg.text((100,240), RankingList.serie_pretty, font=self.ResultSerieStyle.font, fill=self.ResultSerieStyle.color)

        for index, pilot in enumerate(RankingList.pilotList[:3]):
            baseX, baseY=self.NameCoord[index]
            try:            
                self.draw_centered_text(drawImg, (baseX, baseY), pilot.LastName[:13].upper(), font=self.PodiumNameStyle.font, fill=self.PodiumNameStyle.color)
                self.draw_centered_text(drawImg, (baseX, baseY+42), pilot.FirstName[:15].upper(), font=self.PodiumLastNameStyle.font, fill=self.PodiumLastNameStyle.color)
                self.draw_centered_text(drawImg, (baseX, baseY+78), f"{pilot.laps} LAPS / BEST : {pilot.besttime_s:0.2f}s", font=self.PodiumStatsStyle.font, fill=self.PodiumStatsStyle.color)
            except Exception as e:
                print(e)
        
        for index, pilot in enumerate(RankingList.pilotList[3:]):
            baseX, baseY = self.NameCoord[3]
            baseY += index*self.yOffset
            
            try:
                self.draw_left_middle_text(drawImg, (baseX, baseY), self.trim_text(pilot.pilot, 18).upper(), font=self.ListNameStyle.font, fill=self.ListNameStyle.color)
                self.draw_right_middle_text(drawImg, (1700, baseY+4), f"{pilot.laps} LAPS / BEST : {pilot.besttime_s:0.2f}s", font=self.PodiumStatsStyle.font, fill=self.PodiumStatsStyle.color)
            except Exception as e:
                print(e)
            
        backgroundImg.save(outputPath)


