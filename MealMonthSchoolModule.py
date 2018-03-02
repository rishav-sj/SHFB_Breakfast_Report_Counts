class MealMonthSchool:

	def __init__(self, county, programGroupYear, fnsReportDate, order, programCode, name, cdsCode, siteName, mealTypeCode, mealsServedFree, mealsServedReducedPrice, mealsServedPaid, mealsServedTotal):
		self.county = county
		self.programGroupYear = programGroupYear
		self.fnsReportDate = fnsReportDate
		self.order = order
		self.programCode = programCode
		self.name = name # Name of the school district
		self.cdsCode = cdsCode
		self.siteName = siteName # Name of a specific school
		self.mealTypeCode = mealTypeCode
		self.mealsServedFree = mealsServedFree
		self.mealsServedReducedPrice = mealsServedReducedPrice
		self.mealsServedPaid = mealsServedPaid
		self.mealsServedTotal = mealsServedTotal

	def __str__(self):
		return "{" + "County: " + self.county + ", " + "FNSReportDate: " + self.fnsReportDate + ", " + "PrgramCode: " + self.programCode + ", " + "SiteName: " + self.siteName + "}"

	def uniqueSiteName(self):
		# Complete site name (includes the name of the district)
		# e.g. "Union Elementary School District - NODDIN ELEMENTARY"
		return self.name + " - " + self.siteName
