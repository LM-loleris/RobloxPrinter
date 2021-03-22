try:
    from escpos.printer import Usb
except ImportError:
    print("Printer library not available")

from PIL import Image, ImageFont, ImageDraw
import threading
import time

import image_edit as ImageEdit

MAX_VERTICAL_SIZE = 1.5 # Limits image height on print
PRINTER_H = 512 # Printer space horizontal size in pixels
EXPECTED_PRINT_SPEED = 128 # Pixels per second
EXPECTED_MAX_REACT_TIME = 2

PrintTaskLock = threading.Lock()

try:
    Printer = Usb(0x04b8, 0x0202, 0, profile = "TM-T88V")
except:
    Printer = None
    print("Printer not found")

IsMaintenance = False
IsPaperLow = False

CurrentPrintTask = None
PrintQueue = [] # [task, expected_time], ...
ExpectedTaskFinishTime = 0
PrinterStatusRequestStart = None
StatusCheckSwitch = True

# Async print queue handling:
def _QueueHandler():
    global PrinterStatusRequestStart, StatusCheckSwitch, CurrentPrintTask, ExpectedTaskFinishTime, IsMaintenance, IsPaperLow
    while True:
        if len(PrintQueue) > 0:
            queue_entry = None
            with PrintTaskLock:
                queue_entry = PrintQueue.pop(0)
                # Combine expected finish time on subsequent queue entries:
                if CurrentPrintTask != None:
                    ExpectedTaskFinishTime += queue_entry[1]
                else:
                    ExpectedTaskFinishTime = time.time() + queue_entry[1]
                CurrentPrintTask = queue_entry

            try:
                task = queue_entry[0]
                getattr(Printer, task["TaskName"])(**task["Params"])
            except Exception as e:
                print("Printer error: " + str(e))
        else:
            with PrintTaskLock:
                CurrentPrintTask = None
                PrinterStatusRequestStart = time.time()

            # Check one of two statuses every queue check cycle:
            StatusCheckSwitch = not StatusCheckSwitch
            get_status = None
            try:
                if StatusCheckSwitch == True:
                    get_status = Printer.is_online() == False
                else:
                    get_status = Printer.paper_status() < 2
            except Exception:
                # Printer is most likely not available anymore:
                with PrintTaskLock:
                    IsMaintenance = True
            else:
                with PrintTaskLock:
                    PrinterStatusRequestStart = None
                    if get_status != None:
                        if StatusCheckSwitch == True:
                            IsMaintenance = get_status
                        else:
                            IsPaperLow = get_status

            time.sleep(0.1)

if Printer != None:
    QueueHandlerProcess = threading.Thread(target = _QueueHandler)
    QueueHandlerProcess.daemon = True
    QueueHandlerProcess.start()

### Functions:

def AddPrinterTaskToQueue(task, expected_time):
    with PrintTaskLock:
        PrintQueue.append([task, expected_time])

def PrepareImageForPrint(img):
    img_class = img.__class__.__name__
    # Support both path and PIL image:
    if img_class == "str":
        img = Image.open(img)
    elif img_class == None:
        print("Invalid image format")
        return None
    # Limit horizontal image size:
    if img.size[0] > PRINTER_H:
        # Otherwise only limit horizontal image size:
        size_ratio = float(img.size[1]) / float(img.size[0])
        img = img.resize((PRINTER_H, PRINTER_H * size_ratio))
    return img

def PrintImage(img):
    img = PrepareImageForPrint(img)
    expected_time = EXPECTED_MAX_REACT_TIME + img.size[1] / EXPECTED_PRINT_SPEED
    AddPrinterTaskToQueue(
        task = {
            "TaskName":"image",
            "Params":{"img_source":img, "center":True},
        },
        expected_time = expected_time
    )

def PrintNewLine():
    AddPrinterTaskToQueue(
        task = {
            "TaskName":"ln",
            "Params":{},
        },
        expected_time = EXPECTED_MAX_REACT_TIME
    )

def Cut(mode = 'PART', feed = False): # FULL
    AddPrinterTaskToQueue(
        task = {
            "TaskName":"cut",
            "Params":{"mode":mode, "feed":feed},
        },
        expected_time = EXPECTED_MAX_REACT_TIME
    )

def PrintText(txt, hw_font = 0):
    AddPrinterTaskToQueue(
        task = {
            "TaskName":"set",
            "Params":{"align":"center", "bold":True, "font":hw_font}, # Hardware font
        },
        expected_time = EXPECTED_MAX_REACT_TIME
    )
    AddPrinterTaskToQueue(
        task = {
            "TaskName":"textln",
            "Params":{"txt":txt},
        },
        expected_time = 0.1
    )

def PrintFontText(txt, font = "FranklinGothic", size = 10, align = "center", bottom_padding = 0):
    loaded_font = ImageEdit.GetFont(font = font, size = size)
    pixel_size = loaded_font.getsize(txt)
    height = pixel_size[1] + 2
    img = Image.new("L", (PRINTER_H, height + bottom_padding), "WHITE")
    draw = ImageDraw.Draw(img)
    if align == "center":
        draw.text(xy = (PRINTER_H // 2, height // 2), text = txt, fill = (0), font = loaded_font, anchor = "mm")
    elif align == "left":
        draw.text(xy = (0, height // 2), text = txt, fill = (0), font = loaded_font, anchor = "lm")
    elif align == "right":
        draw.text(xy = (PRINTER_H, height // 2), text = txt, fill = (0), font = loaded_font, anchor = "rm")
    else:
        print("Invalid alignment")
        return None
    expected_time = EXPECTED_MAX_REACT_TIME + img.size[1] / EXPECTED_PRINT_SPEED
    AddPrinterTaskToQueue(
        task = {
            "TaskName":"image",
            "Params":{"img_source":img, "center":True},
        },
        expected_time = expected_time
    )

def CheckIsMaintenance():
    with PrintTaskLock:
        if IsMaintenance == True:
            return True
        if CurrentPrintTask != None and time.time() > ExpectedTaskFinishTime:
            return True
        if PrinterStatusRequestStart != None:
            if time.time() - PrinterStatusRequestStart > 4:
                return True
        return False

def CheckIsPaperLow():
    with PrintTaskLock:
        return IsPaperLow