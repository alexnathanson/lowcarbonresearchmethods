import os


class StaticSiteUpdater:
	def __init__(self, aSrcDirectory, aDstDirectory, swapDict):
		self.srcDirectory = aSrcDirectory
		self.dstDirectory = aDstDirectory
		# a dictionary of placeholder: replacement pairs
		self.swapDict = {}

	#accepts either key and value as string or 
	#file can be either a single file as string or a list of strings
	#key and value can be individual strings or can I pass in a dict?
	def findReplace(self,inputString, swapList, fileName):
		for placeholder, replacement in self.swapDict:
			inputString.replace(placeholder,replacement)
		saveFile(inputString, )

	#load in data from config file
	def readFile(self, aFile):
		print('loading file ' + aFile)
		#load file
		try:
			with open(aFile) as f:
				fileContents = f.read()
				#findReplace(fileContents, self.swapDict, aFile)
				f.close()
				
		except:
			print('Error reading file ' + aFile)

	def saveFile(self, fileContents, dstFileName):
		#save this file!
		print(dstFileName)

	#recursively gets all files from dirctory including subdirectory
	def findReplaceEntireDirectory(self, aDirectory):
		for (root, dirs, file) in os.walk(aDirectory):
			# print(root)
			# print(dirs)
			# print(file)
		    for f in file:
			    #print(root + "/" + f)
			    fullPath = root + "/" + f
			    fullPath = fullPath.replace("\\","/")
			    self.readFile(fullPath)