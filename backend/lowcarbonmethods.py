import datetime
from SimpleStaticSiteUpdater import StaticSiteUpdater
#from CC import ChargeControllerData
import requests
import json

src = "/home/pi/local/www/lowcarbonresearchmethods/templates"
#src = "D:/LowCarbonMethods/templates"
dst = "/home/pi/local/www/lowcarbonresearchmethods"

# CC = ChargeControllerData("/home/pi/solar-protocol/charge-controller/data/tracerData"+ str(datetime.date.today()) +".csv")

getServer = "http://localhost"
#getServer = "http://www.solarprotocol.net"

def getRequest(url):
	try:			
		response = requests.get(url)
		return response.text	
	except requests.exceptions.HTTPError as err:
		print(err)
	except requests.exceptions.Timeout as err:
		print(err)
	except:
		print(err)

battPercentage = 100 * float(getRequest(getServer + "/api/v1/chargecontroller.php?value=battery-percentage"))

if battPercentage != 'None':
	battPercentage = str(battPercentage) + "%"
	battBar = battPercentage
else:
	battPercentage = "error"
	battBar = "0%"

localTime = datetime.datetime.today().strftime("%I:%M %p")

weatherToday = "unknown"
weatherTomorrow = "unknown"

# nightTheme = {
	
# }

# dayTheme = {
	
# }

swapDictionary = { 
	"%%TIME%%": localTime,
	"%%BATTERY%%": battPercentage,
	"%%BATTERY_BAR%%": battBar,
	"%%WEATHER_TODAY%%": weatherToday,
	"%%WEATHER_TOMORROW%%": weatherTomorrow
	}

#print(swapDictionary)

#retrieve past 2 calendar days work of PV power data
PVpower = json.loads(getRequest(getServer + "/api/v1/chargecontroller.php?value=PV-power-L&duration=2"))

#remove the header so it can be sorted
PVpower.pop("datetime")

powerKeys = list(PVpower.keys())

#sort keys
powerKeys.sort(key = lambda date: datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f"), reverse = True)

#average PV power data by hour for the last 24 hours
avgPVPower = []

for h in range(24):
	collectVals = []

	tdMin = datetime.datetime.strptime(powerKeys[0], "%Y-%m-%d %H:%M:%S.%f") - datetime.timedelta(hours=h)
	tdMax = datetime.datetime.strptime(powerKeys[0], "%Y-%m-%d %H:%M:%S.%f") - datetime.timedelta(hours=h + 1)
	#print(str(tdMax) + " : " + str(tdMin))

	for ts in powerKeys:
		#convert powerKeys to datetime
		pkDT = datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")

		#check if the value falls within the specified range
		if  pkDT < tdMin and pkDT > tdMax:
			collectVals.append(PVpower[ts])
	#cast all to floats
	collectVals = list(map(float, collectVals))

	avgPVPower.append(sum(collectVals)/len(collectVals))	

#scale the average power data to get a percentage

#the default module size is 50 watts. if the server has a different sized module it will be scaled appropriately
moduleSize = 50 * float(getRequest(getServer + "/api/v1/chargecontroller.php?systemInfo=wattage-scaler"))

powerPercentage = [str(100.0 * (p / moduleSize)) + "%" for p in avgPVPower]

#add these average power stats to the dictionary
for p in range(len(powerPercentage)):
	swapDictionary['%%'+ str(p + 1) + 'H%%'] = powerPercentage[p]

print(swapDictionary)

SS = StaticSiteUpdater(src, dst, swapDictionary)

SS.findReplaceEntireDirectory(SS.srcDirectory)


