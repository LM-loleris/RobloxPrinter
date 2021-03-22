from PIL import Image
import socket
import requests
import upnpclient
import shutil
import tempfile

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
SERVICE_URL = "" # e.g. http://domain.com/project_name/
PASSWORD = "" # e.g. 123IAmSecure

ROBLOX_ASSET_DELIVERY = "https://assetdelivery.roblox.com/v1/asset?id="

def DownloadImage(url, path):
    with requests.get(url, stream = True, headers = HEADERS) as response:
        if response.headers['content-type'] == "binary/octet-stream" or response.headers['content-type'] == "application/octet-stream":
            file_path = path + ".jpg"
            with tempfile.TemporaryFile() as temp:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, temp)
                del response

                img = Image.open(temp)
                # Resizing to 512 limit
                if img.size[0] > 512 or img.size[1] > 512:
                    size_ratio = float(img.size[1]) / float(img.size[0])
                    if size_ratio > 1:
                        img = img.resize((int(512 / size_ratio), 512))
                    else:
                        img = img.resize((512, int(512 * size_ratio)))
                # Adding white background to trasnaprent images:
                if img.mode != "RGBA":
                    img = img.convert("RGB")
                elif img.mode == "RGBA":
                    white_bg = Image.new("RGBA", img.size, "WHITE")
                    white_bg.paste(img, (0, 0), img)
                    img = white_bg.convert('RGB')

                # Root might have grabbed permissions for this file:
                img.save(file_path, quality = 75)

                temp.close()
                return img

                    

"""
def DownloadImage(url, path):
    try:
        with requests.get(url, stream = True, headers = HEADERS) as response:
            if response.headers['content-type'] == "binary/octet-stream":
                file_path = path + ".jpg"
                with tempfile.TemporaryFile() as temp:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, temp)
                    del response
                    try:
                        img = Image.open(temp)
                        # Resizing to 512 limit
                        if img.size[0] > 512 or img.size[1] > 512:
                            size_ratio = float(img.size[1]) / float(img.size[0])
                            if size_ratio > 1:
                                img = img.resize((int(512 / size_ratio), 512))
                            else:
                                img = img.resize((512, int(512 * size_ratio)))
                        # Adding white background to trasnaprent images:
                        if img.mode == "RGBA":
                            white_bg = Image.new("RGBA", img.size, "WHITE")
                            white_bg.paste(img, (0, 0), img)
                            img = white_bg.convert('RGB')
                        img.save(file_path, quality = 75)
                        return file_path
                    finally:
                        temp.close()
    except:
        return None
"""

def GetNextTask():
    try:
        post_data = {"Password":PASSWORD, "RequestType":"GetNextTask"}
        response = requests.post(SERVICE_URL, json = post_data, headers = HEADERS)
        next_task = response.json()
        if "Task" in next_task:
            return next_task
        else:
            return None
    except:
        return None

def ConfirmTask(confirm_token):
    try:
        post_data = {"Password":PASSWORD, "RequestType":"ConfirmTask", "ConfirmToken":confirm_token}
        requests.post(SERVICE_URL, json = post_data, headers = HEADERS)
    except:
        pass

def GetPrinterSignal():
    try:
        post_data = {"Password":PASSWORD, "RequestType":"GetPrinterSignal"}
        response = requests.post(SERVICE_URL, json = post_data, headers = HEADERS)
        signal_data = response.json()
        if "PrinterSignal" in signal_data:
            return signal_data["PrinterSignal"]
        else:
            return None
    except:
        return None

def GetLocalIP():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return str(local_ip)
    except:
        return "0.0.0.0"

def GetPublicIP():
    try:
        public_ip = str(requests.get("https://ident.me").text)
        if len(public_ip) <= 15:
            return public_ip
        else:
            return "0.0.0.0"
    except:
        return "0.0.0.0"


def SetPrinterStatus(is_maintenance, is_paper_low, is_on):
    try:
        post_data = {
            "Password":PASSWORD,
            "RequestType":"SetPrinterStatus",
            "IsMaintenance":is_maintenance,
            "IsPaperLow":is_paper_low,
            "IsOn":is_on,
            "IpLocal":GetLocalIP(),
            "IpPublic":GetPublicIP(),
        }
        requests.post(SERVICE_URL, json = post_data, headers = HEADERS)
        response = requests.post(SERVICE_URL, json = post_data, headers = HEADERS)
        printer_status = response.json()
        return printer_status
    except:
        return None

"""    
img = DownloadImage(
    url = ROBLOX_ASSET_DELIVERY + str(6349102225),
    path = "RobloxImages/" + str(6349102225)
)
print("Done!")
"""

"""
next_task = GetNextTask()
if next_task != None:
    print("Task received!")
    ConfirmTask(next_task["ConfirmToken"])
"""