import csv
from MealMonthSchoolModule import MealMonthSchool

DATA_FILE_NAME='San_Mateo_Santa_Clara_Meals.csv'
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

	def parseData(self):
		mealMonthSchools = []
		file = open(DATA_FILE_NAME)
		fileCsvReader = csv.reader(file)
		isHeaderRow = True
		for row in fileCsvReader:
			if (not(isHeaderRow)):
				mealMonthSchools.append(self.parseRow(row))
			else:
				isHeaderRow = False
		return mealMonthSchools

print DataParser().parseData()