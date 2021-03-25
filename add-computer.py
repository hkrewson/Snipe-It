import subprocess, snipeit, json, osquery
from snipeit import Assets, Models, Company, Manufacturers

server = 'http://snipeit'
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMmY4Nzc0MGZkNjAyYmIwNDJmOThlZDNlMjc1MWE1NDMxY2IxOWVjMTA2Y2I2ZjljNjdhMDc0ZDQwNmU2YTdmYmVkMzAzZTAzNjFiYjljZmIiLCJpYXQiOjE2MTM1MDcxMjQsIm5iZiI6MTYxMzUwNzEyNCwiZXhwIjoyODc1ODExMTI0LCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.am4GoSndlt0MUcm0xnFmXJiRwoIm3hidzGB4IWnKHgIDNKQoSUvYaSDYnWsK6a-MVa2wPDEau4QgMTnYDyeynibb6WdeCWUGDUTVaA1b3WjeCb-yAC4X9ueOl0-Q354ePO5D5PQIIEr1MkorzKDj0I-Qw0TW81dR6RXIi2CWIRElhp2FL5tIPrQLz72tN4bRFlueHxzxitxcHBlMr7QgZs6j_VIcj_v6t1p0AoRAQoT5n1vy2nbHs29BHBTYzLbBmFT82itTJZq0y5jRjz6ZBOZqXlJ5BxDhIzP-zaaJpqsAsYArBokWwEN2ZiYUlY8j5tIyUhPqmfIi9BOg2MrYGjFM1Wm_HT_OzYpBx8X2N9asTAyO5W_2nFv1jJPLe17ttXOaFeTBilfuRNXZVIiEBOQ-R9oNPkeBWJ-Otw4l1qbYJ-WoWT6m6Tt7k6hLiajeH71-gLwn-hGQU5VfAt-OTyoaZCCmZc3lz0lsfNqRYGiwBkYVvCUnzxPPNqOGNrc0FnicP1fP1IBoX3sA_JJd6CSTFb5TSY1GE-S4eTrXlpYtgE0LJ1pOSxHuZV1t8E5zDr7bXsb-Ma0ppvo6fnY_hCTDT0Dnu2BwlXzxjMVPN-kvkYlycc-fsHb_4u3Pfwu9_8jp-MD8MwoetIJGCLXViCndX3379APN3kNFoStOuJE'
Asset = Assets()

'''
Gather Hardware info from System Profiler

'_name', 'activation_lock_status', 'boot_rom_version', 'cpu_type', 'current_processor_speed', 'l2_cache_core', 'l3_cache', 'machine_model', 'machine_name', 'number_processors', 'packages', 'physical_memory', 'platform_cpu_htt', 'platform_UUID', 'provisioning_UDID', 'serial_number'
'''
sysProfiler = subprocess.Popen(['system_profiler', 'SPHardwareDataType', '-json'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
outSP, errSP = sysProfiler.communicate()

currentHardware = json.loads(outSP)

serialNum = currentHardware["SPHardwareDataType"][0]['serial_number']
assetTag = serialNum
modelID = currentHardware["SPHardwareDataType"][0]['machine_model']
processorName = currentHardware["SPHardwareDataType"][0]['cpu_type']
processorSpeed = currentHardware["SPHardwareDataType"][0]['current_processor_speed']

# Get Model ID
Model = Models()
modelLookup = Model.search(server, token, keyword=modelID)
modelLookup = json.loads(modelLookup)
if modelLookup['rows'] == []:
	Manufacturer = Manufacturers()
	devMan = Manufacturer.get(server, token)
	for id in devMan['rows']:
		for key in id:
			if (id[key] == 'Apple Inc'):
				devManID = id['id']
	deviceName = currentHardware["SPHardwareDataType"][0]['machine_name']
	payload = json.dumps({'name': deviceName, 'model_number': modelID, 'fieldset': {'id': 1}, 'manufacturer': {'id': devManID } })
	response = Model.create(server, token, payload)
else:
	modelLookup = modelLookup['rows'][0]['id']

# Get Company ID
Company = Company()
getCompany = Company.get(server, token)
getCompany = json.loads(getCompany)

for id in getCompany['rows']:
	for key in id:
		if (id[key] == 'kArt'):
			companyID = id['id']

# Set up for pushing Asset info.
assetExists = Asset.search(server, token, keyword=serialNum)
if assetExists['rows'] == []:
	payload = json.dumps({'company_id': 1, 'asset_tag': assetTag ,'status_id':1,'model_id': modelLookup, 'serial': serialNum })
	response = Asset.create(server, token, payload)

