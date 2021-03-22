from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import time
import threading
import subprocess
import os
import sys

import web_app as WebApp
import printer_control as PrinterControl
import twitch_stream as TwitchStream
import ascii_art as ASCIIArt
import image_edit as ImageEdit
import hardware as Hardware
import special_tasks as SpecialTasks

STREAMING_ENABLED = True # Overrides streaming config
HIDDEN = False # Hides acctive status from Roblox game
ORIENTATION = 0 # (0 or 1) Changes the direction of content
PRINTER_ABANDON_TIME = 60 * 5 # How much time until the stream will be turned off after paper runs out or a jam occurs

# References to modules:

Printer = PrinterControl.Printer
IsCameraConnected = TwitchStream.IsCameraConnected()

PrintImage = PrinterControl.PrintImage
PrintText = PrinterControl.PrintText
PrintFontText = PrinterControl.PrintFontText
PrintNewLine = PrinterControl.PrintNewLine
Cut = PrinterControl.Cut

# Directories:

if not os.path.exists('RobloxImages'):
    os.makedirs('RobloxImages')

if not os.path.exists('BWImages'):
    os.makedirs('BWImages')

# Async constant printer status updating:

PrinterStatusLock = threading.Lock()
IsPrintingActive = False

AbandonTimer = 0
IsPrinterAbandoned = False

def CheckIsPrintingActive():
    with PrinterStatusLock:
        return IsPrintingActive

def UpdateStreamState(is_streaming_active):
    if TwitchStream.IsStreamRunning() != is_streaming_active:
        if is_streaming_active == True:
            TwitchStream.StartStream()
        else:
            TwitchStream.StopStream()

def _PrinterStatusUpdate():
    global AbandonTimer, IsPrinterAbandoned, IsPrintingActive
    while True:
        try:
            is_maintenance = PrinterControl.CheckIsMaintenance()
            is_paper_low = PrinterControl.CheckIsPaperLow()
            printer_status = WebApp.SetPrinterStatus(
                is_maintenance = is_maintenance,
                is_paper_low = is_paper_low,
                is_on = IsPrintingActive and not HIDDEN,
            )
            # Printer abandonment logic:
            with PrinterStatusLock:
                if is_maintenance == True:
                    if AbandonTimer == 0:
                        AbandonTimer = time.time()
                    elif time.time() - AbandonTimer > PRINTER_ABANDON_TIME:
                        IsPrinterAbandoned = True
                else:
                    AbandonTimer = 0
                    IsPrinterAbandoned = False
            
            if printer_status != None:
                # IsPrintingActive logic:
                with PrinterStatusLock:
                    if printer_status["IsPrintingActive"] == True:
                        if printer_status["IsScheduled"] == False:
                            IsPrintingActive = True
                        elif printer_status["NextStartTime"] < printer_status["NextStopTime"]:
                            IsPrintingActive = False
                        else:
                            IsPrintingActive = True
                    else:
                        IsPrintingActive = False
                # Streaming activation:
                if STREAMING_ENABLED == True and IsCameraConnected == True:
                    with PrinterStatusLock:
                        UpdateStreamState(IsPrintingActive and printer_status["IsStreamActive"] and IsPrinterAbandoned == False)
        except:
            pass
        time.sleep(1)

PrinterStatusProcess = threading.Thread(target = _PrinterStatusUpdate)
PrinterStatusProcess.daemon = True
PrinterStatusProcess.start()

# Main code:

def HandleImageTask(task_data):
    img = WebApp.DownloadImage(
        url = WebApp.ROBLOX_ASSET_DELIVERY + str(task_data["Task"]["ImageId"]),
        path = "RobloxImages/" + str(task_data["Task"]["ImageId"])
    )
    if img != None:
        """
        date_time_obj = datetime.now()
        PrintNewLine()
        PrintText(task_data["Task"]["Username"])
        PrintText(date_time_obj.strftime("(%m/%d/%Y - %H:%M:%S)"))
        PrintNewLine()
        PrintImage(image_path)
        """
        # Generate image request:
        bw_image = ImageEdit.ImageToBWEdgeDetect(img)
        try:
            # Root might have grabbed permissions for this file:
            bw_image.save("BWImages/" + str(task_data["Task"]["ImageId"]) + ".jpg", quality = 75)
        except:
            pass

        gen_img = Image.new("RGB", (PrinterControl.PRINTER_H, PrinterControl.PRINTER_H), "WHITE")
        gen_draw = ImageDraw.Draw(gen_img)

        paste_offset = 40
        bw_image = bw_image.resize(ImageEdit.GetImageResize(bw_image, 512, max_height = 512 - paste_offset))
        paste_position = (
            int(gen_img.size[0] - bw_image.size[0]) // 2,
            paste_offset + int(gen_img.size[1] - paste_offset) // 2 - bw_image.size[1] // 2
        )
        gen_img.paste(bw_image, paste_position)

        gen_font = ImageEdit.GetFont("FrontPageNeue", size = 35)
        gen_draw.text(
            xy = (1, 7), text = task_data["Task"]["Username"],
            font = gen_font, fill = (0, 0, 0), anchor = "lt",
        )
        gen_font = ImageEdit.GetFont("FrontPageNeue", size = 45)
        gen_draw.text(
            xy = (gen_img.size[0] - 1, 3), text = task_data["Task"]["ImageId"],
            font = gen_font, fill = (0, 0, 0), anchor = "rt",
        )

        if ORIENTATION == 0:
            gen_img = gen_img.rotate(-90)
        else:
            gen_img = gen_img.rotate(90)

        PrintImage(gen_img)

        print("Image request from " + str(task_data["Task"]["UserId"])
                    + " (" + task_data["Task"]["Username"] + ")")
        Hardware.IncremetRequestCount()
    else:
        print("FAILED image request from " + str(task_data["Task"]["UserId"])
                    + " (" + task_data["Task"]["Username"] + ")")

