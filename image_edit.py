from PIL import Image, ImageFont, ImageDraw
from cv2 import cv2
import numpy
import ascii_art

import tempfile

Fonts = {
    "FranklinGothic":"Fonts/FranklinGothic.ttf",
    "FrontPageNeue":"Fonts/FrontPageNeue.otf",
    "ModernDOS8x14":"Fonts/ModernDOS8x14.ttf",
    "Square":"Fonts/Square.ttf",
    "Squareo":"Fonts/Squareo.ttf",
    "Symtext":"Fonts/Symtext.ttf",
}

def GetImageResize(img, desired_width, max_height = None, max_ratio = None):
    # Load image:
    img_class = img.__class__.__name__
    if img_class == "str":
        img = Image.open(img)
    elif img_class == None:
        print("Invalid image format")
        return None
        
    size_ratio = float(img.size[1]) / img.size[0]
    fit_height = int(size_ratio * desired_width)
    if max_height != None:
        fit_height = min(fit_height, max_height)
    elif max_ratio != None:
        max_height = int(desired_width * max_ratio)
        fit_height = min(max_height, fit_height)
    fit_width = int(fit_height / size_ratio)
    #if size_ratio < 0:
    #    fit_width = desired_width
    return (fit_width, fit_height)

def GetFont(font = "FranklinGothic", size = 20):
    if font in Fonts:
        return ImageFont.truetype(Fonts[font], size)
    else:
        print("Undefined font")
        return ImageFont.truetype("FranklinGothic", size)

def ToASCIIArt(img, character_map = ascii_art.DEFAULT_CHARACTER_MAP):
    txt = ascii_art.GenerateASCIIArt(img = img, character_map = character_map, max_width = 300, max_ratio = 1.5, output = "text", stretch_fix = 0.6)
    loaded_font = GetFont(font = "ModernDOS8x14", size = 24)
    pixel_size = loaded_font.getsize_multiline(txt)
    img = Image.new("L", pixel_size, "WHITE")
    draw = ImageDraw.Draw(img)
    draw.fontmode = "L"
    draw.text(xy = (0, 0), text = txt, fill = (0), font = loaded_font) # , anchor = "lt"
    return img

def ImageToBW(img):
    # Load image:
    img_class = img.__class__.__name__
    if img_class == "str":
        img = Image.open(img)
    elif img_class == None:
        print("Invalid image format")
        return None
    # Adding white background to trasnaprent images:
    working_size = GetImageResize(img, 512, max_ratio = 1.5)
    img = img.resize(working_size)
    img = img.convert("RGBA")
    white_bg = Image.new("RGB", img.size, "WHITE")
    white_bg.paste(img, (0, 0), img)
    img = white_bg.convert("RGB")
    
    img = img.quantize(colors = 2, method = Image.MAXCOVERAGE)
    img = img.convert(mode = "1", dither = Image.NONE)
    return img

def ImageToBWEdgeDetect(img):
    # Load image:
    img_class = img.__class__.__name__
    if img_class == "str":
        img = Image.open(img)
    elif img_class == None:
        print("Invalid image format")
        return None
    # Adding white background to trasnaprent images:
    working_size = GetImageResize(img, 512, max_ratio = 1.5)
    img = img.resize(working_size)
    img = img.convert("RGBA")
    white_bg = Image.new("RGB", img.size, "WHITE")
    white_bg.paste(img, (0, 0), img)
    img = white_bg.convert("RGB")
    # Usin OpenCV to find edges:
    # img = cv2.imread(img, 0)
    img = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2GRAY)
    img = cv2.resize(img, working_size, interpolation = cv2.INTER_LINEAR)

    img = cv2.medianBlur(img, 5)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)

    # img = img.convert("RGBA")
    # white_bg = Image.new("RGB", img.size, "WHITE")
    # white_bg.paste(img, (0, 0), img)
    # img = white_bg.convert("RGB")
    
    # img = img.quantize(colors = 2, method = Image.MAXCOVERAGE)
    # img = img.convert(mode = "1", dither = Image.NONE)
    #return img.quantize(colors = 2)
    return img

# img = ImageToBWEdgeDetect("RobloxImages/5918162200.jpg")
# img.save("grayscale_test.png")