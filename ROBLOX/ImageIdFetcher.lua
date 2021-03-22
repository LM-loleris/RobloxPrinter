--[[
[TheBox]

-[ImageIdFetcher]---------------------------------------
	Attempts to get the image id from user inputted string of a link or decal / image id
	
	Functions:
	
		ImageIdFetcher.Fetch(user_input) --> image_id [number] or nil
			user_input   [any]
		
--]]

local SETTINGS = {
	
}

----- Module Table -----

local ImageIdFetcher = {
	
}

----- Private Variables -----

local InsertService = game:GetService("InsertService")
local MarketplaceService = game:GetService("MarketplaceService")
local RunService = game:GetService("RunService")

----- Private functions -----

local function ExtractDecal(instance)
	if instance.ClassName == "Decal" then
		return instance
	else
		for _, obj in ipairs(instance:GetDescendants()) do
			local get_decal = ExtractDecal(obj)
			if get_decal ~= nil then
				return get_decal
			end
		end
	end
	return nil
end

local function GetImageIdAsImageAsync(image_id, callback) --> image_id or nil
	image_id = tonumber(image_id)
	if type(image_id) == "number" and image_id > 0 then
		local product_info
		pcall(function()
			product_info = MarketplaceService:GetProductInfo(image_id, Enum.InfoType.Asset)
		end)
		if product_info ~= nil and type(product_info) == "table" then
			if product_info.AssetTypeId == 1 and product_info.AssetId > 0 then
				callback(product_info.AssetId)
				callback = nil
			end
		end
	end
	if callback ~= nil then
		callback()
	end
end

local function GetImageIdAsDecalAsync(decal_id, callback) --> image_id or nil
	decal_id = tonumber(decal_id)
	if type(decal_id) == "number" and decal_id > 0 then

		local decalInfo = MarketplaceService:GetProductInfo(decal_id)

		for i = decal_id - 20, decal_id + 1 do
			local info = MarketplaceService:GetProductInfo(i)
			if info.Creator.Id == decalInfo.Creator.Id and info.AssetTypeId == 1 then
				callback(i)
				callback = nil
				return
			end
		end

	end
	if callback ~= nil then
		callback()
	end
end

----- Public functions -----

function ImageIdFetcher.Fetch(user_input) --> image_id [number] or nil
	local asset_id = tonumber(user_input)
	if asset_id == nil then
		asset_id = tonumber(string.match(user_input, "%d+"))
	end
	if asset_id ~= nil then
		local jobs = 2
		local image_id = nil
		local function callback(returned_image_id)
			jobs -= 1
			if returned_image_id ~= nil and returned_image_id > 0 then
				image_id = returned_image_id
			end
		end
		coroutine.wrap(GetImageIdAsImageAsync)(asset_id, callback)
		coroutine.wrap(GetImageIdAsDecalAsync)(asset_id, callback)
		while jobs > 0 and image_id == nil do
			RunService.Heartbeat:Wait()
		end
		return image_id
	end
	return nil
end

return ImageIdFetcher