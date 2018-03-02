import csv
from MealMonthSchoolModule import MealMonthSchool

DATA_FILE_NAME='San_Mateo_Santa_Clara_Meals_Meals_Served.csv'
EXPECTED_SIZE_OF_ROW=13

class DataParser:

	def longify(self, number):
		condensedNumberStr = number.replace(',','')
		if not(condensedNumberStr):
			return long(0)
		return long(condensedNumberStr)

	def parseRow(self, row):
		assert len(row) == EXPECTED_SIZE_OF_ROW
		county = row[0]
		programGroupYear = row[1]
		fnsReportData = row[2]
		order = row[3]
		programCode = row[4]
		name = row[5]
		cdsCode = row[6]
		siteName = row[7]
		mealTypeCode = row[8]
		mealsServedFree = self.longify(row[9])
		mealsServedReducedPrice = self.longify(row[10])
		mealsServedPaid = self.longify(row[11])
		mealsServedTotal = self.longify(row[12])
		return MealMonthSchool(county, programGroupYear, fnsReportData, order, programGroupYear, name, cdsCode, siteName, mealTypeCode, mealsServedFree, mealsServedReducedPrice, mealsServedPaid, mealsServedTotal)

	def addToDict(self, key, someDictionary, valueToAdd):
		if (not(key in someDictionary)):
			someDictionary[key] = []
		someDictionary[key].append(valueToAdd)

	def parseData(self):
		mealMonthSchools = []
		file = open(DATA_FILE_NAME)
		fileCsvReader = csv.reader(file)
		isHeaderRow = True
		schoolNameDictionary = {}
		siteNameDictionary = {}
		for row in fileCsvReader:
			if (not(isHeaderRow)):
				mealMonthSchool = self.parseRow(row)
				schoolName = mealMonthSchool.name
				siteName = mealMonthSchool.uniqueSiteName()
				self.addToDict(schoolName, schoolNameDictionary, mealMonthSchool)
				self.addToDict(siteName, siteNameDictionary, mealMonthSchool)
				mealMonthSchools.append(mealMonthSchool)
			else:
				isHeaderRow = False
		return siteNameDictionary, schoolNameDictionary, mealMonthSchools

#siteNameDictionary, schoolNameDictionary, mealMonthSchools = DataParser().parseData()


# Unique Meal Type Codes
# NSLP - National School Lunch Program
# 
#set(['SSFO_LUNCH', 'SSFO_BREAKFAST_SEVERENEED', 'NSLP_BREAKFAST', 'NSLP_LUNCH', 'NSLP_BREAKFAST_SEVERENEED'])