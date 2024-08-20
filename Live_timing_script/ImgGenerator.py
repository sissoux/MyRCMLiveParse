from PIL import Image, ImageDraw, ImageFont, ImageColor
from pathlib import Path

Montserrat_Black_file = Path("./Fonts/Montserrat","Montserrat-Black.ttf")

class TextStyle():
    def __init__(self, font, color=ImageColor.getrgb("black"), size=20) -> None:
        self.font = font
        self.color = color
        self.size = size

pilotStyle = TextStyle(font=Montserrat_Black_file, color=ImageColor.getrgb("red"), size=25)

def initImage():
    # Create a blank image with a transparent background
    image = Image.new('RGBA', (1920, 1080), (255, 255, 255, 0))
    return image

def addTableToImage(image, table):
    draw = ImageDraw.Draw(image)
    
    for line in table:
        text, x, y, style = line
        try:
            font = ImageFont.truetype(style.font, style.size)  
        except IOError:
            print(f"{font} font not found.")
            return    
        draw.text((x, y), text, font=font, fill=style.color)  # Black text color
    return image

# Function to add and resize a PNG image on the generated image
def add_resized_png_to_image(image, png_filepath, x, y, output_width, output_height):
    try:
        # Open the PNG image
        png_image = Image.open(png_filepath).convert("RGBA")
        
        # Resize the PNG image to the desired size
        png_image = png_image.resize((output_width, output_height), Image.LANCZOS)
        
        # Paste the resized PNG onto the base image at the specified coordinates
        image.paste(png_image, (x, y), png_image)
    except Exception as e:
        print(f"Error loading or processing PNG file: {e}")

    return image

def generateRankingImage(ranking, filepath):
    xbase = 600
    ybase = 200
    yoffset = 50
    rankingDisplayTable = []
    for line in ranking:
        rankingDisplayTable.append([line, xbase, ybase, pilotStyle])
        ybase+=yoffset
    
    addTableToImage(initImage(), rankingDisplayTable).save(filepath)

# # Define the table with ["string to print", x, y]
# displayTable = [
#     ["Hello, World!", 0, 0, pilotStyle],
#     ["Python is awesome!", 500, 300, pilotStyle],
#     ["This is a transparent image.", 400, 600, pilotStyle]
# ]

# # Generate the base image with text
# base_image = initImage()

# base_image = addTableToImage(base_image, displayTable)

# # Add and resize a PNG image onto the generated image
# final_image = add_resized_png_to_image(base_image, "./example.png", 800, 400, 400, 400)

# # Save the final image
# final_image.save("final_output_image.png")