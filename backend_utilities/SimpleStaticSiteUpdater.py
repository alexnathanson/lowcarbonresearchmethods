import os


class StaticSiteUpdater:
	def __init__(self, aSrcDirectory, aDstDirectory):
		self.srcDirectory = aSrcDirectory
		self.dstDirectory = aDstDirectory
		# a dictionary of placeholder: replacement pairs
		self.swapList = {}

	#accepts either key and value as string or 
	#file can be either a single file as string or a list of strings
	#key and value can be individual strings or can I pass in a dict?
	def findReplace(self,inputString, swapDict, fileName):
		for placeholder, replacement in self.swapDict:
			inputString.replace(placeholder,replacement)
		saveFile(inputString, )

	#load in data from config file
	def readFile(self, aFile):
		print('loading file ' + aFile)
		#load file
		try:
			with open(aFile, r) as f:
				fileContents = f.read()
				findReplace(fileContents, self.swapList, aFile)
				f.close()
				
		except:
			print('Error reading file ' + aFile)

	def saveFile(self, fileContents, dstFileName):


	#recursively gets all files from dirctory including subdirectory
	def findReplaceEntireDirectory(self, aDirectory):
		for (root, dirs, file) in os.walk(aDirectory):
		    for f in file:
		        readFile(f)