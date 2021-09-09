from SimpleStaticSiteUpdater import StaticSiteUpdater

src = "/home/pi/local/www/lowcarbonresearchmethods/templates"
#src = "D:/LowCarbonMethods/templates"
dst = "/home/pi/local/www/lowcarbonresearchmethods/output"

battPercentage = "0%"
weatherToday = "sunny"
weatherTomorrow = "cloudy"
localTime = "3pm"

swapDictionary = { 
	"%%TIME%%":localTime,
	"%%BATTERY%%": battPercentage,
	"%%WEATHER_TODAY%%": weatherToday,
	"%%WEATHER_TOMORROW%%": weatherTomorrow
	}

SS = StaticSiteUpdater(src, dst, swapDictionary)

SS.findReplaceEntireDirectory(SS.srcDirectory)