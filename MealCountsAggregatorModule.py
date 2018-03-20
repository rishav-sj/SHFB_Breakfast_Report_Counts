from DataParserModule import DataParser

def removeCommas(someString):
	return someString.replace(',', '')

class AggregatedMealsSchoolDistrict:

	def __init__(self, schoolDistrictName, totalFreeBreakfasts, totalReducedPriceBreakfasts, totalFreeLunches, totalReducedPriceLunches, county, totalPaidBreakfasts, totalPaidLunches):
		self.schoolDistrictName = schoolDistrictName
		self.totalFreeBreakfasts = totalFreeBreakfasts
		self.totalReducedPriceBreakfasts = totalReducedPriceBreakfasts
		self.totalFreeLunches = totalFreeLunches
		self.totalReducedPriceLunches = totalReducedPriceLunches
		self.county = county
		self.totalPaidBreakfasts = totalPaidBreakfasts
		self.totalPaidLunches = totalPaidLunches

	def __str__(self):

		return (removeCommas(self.schoolDistrictName)) + "," + (removeCommas(self.county)) + "," + str(self.totalFreeBreakfasts) + "," + str(self.totalReducedPriceBreakfasts) + "," + str(self.totalPaidBreakfasts) + "," + str(self.totalFreeLunches) + "," + str(self.totalReducedPriceLunches) + "," + str(self.totalPaidLunches)



class MealCountsAggregator:

	def isBreakfast(self, mealMonthSchool):
		return 'BREAKFAST' in mealMonthSchool.mealTypeCode

	def isLunch (self, mealMonthSchool):
		return 'LUNCH' in mealMonthSchool.mealTypeCode

	def isEitherLunchOrBreakfast(self, mealMonthSchool):
		return self.isLunch(mealMonthSchool) or self.isBreakfast(mealMonthSchool)

	def addToDict(self, key, someDictionary, valueToAdd):
		if (not(key in someDictionary)):
			someDictionary[key] = []
		someDictionary[key].append(valueToAdd)

	def buildFnsReportDateMap(self, mealMonthSchools):
		fnsReportDateMap = {}
		for mealMonthSchool in mealMonthSchools:
			assert self.isEitherLunchOrBreakfast(mealMonthSchool)
			self.addToDict(mealMonthSchool.fnsReportDate, fnsReportDateMap, mealMonthSchool)
		return fnsReportDateMap

	def totalFreeBreakfasts(self, mealMonthSchools):
		freeBreakfasts = 0
		for mealMonthSchool in mealMonthSchools:
			if (self.isBreakfast(mealMonthSchool)):
				freeBreakfasts = freeBreakfasts + mealMonthSchool.mealsServedFree
		return freeBreakfasts

	def totalReducedPriceBreakfasts(self, mealMonthSchools):
		reducedPriceBreakfasts = 0
		for mealMonthSchool in mealMonthSchools:
			if (self.isBreakfast(mealMonthSchool)):
				reducedPriceBreakfasts = reducedPriceBreakfasts + mealMonthSchool.mealsServedReducedPrice
		return reducedPriceBreakfasts

	def totalPaidBreakfasts(self, mealMonthSchools):
		paidBreakfasts = 0
		for mealMonthSchool in mealMonthSchools:
			if (self.isBreakfast(mealMonthSchool)):
				paidBreakfasts = paidBreakfasts + mealMonthSchool.mealsServedPaid
		return paidBreakfasts

	def totalFreeLunches(self, mealMonthSchools):
		freeLunches = 0
		for mealMonthSchool in mealMonthSchools:
			if (self.isLunch(mealMonthSchool)):
				freeLunches = freeLunches + mealMonthSchool.mealsServedFree
		return freeLunches

	def totalReducedPriceLunches(self, mealMonthSchools):
		reducedPriceLunches = 0
		for mealMonthSchool in mealMonthSchools:
			if (self.isLunch(mealMonthSchool)):
				reducedPriceLunches = reducedPriceLunches + mealMonthSchool.mealsServedReducedPrice
		return reducedPriceLunches

	def totalPaidLunches(self, mealMonthSchools):
		paidLunches = 0
		for mealMonthSchool in mealMonthSchools:
			if (self.isLunch(mealMonthSchool)):
				paidLunches = paidLunches + mealMonthSchool.mealsServedPaid
		return paidLunches

	def aggregateMealCounts(self):
		schoolDistrictToCountyMap, siteNameDictionary, schoolDistrictNameDictionary, mealMonthSchools = DataParser().parseData()
		aggregatedMealsSchoolDistricts = []
		for schoolDistrictName in schoolDistrictNameDictionary:
			mealMonthSchools = schoolDistrictNameDictionary[schoolDistrictName]
			fnsReportDateMap = self.buildFnsReportDateMap(mealMonthSchools)
			totalFreeBreakfasts = 0
			totalReducedPriceBreakfasts = 0
			totalPaidBreakfasts = 0
			totalFreeLunches = 0
			totalReducedPriceLunches = 0
			totalPaidLunches = 0
			for fnsReportDate in fnsReportDateMap:
				relevantMealMonthSchools = fnsReportDateMap.get(fnsReportDate)
				totalFreeBreakfasts = totalFreeBreakfasts + self.totalFreeBreakfasts(relevantMealMonthSchools)
				totalReducedPriceBreakfasts = totalReducedPriceBreakfasts + self.totalReducedPriceBreakfasts(relevantMealMonthSchools)
				totalPaidBreakfasts = totalPaidBreakfasts + self.totalPaidBreakfasts(relevantMealMonthSchools)

				totalFreeLunches = totalFreeLunches + self.totalFreeLunches(relevantMealMonthSchools)
				totalReducedPriceLunches = totalReducedPriceLunches + self.totalReducedPriceLunches(relevantMealMonthSchools)
				totalPaidLunches = totalPaidLunches + self.totalPaidLunches(relevantMealMonthSchools)

			aggregatedMealsSchoolDistrict = AggregatedMealsSchoolDistrict(schoolDistrictName, totalFreeBreakfasts, totalReducedPriceBreakfasts, totalFreeLunches, totalReducedPriceLunches, schoolDistrictToCountyMap[schoolDistrictName], totalPaidBreakfasts, totalPaidLunches)
			aggregatedMealsSchoolDistricts.append(aggregatedMealsSchoolDistrict)
		return aggregatedMealsSchoolDistricts


#print len(MealCountsAggregator().aggregateMealCounts())