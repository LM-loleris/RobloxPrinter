--[[
[TheBox]

-[PrinterHttp]---------------------------------------
	Printer app proxy server http methods
	
	Functions:
	
		
		
--]]

local SETTINGS = {
	AppUrl = "", -- e.g. http://domain.com/project_name/
	AppPassword = "", -- e.g. 123IAmSecure
}

----- Module Table -----

local PrinterHttp = {
	
}

----- Private Variables -----

local HttpService = game:GetService("HttpService")

----- Public functions -----

function PrinterHttp.GetPrinterStatus() --> [table] or nil -- {IsActive, IsMaintenance, IsPaperLow, IsOn, IpLocal}
	local status_table = nil
	pcall(function()
		local post_data = {
			Password = SETTINGS.AppPassword,
			RequestType = "GetPrinterStatus"
		}
		local result = HttpService:PostAsync(SETTINGS.AppUrl, HttpService:JSONEncode(post_data))
		if type(result) == "string" then
			local decode = HttpService:JSONDecode(result)
			if decode.IsActive ~= nil then
				status_table = decode
			end
		end
	end)
	return status_table
end

function PrinterHttp.MakePrintRequest(user_id, username, image_id, robux_paid)
	coroutine.wrap(function()
		local post_data = {
			Password = SETTINGS.AppPassword,
			RequestType = "MakeRequest",
			
			TaskType = "Image",
			TaskParams = {
				UserId = user_id,
				Username = username,
				ImageId = image_id,
				RobuxPaid = robux_paid,
			},
		}
		HttpService:PostAsync(SETTINGS.AppUrl, HttpService:JSONEncode(post_data))
	end)()
end

return PrinterHttp