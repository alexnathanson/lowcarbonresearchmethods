from SimpleStaticSiteUpdater import StaticSiteUpdater

src = "/home/pi/local/www/templates"
dst = "home/pi/local/www"

SS = StaticSiteUpdater(src, dst)

SS.findReplaceEntireDirectory(SS.srcDirectory)