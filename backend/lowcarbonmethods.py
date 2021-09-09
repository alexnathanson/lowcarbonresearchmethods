#from datetime import datetime
import datetime
from SimpleStaticSiteUpdater import StaticSiteUpdater
from CC import ChargeControllerData

src = "/home/pi/local/www/lowcarbonresearchmethods/templates"
#src = "D:/LowCarbonMethods/templates"
dst = "/home/pi/local/www/lowcarbonresearchmethods/output"

CC = ChargeControllerData("/home/pi/solar-protocol/charge-controller/data/tracerData"+ str(datetime.date.today()) +".csv")

battPercentage = "0%"
weatherToday = "unknown"
weatherTomorrow = "unknown"
localTime = datetime.datetime.today().strftime("%I:%M %p")

# nightTheme = {
	
# }

# dayTheme = {
	
# }

swapDictionary = { 
	"%%TIME%%": localTime,
	#"%%BATTERY%%": CC.localData("battery percentage"),
	"%%BATTERY%%": CC.getRequest("http://localhost/api/v1/?value=battery-percentage")
	"%%WEATHER_TODAY%%": weatherToday,
	"%%WEATHER_TOMORROW%%": weatherTomorrow
	}

PVtime = []
for h in range(24):
	PVtime.append("%%" + str(h+1) + "%%")

print(PVtime)


print(CC.getRequest("http://localhost/api/v1/?value=PV-power-L&duration=2"))

# PVhist = zip(PVtime,)


SS = StaticSiteUpdater(src, dst, swapDictionary)

SS.findReplaceEntireDirectory(SS.srcDirectory)

#SS.readFile(SS.)