from MealCountsAggregatorModule import MealCountsAggregator


def removeCommas(someString):
	return someString.replace(',', '')

aggregatedMealCounts = MealCountsAggregator().aggregateMealCounts()
for elem in aggregatedMealCounts:
	print str(elem)