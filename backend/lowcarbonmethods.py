import datetime
from SimpleStaticSiteGenerator import StaticSiteGenerator
import requests
import json
from keys import *

src = "/home/pi/local/www/lowcarbonresearchmethods/templates"
dst = "/home/pi/local/www/lowcarbonresearchmethods"

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

try:
	battPercentage = str(100 * float(getRequest(getServer + "/api/v1/chargecontroller.php?value=battery-percentage"))) + "%"
	battBar = battPercentage
except:
	battPercentage = "error"
	battBar = "0%"


localTime = datetime.datetime.today().strftime("%I:%M %p")


# weatherToday = json.loads(getRequest("http://api.openweathermap.org/data/2.5/weather?q=Toronto&appid="+ openweatherapi))
# print(weatherToday['weather'][0]['description'])

# weatherTomorrow = json.loads(getRequest("http://api.openweathermap.org/data/2.5/forecast/daily?q=Toronto&appid="+ openweatherapi))
# print(weatherTomorrow)

TrenteLat = "44.35949686052928"
TrenteLong = "-78.28909175456307"
weather = json.loads(getRequest("https://api.openweathermap.org/data/2.5/onecall?lat=" + TrenteLat +"&lon=" + TrenteLong + "&exclude=minutely,hourly,alerts&appid=" + openweatherapi))
weatherToday = weather['current']['weather'][0]['description']

#CONFIRM THAT POSITION 0 IS TOMORROW!!!
weatherTomorrow = weather['daily'][0]['weather'][0]['description']

nightTheme = {
	"%%logo-bg%%" : "black" ,
	"%%body-bg%%" : "#D6D6D6",
	"%%local-bg%%": "#82E6E8",
	"%%nav-bg%%" : "#516666",
	"%%bat-bg%%" : "lightgray",
	"%%bat-bar%%": "#04BCBF",
	"%%content-bg%%": "#D3E8E8",
	"%%data-bg%%" : "grey",
	"%%header-bg%%" : "black"
}

dayTheme = {
	"%%logo-bg%%" : "black" ,
	"%%body-bg%%" : "#B0E7FC",
	"%%local-bg%%": "#E3FC80",
	"%%nav-bg%%" : "#71861D",
	"%%bat-bg%%" : "#D3E87D", #should I set opacity low?
	"%%bat-bar%%": "#B8CC66",
	"%%content-bg%%": "#D3E8E8",
	"%%data-bg%%" : "grey",
	"%%header-bg%%" : "black"
}

swapDictionary = { 
	"%%TIME%%": localTime,
	"%%BATTERY%%": battPercentage,
	"%%BATTERY_BAR%%": battBar,
	"%%WEATHER_TODAY%%": weatherToday,
	"%%WEATHER_TOMORROW%%": weatherTomorrow
	}

'''GET PV MODULE POWER PRODUCTION HISTORY'''
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

# NOTE: in the future the background graph could be mapped so whatever the range of numbers is is visually larger on the page

powerPercentage = [str(100.0 * (p / moduleSize)) + "%" for p in avgPVPower]

#add these average power stats to the dictionary
for p in range(len(powerPercentage)):
	swapDictionary['%%'+ str(24 - (p + 1)) + 'H%%'] = powerPercentage[p]

if 	float(getRequest(getServer + "/api/v1/chargecontroller.php?value=PV-power-L")) <= 0.0 :
	swapDictionary.update(nightTheme)
else:
	swapDictionary.update(dayTheme)

print(swapDictionary)

SS = StaticSiteGenerator(src, dst, swapDictionary)

SS.findReplaceEntireDirectory(SS.srcDirectory)


