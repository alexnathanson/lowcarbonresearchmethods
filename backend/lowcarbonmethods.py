from SimpleStaticSiteUpdater import StaticSiteUpdater

#src = "/home/pi/local/www/templates"
src = "D:/LowCarbonMethods/templates"
dst = "home/pi/local/www"

battPercentage = 0
weatherToday = "sunny"
weatherTomorrow = "cloudy"

swapDictionary = { 
	"%%BATTERY%%": battPercentage,
	"%%W_TODAY%%": weatherToday,
	"%%W_TOMORROW%%": weatherTomorrow
	}

SS = StaticSiteUpdater(src, dst, swapDictionary)

SS.findReplaceEntireDirectory(SS.srcDirectory)