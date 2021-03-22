HardwareLibrariesActive = True
try:
    import busio
    import board
    import neopixel
    import adafruit_ssd1306
except ImportError:
    HardwareLibrariesActive = False

from PIL import Image, ImageDraw, ImageFont
import colorsys
import threading
import time

import printer_control as PrinterControl
import image_edit as ImageEdit

IS_FLIPPED = True # Flip OLED display 180 degrees

# Thread locked variables:

HardwareLock = threading.Lock()

RequestCount = 0
RequestStop = False

# Hardware setup:

if HardwareLibrariesActive == True:
    pixels = neopixel.NeoPixel(
        board.D18, 4, brightness=1, auto_write = False, pixel_order = neopixel.GRB
    )

    i2c = busio.I2C(board.SCL, board.SDA)
    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr = 0x3C)
    oled_image = None
    oled_draw = None

# Hardware functions:

def ClearScreen():
    global oled_image, oled_draw
    oled_image = Image.new("1", (oled.width, oled.height))
    oled_draw = ImageDraw.Draw(oled_image)

def SendDrawToScreen():
    if IS_FLIPPED == True:
        oled.image(oled_image.rotate(180))
    else:
        oled.image(oled_image)
    oled.show()

def SetLampColor(color, value = 100):
    # Ensuring the V parameter is always 100%:
    hsv = colorsys.rgb_to_hsv(float(color[0]) / 255, float(color[1]) / 255, float(color[2]) / 255)
    rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], float(value) / 100)
    pixels.fill((round(rgb[0] * 255), round(rgb[1] * 255), round(rgb[2] * 255)))
    pixels.show()

def DrawTaskCounter(count = 0):
    font_big = ImageEdit.GetFont("Squareo", size = 52)
    oled_draw.text(
        xy = (64, 32), text = str(count),
        font = font_big, fill = 255, anchor = "mm",
    )

# External control functions:

def StopHardware():
    global RequestStop
    with HardwareLock:
        RequestStop = True

def IncremetRequestCount():
    global RequestCount
    with HardwareLock:
        RequestCount += 1

def ResetRequestCount():
    global RequestCount
    with HardwareLock:
        RequestCount  = 0

# Hardware loop:

ErrorImg = Image.open("Assets/OLED_Error.bmp")
ErrorImg = ErrorImg.convert("1")

def _HardwareUpdate():
    while RequestStop == False:
        with HardwareLock:
            if PrinterControl.CheckIsMaintenance() == True:
                ClearScreen()
                if time.time() % 3 < 1.5:
                    oled_image.paste(ErrorImg, (0, 0))
                SendDrawToScreen()
            else:
                ClearScreen()
                DrawTaskCounter(RequestCount)
                SendDrawToScreen()
        time.sleep(0.1)
    # Stop:
    ClearScreen()
    SendDrawToScreen()
    SetLampColor((0, 0, 0), value = 0)


if HardwareLibrariesActive == True:
    # Startup restart hardware:
    ClearScreen()
    SendDrawToScreen()
    SetLampColor((0, 0, 0), value = 0)

    # Async hardware process
    HardwareProcess = threading.Thread(target = _HardwareUpdate)
    HardwareProcess.daemon = True
    HardwareProcess.start()
    