from PIL import Image
import math

DEFAULT_CHARACTER_MAP = "@%#*+=-:. "

HIGH_DEFINITION_MAP = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1"
HIGH_DEFINITION_MAP += "{}[]?-_+~<>i!lI;:,\"^`\'. "

HIGH_CONTRAST_MAP = "█▓▒░ "

def PixelToCharacter(pixel, character_map):
    return character_map[math.floor(float(pixel) / 256 * len(character_map))]

# 42 with font 0
# 57 with font 1
def GenerateASCIIArt(img, character_map = DEFAULT_CHARACTER_MAP, max_width = 200, max_ratio = 1.5, output = "text", stretch_fix = 0.33):
    # Load image:
    img_class = img.__class__.__name__
    if img_class == "str":
        img = Image.open(img)
    elif img_class == None:
        print("Invalid image format")
        return None
    # Figure out text bounds:
    size_ratio = float(img.size[1] * stretch_fix) / img.size[0]
    max_height = int(max_width * max_ratio * stretch_fix)
    desired_height = int(size_ratio * max_width)
    fit_height = min(max_height, desired_height)
    fit_width = min(max_width, int(fit_height / size_ratio))
    # Convert to ASCII
    img = img.resize((fit_width, fit_height))
    img = img.convert("L")

    pixels = img.getdata()
    pixel_count = 0

    if output == "text":

        text = ""
        for y in range(fit_height):
            for _ in range(fit_width):
                text += PixelToCharacter(pixels[pixel_count], character_map)
                pixel_count += 1
            if y < fit_height - 1:
                text += "\n"
        return text

    elif output == "table":

        characters = []
        for _ in range(fit_height):
            row = []
            characters.append(row)
            for _ in range(fit_width):
                row.append(PixelToCharacter(pixels[pixel_count], character_map))
                pixel_count += 1
        return characters

"""
print(GenerateASCIIArt(
    img = "RobloxImages/637281025.jpg",
    output = "text"
))
"""