def HandleSpecialTask(task_data):
    try:
        special_task = getattr(SpecialTasks, task_data["Task"]["Type"])
    except:
        print("Special task \"" + str(task_data["Task"]["Type"]) + "\" not defined")
    else:
        print("Found!")
        special_task(task_data["Task"])

def HandleAdminTask(task_data):
    print("Handling admin task")

CutCounter = 0

def AskForPrintTask():
    global CutCounter
    task_data = WebApp.GetNextTask()
    if task_data != None:
        WebApp.ConfirmTask(task_data["ConfirmToken"])
        try:
            if task_data["TaskType"] == "Image":
                HandleImageTask(task_data)
            elif task_data["TaskType"] == "Special":
                HandleSpecialTask(task_data)
            elif task_data["TaskType"] == "Admin":
                HandleAdminTask(task_data)
        except Exception as e:
            print(e)
        else:
            # Auto cutting logic:
            CutCounter += 1
            if CutCounter >= 3:
                CutCounter = 0
                # Cut()
            # else:
                # PrintNewLine()


# Try to kill ffmpeg running from a previous session:
try:
    StreamProcess = subprocess.Popen("sudo killall ffmpeg",
                            stdout = subprocess.DEVNULL,
                            stderr = subprocess.DEVNULL,
                            shell = True,
                            )
except:
    pass

print("Printer program begin (CTRL+C to exit)")

PrinterSignal = None

while True:
    try:
        try:
            printer_signal = WebApp.GetPrinterSignal()
            if printer_signal != None:
                PrinterSignal = printer_signal
                break
            if PrinterControl.CheckIsMaintenance() == False:
                if CheckIsPrintingActive() == True:
                    AskForPrintTask()
            else:
                Hardware.ResetRequestCount()
            time.sleep(1)
        except Exception as e:
            print(e)
    except KeyboardInterrupt:
        print("Program exit")
        raise

# Cleanup:
WebApp.SetPrinterStatus(is_maintenance = False, is_paper_low = False, is_on = False)
if TwitchStream.IsStreamRunning() == True:
    TwitchStream.StopStream()
try:
    Hardware.StopHardware()
    time.sleep(0.3) # Wait for hardware thread to stop
except:
    pass

# Printer signal:
if PrinterSignal == "RestartApp":
    print("Restarting app...")
    os.execv(sys.executable, ['python'] + sys.argv)
elif PrinterSignal == "ShutdownApp":
    print("Closing app...")
    try:
        StreamProcess = subprocess.Popen("sudo systemctl stop robloxprinter.service",
                                stdout = subprocess.DEVNULL,
                                stderr = subprocess.DEVNULL,
                                shell = True,
                                )
    except:
        pass
elif PrinterSignal == "ShutdownDevice":
    print("Shutting down")
    try:
        command = "/usr/bin/sudo /sbin/shutdown -h now"
        subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    except:
        pass

"""
img = "RobloxImages/2458875704.jpg"

PrintFontText("OnlyTwentyCharacters", font = "FrontPageNeue", size = 45, bottom_padding = 5)
PrintFontText("(03/12/2021 - 07:19)", font = "FrontPageNeue", size = 35, bottom_padding = 5)
PrintText(ASCIIArt.GenerateASCIIArt(img), hw_font = 1)
"""

"""
PrintNewLine()
PrintText(ASCIIArt.GenerateASCIIArt(img))

PrintNewLine()
PrintText(ASCIIArt.GenerateASCIIArt(img, character_map = ASCIIArt.HIGH_CONTRAST_MAP))
"""

"""
PrintNewLine()
PrintText(ASCIIArt.GenerateASCIIArt(img, character_map = ASCIIArt.HIGH_DEFINITION_MAP))

PrintNewLine()
PrintImage(ASCIIArt.Shrink(img), nearest = True)
"""

"""
PrintNewLine()
PrintFontText("loleris", size = 35)
PrintFontText("(03/12/2021 07:19)", size = 35)
PrintNewLine()
PrintImage(PrinterControl.PrepareImageForPrint("test.png"))
"""