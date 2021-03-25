import subprocess, snipeit, json
from snipeit import Assets, Models, Company, Manufacturers

server = ''
token = ''
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
	#ManufacturerID is the ID number. First manufacturer created is 1.
	ManufacturerID =  
	deviceName = currentHardware["SPHardwareDataType"][0]['machine_name']
	payload = json.dumps({'name': deviceName, 'model_number': modelID, 'fieldset': {'id': 1}, 'manufacturer': {'id': ManufacturerID } })
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

