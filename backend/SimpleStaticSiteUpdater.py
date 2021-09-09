import os
import errno

class StaticSiteUpdater:
	def __init__(self, aSrcDirectory, aDstDirectory, swapDict):
		self.srcDirectory = aSrcDirectory
		self.dstDirectory = aDstDirectory
		# a dictionary of placeholder: replacement pairs
		self.swapDict = swapDict


	#recursively gets all files from dirctory including subdirectory
	#passes files to readFile()
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


	#reads in text from files
	#passes contents to findReplace()
	def readFile(self, aFile):
		print('loading file ' + aFile)
		#load file
		try:
			with open(aFile) as f:
				fileContents = f.read()
				self.findReplace(fileContents, self.swapDict, aFile)
				f.close()
				
		except:
			print('Error reading file ' + aFile)

	#replaces strings from swapList dictionary and sends the output to saveFile()
	#swapList is a dictionary
	#key and value can be individual strings or can I pass in a dict?
	def findReplace(self,inputString, swapPairs, srcFileName):

		for placeholder, replacement in swapPairs.items():
			inputString = inputString.replace(str(placeholder), str(replacement))
		self.saveFile(inputString, srcFileName)


	#writes the file to the specified destination
	def saveFile(self, fileContents, srcFileName):
		# swap out the src file path for the dst file path
		dstFileName = srcFileName.replace(self.srcDirectory, self.dstDirectory)
		print(dstFileName)

		#make new directory if needed
		if not os.path.exists(os.path.dirname(dstFileName)):
		    try:
		        os.makedirs(os.path.dirname(dstFileName))
		    except OSError as exc: # Guard against race condition
		        if exc.errno != errno.EEXIST:
		            raise

		try:
			with open(dstFileName, "w") as f:
				f.write(fileContents)
				f.close()
				
		except:
			print('Error writing file ' + dstFileName)


	