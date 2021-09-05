class StaticSiteUpdater:
	def __init__(self):
		#optional argument for passing in live data when instantiated???
		self.livedata = {}

	#accepts either key and value as string or 
	#file can be either a single file as string or a list of strings
	#key and value can be individual strings or can I pass in a dict?
	def findReplace(self,files, key, value):


