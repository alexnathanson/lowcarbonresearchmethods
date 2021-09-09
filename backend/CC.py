import requests

class ChargeControllerData:
	def __init__(self, fP):
		self.filePath = fP

	#this should be added to class
	def localData(self, chosenDataValue):

		csvArray = []

		#get the local PV data
		with open(self.filePath, mode='r') as csvfile:
			localPVData = csv.reader(csvfile)

			for row in localPVData:
			 	csvArray.append(row)

			#print(csvArray)

			#loop through headers to determine position of value needed
			for v in range(len(csvArray[0])):
				if csvArray[0][v] == chosenDataValue:
					return csvArray[-1][v]


	def getRequest(self, url):
		try:			
			response = requests.get(url, timeout = 5)
			print(response.text)		
		except requests.exceptions.HTTPError as err:
			print(err)
		except requests.exceptions.Timeout as err:
			print(err)
		except:
			print(err)