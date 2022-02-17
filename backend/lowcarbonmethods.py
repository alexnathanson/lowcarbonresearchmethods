import datetime
from SimpleStaticSiteGenerator import StaticSiteGenerator
import requests
import json
from keys import *


src = "/home/pi/local/www/templates"
dst = "/home/pi/local/www/"

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
	battPercentage = str(round(100.0 * float(getRequest(getServer + "/api/v1/chargecontroller.php?value=battery-percentage")),2)) + "%"
	battBar = battPercentage
except:
	battPercentage = "error"
	battBar = "0%"


localTime = datetime.datetime.today().strftime("%I:%M %p")
localDate = datetime.datetime.today().strftime("%m/%d/%y")

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
	"%%logo-bg%%" : "#F5D14E" ,
	"%%body-bg%%" : "#B3A8A8",#BDB3B3
	"%%local-bg%%": "#624884",
	"%%nav-bg%%" : "#312442",
	"%%bat-bg%%" : "#B5A3CC",
	"%%bat-bar%%": "black",
	"%%content-bg%%": "#D3E8E8",
	"%%data-bg%%" : "grey",
	"%%header-bg%%" : "#312442",
	"%%logo-src%%" : "assets/logos/logo_black_on_clear.png",
	"%%local-text%%" : "white"
}

dayTheme = {
	"%%logo-bg%%" : "#321F32" ,
	"%%body-bg%%" : "#D8F3FD",
	"%%local-bg%%": "#FBE289",
	"%%nav-bg%%" : "#6E6235",
	"%%bat-bg%%" : "#EBCC5C",
	"%%bat-bar%%": "black",
	"%%content-bg%%": "#D3E8E8",
	"%%data-bg%%" : "grey",
	"%%header-bg%%" : "#FBE289",
	"%%logo-src%%" : "assets/logos/logo_white_on_clear.png",
	"%%local-text%%" : "black"
}

swapDictionary = { 
	"%%TIME%%": localTime,
	"%%DATE%%": localDate,
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

	#avoid zero division error

	if len(collectVals) == 0:
		avgPVPower.append(0)
	else:
		avgPVPower.append(sum(collectVals)/len(collectVals))
	
	#avgPVPower.append(sum(collectVals)/len(collectVals))	

#scale the average power data to get a percentage
#the default module size is 50 watts. if the server has a different sized module it will be scaled appropriately
moduleSize = 50 * float(getRequest(getServer + "/api/v1/chargecontroller.php?systemInfo=wattage-scaler"))

# NOTE: in the future the background graph could be mapped so whatever the range of numbers is is visually larger on the page (currently hardcoded to 600px)
powerPercentage = [str(100.0 * (p / moduleSize)) + "%" for p in avgPVPower]


#add average power to the dictionary
for p in range(len(avgPVPower)):
	if avgPVPower[p] >= 0.1:
		swapDictionary['%%avgP'+ str(24 - p) + '%%'] = str(round(avgPVPower[p],1)) + 'W'
	else:
		swapDictionary['%%avgP'+ str(24 - p) + '%%'] = ''

swapDictionary['%%graphMaxPixels%%'] = str(600.0 * (max(avgPVPower) / moduleSize))

#add average power percentage to the dictionary
for p in range(len(powerPercentage)):
	swapDictionary['%%'+ str(24 - p) + 'H%%'] = powerPercentage[p]

if 	float(getRequest(getServer + "/api/v1/chargecontroller.php?value=PV-power-L")) <= 0.0 :
	swapDictionary.update(nightTheme)
else:
	swapDictionary.update(dayTheme)

print(swapDictionary)

SS = StaticSiteGenerator(src, dst, swapDictionary)

SS.findReplaceEntireDirectory(SS.srcDirectory)


