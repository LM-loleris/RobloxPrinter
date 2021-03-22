import requests

# I was using this to test my php code on the web server

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
SERVICE_URL = ""
PASSWORD = ""

"""
post_data = {"Password":PASSWORD, "RequestType":"GetNextTask",
"IsMaintenance":True, "PaperStatus":1, "IpLocal":"1.1.1.1"}
"""

post_data = {"Password":PASSWORD, "RequestType":"GetPrinterStatus"}

"""
"TaskType":"Special",
"TaskParams":{
            "UserId":2312310,
            "Username":"loleris",
            "Type":"sus",
            "Param":"",
            "RobuxPaid":100,
}
"""

response = requests.post(SERVICE_URL, json = post_data, headers = HEADERS)
print(response.text)

print("Hello world!")