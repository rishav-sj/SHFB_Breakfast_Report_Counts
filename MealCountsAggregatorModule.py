from DataParserModule import DataParser


class AggregatedMealsSchoolDistrict:

	def __init__(self, schoolDistrictName, totalFreeBreakfasts, totalReducedPriceBreakfasts, totalFreeLunches, totalReducedPriceLunches, county):
		self.schoolDistrictName = schoolDistrictName
		self.totalFreeBreakfasts = totalFreeBreakfasts
		self.totalReducedPriceBreakfasts = totalReducedPriceBreakfasts
		self.totalFreeLunches = totalFreeLunches
		self.totalReducedPriceLunches = totalReducedPriceLunches
		self.county = county

	def __str__(self):
		return "{" + self.county + " " + self.schoolDistrictName + ": BREAKFASTS(" + str(self.totalFreeBreakfasts) + "," + str(self.totalReducedPriceBreakfasts) + "), LUNCHES(" + str(self.totalFreeLunches) + "," + str(self.totalReducedPriceLunches) + ")}"



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

	def aggregateMealCounts(self):
		schoolDistrictToCountyMap, siteNameDictionary, schoolDistrictNameDictionary, mealMonthSchools = DataParser().parseData()
		aggregatedMealsSchoolDistricts = []
		for schoolDistrictName in schoolDistrictNameDictionary:
			mealMonthSchools = schoolDistrictNameDictionary[schoolDistrictName]
			fnsReportDateMap = self.buildFnsReportDateMap(mealMonthSchools)
			totalFreeBreakfasts = 0
			totalReducedPriceBreakfasts = 0
			totalFreeLunches = 0
			totalReducedPriceLunches = 0
			for fnsReportDate in fnsReportDateMap:
				relevantMealMonthSchools = fnsReportDateMap.get(fnsReportDate)
				totalFreeBreakfasts = totalFreeBreakfasts + self.totalFreeBreakfasts(relevantMealMonthSchools)
				totalReducedPriceBreakfasts = totalReducedPriceBreakfasts + self.totalReducedPriceBreakfasts(relevantMealMonthSchools)
				totalFreeLunches = totalFreeLunches + self.totalFreeLunches(relevantMealMonthSchools)
				totalReducedPriceLunches = totalReducedPriceLunches + self.totalReducedPriceLunches(relevantMealMonthSchools)
			aggregatedMealsSchoolDistrict = AggregatedMealsSchoolDistrict(schoolDistrictName, totalFreeBreakfasts, totalReducedPriceBreakfasts, totalFreeLunches, totalReducedPriceLunches, schoolDistrictToCountyMap[schoolDistrictName])
			aggregatedMealsSchoolDistricts.append(aggregatedMealsSchoolDistrict)
		return aggregatedMealsSchoolDistricts


#print len(MealCountsAggregator().aggregateMealCounts())