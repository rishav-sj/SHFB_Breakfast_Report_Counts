import csv

FRPM_DATA_FILE_NAME='frpm1617.csv'
EXPECTED_SIZE_OF_ROW=28

class SchoolDistrictFRPMData:

	def __init__(self, schoolDistrictName, schoolDistrictCode, totalFreeEligibleStudents, totalReducedPriceEligibleStudents, totalStudents, county):
		self.schoolDistrictName = schoolDistrictName
		self.schoolDistrictCode = schoolDistrictCode
		self.totalFreeEligibleStudents = totalFreeEligibleStudents
		self.totalReducedPriceEligibleStudents = totalReducedPriceEligibleStudents
		self.totalStudents = totalStudents
		self.county = county

	def __str__(self):
		if (self.totalStudents == 0):
			return 'No Students'

		freeEligibleStr = str(self.totalFreeEligibleStudents)
		reducedPriceStr = str(self.totalReducedPriceEligibleStudents)
		totalStudentsStr = str(self.totalStudents)

		return self.schoolDistrictName + "," + self.county + "," + totalStudentsStr + "," + freeEligibleStr + "," + reducedPriceStr

class FRPMDataParser:

	def longify(self, number):
		condensedNumberStr = number.replace(',','')
		if not(condensedNumberStr):
			return long(0)
		return long(condensedNumberStr)

	def addToDict(self, key, someDictionary, valueToAdd):
		if (not(key in someDictionary)):
			someDictionary[key] = []
		someDictionary[key].append(valueToAdd)

	def condense(self, FRPMData):
		schoolDistrictToFRPMMap = {}
		for school in FRPMData:
			self.addToDict(school.schoolDistrictName, schoolDistrictToFRPMMap, school)
		condensedList = []
		for schoolDistrictName in schoolDistrictToFRPMMap:
			schoolDistrictCode = 0
			totalFreeEligibleStudents = 0
			totalReducedPriceEligibleStudents = 0
			totalStudents = 0
			county = ''

			for schoolDistrictData in schoolDistrictToFRPMMap[schoolDistrictName]:
				schoolDistrictCode = schoolDistrictData.schoolDistrictCode
				totalFreeEligibleStudents = totalFreeEligibleStudents + schoolDistrictData.totalFreeEligibleStudents
				totalReducedPriceEligibleStudents = totalReducedPriceEligibleStudents + schoolDistrictData.totalReducedPriceEligibleStudents
				totalStudents = totalStudents + schoolDistrictData.totalStudents
				county = schoolDistrictData.county

			condensedList.append(SchoolDistrictFRPMData(schoolDistrictName, schoolDistrictCode, totalFreeEligibleStudents, totalReducedPriceEligibleStudents, totalStudents, county))

		return condensedList

	def parseRow(self, row):
		assert len(row) == EXPECTED_SIZE_OF_ROW

		county = row[4]
		schoolDistrictName = row[5]
		schoolDistrictCode = self.longify(row[2])
		totalStudents = self.longify(row[17]) + self.longify(row[22])
		totalFreeEligibleStudents = self.longify(row[18]) + self.longify(row[23])
		totalFRPMStudents = self.longify(row[20]) + self.longify(row[25])
		totalReducedPriceEligibleStudents = totalFRPMStudents - totalFreeEligibleStudents
		return SchoolDistrictFRPMData(schoolDistrictName, schoolDistrictCode, totalFreeEligibleStudents, totalReducedPriceEligibleStudents, totalStudents, county)

	def addToDict(self, key, someDictionary, valueToAdd):
		if (not(key in someDictionary)):
			someDictionary[key] = []
		someDictionary[key].append(valueToAdd)

	def parseData(self):
		FRPMData = []
		file = open(FRPM_DATA_FILE_NAME)
		fileCsvReader = csv.reader(file)
		isHeaderRow = True
		for row in fileCsvReader:
			if (not(isHeaderRow)):
				schoolDistrictFRPMData = self.parseRow(row)
				FRPMData.append(schoolDistrictFRPMData)
			else:
				isHeaderRow = False
		return self.condense(FRPMData)