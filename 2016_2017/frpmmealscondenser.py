import csv


def removeWordDistrict(someName):
	return someName.replace(' School District', '')

def removeWhitespaces(someString):
	return someString.lstrip().rstrip().replace('\xef\xbb\xbf','')

def getSchoolDaysMap():
	schoolDaysMap = {}

	m = open('Input/schooldays.csv')
	csv_m = csv.reader(m)

	for row in csv_m:
		if (len(row) == 2 and (row[1])):
			schoolDistrictName = row[0]
			schoolDistrictName = removeWhitespaces(removeWordDistrict(schoolDistrictName))
			schoolDaysMap[schoolDistrictName] = int(row[1])

	m.close()
	return schoolDaysMap


PERCENT_MULTIPLYING_FACTOR = 100

f = open('Output/frpmcondensed.csv')
g = open('Output/mealscondensed.csv')
h = open('Output/frpmmealscondensed.csv', 'w')

csv_f = csv.reader(f)
csv_g = csv.reader(g)

frpmMap = {}
mealsMap = {}
schoolDaysMap = getSchoolDaysMap()

rowNum = 0
for row in csv_f:
	if (rowNum != 0):
		schoolDistrictName = row[1]
		frpmMap[schoolDistrictName] = row
	rowNum = rowNum + 1

rowNum = 0
for row in csv_g:
	if (rowNum != 0):
		schoolDistrictName = row[1]
		mealsMap[schoolDistrictName] = row
	rowNum = rowNum + 1

for key in mealsMap:
	if (not(key in frpmMap)):
		print 'Key not in frpmMap but in mealsMap:' + key

for key in frpmMap:
	if (not(key in mealsMap)):
		print 'Key not in mealsMap but in frpmMap:' + key

h.write('County, School District, Total Students, Free Eligible, RP Eligible, Paid Eligible, Total Free Breakfasts, Total RP Breakfasts, Total Paid Breakfasts, Total Free Lunches, Total RP Lunches, Total Paid Lunches, FRPM Eligible Percentage, FRPM Breakfast %, FRPM Lunch %, Total Breakfast Reimbursement, Total Lunch Reimbursement, Total Reimbursement, Lost FRPM Dollars, Lost Meals, FRPM Breakfast/Lunch\n')

for key in frpmMap:
	frpmRow = frpmMap[key]
	mealsRow = mealsMap[key]

	county = frpmRow[0]
	schoolDistrictName = removeWhitespaces(frpmRow[1])
	totalStudents = long(frpmRow[2])
	freeEligible = long(frpmRow[3])
	rpEligible = long(frpmRow[4])
	paidEligible = long(frpmRow[5])

	freeBreakfasts = long(mealsRow[2])
	rpBreakfasts = long(mealsRow[3])
	paidBreakfasts = long(mealsRow[4])

	freeLunches = long(mealsRow[5])
	rpLunches = long(mealsRow[6])
	paidLunches = long(mealsRow[7])

	if (not (schoolDistrictName in schoolDaysMap)):
		print 'No entry for school district with name ' + schoolDistrictName

	numSchoolDaysPerYear = schoolDaysMap[schoolDistrictName]

	frpmEligiblePercent = PERCENT_MULTIPLYING_FACTOR * (freeEligible + rpEligible)/totalStudents
	frpmBreakfastServedPercent = PERCENT_MULTIPLYING_FACTOR * (freeBreakfasts + rpBreakfasts)/((freeEligible + rpEligible) * numSchoolDaysPerYear)
	frpmLunchServedPercent = PERCENT_MULTIPLYING_FACTOR * (freeLunches + rpLunches)/((freeEligible + rpEligible) * numSchoolDaysPerYear)

	# Source for Reimbursement Info: https://www.cde.ca.gov/ls/nu/rs/rates1516.asp
	# Expressed here as California reimbursement + Federal reimbursement

	isSevereNeedSchool = frpmEligiblePercent >= 0.6
	isEspeciallyNeedy = frpmEligiblePercent >= 0.4

	freeBreakfastReimbursementRate = (0.2271) + (2.04 if isEspeciallyNeedy else 1.71)
	rpBreakfastReimbursementRate = (0.2271) + (1.74 if isEspeciallyNeedy else 1.41)
	paidBreakfastReimbursementRate = (0) + (0.29)

	freeLunchReimbursementRate = (0.2271) + (3.18 if isSevereNeedSchool else 3.16)
	rpLunchReimbursementRate = (0.2271) + (2.78 if isSevereNeedSchool else 2.76)
	paidLunchReimbursementRate = (0) + (0.32 if isSevereNeedSchool else 0.30)


	totalBreakfastReimbursement = (freeBreakfastReimbursementRate * freeBreakfasts) + (rpBreakfastReimbursementRate * rpBreakfasts) + (paidBreakfastReimbursementRate * paidBreakfasts)
	totalLunchReimbursement = (freeLunchReimbursementRate * freeLunches) + (rpLunchReimbursementRate * rpLunches) + (paidLunchReimbursementRate * paidLunches)
	totalReimbursement =  totalBreakfastReimbursement + totalLunchReimbursement

	totalReimbursementIfServedSameAmountOfBreakfastsAsLunches = (freeBreakfastReimbursementRate * freeLunches) + (rpBreakfastReimbursementRate * rpLunches) + (paidBreakfastReimbursementRate * paidLunches) + (freeLunchReimbursementRate * freeLunches) + (rpLunchReimbursementRate * rpLunches) + (paidLunchReimbursementRate * paidLunches)

	lostFRPMDollars = max(0, (totalReimbursementIfServedSameAmountOfBreakfastsAsLunches - totalReimbursement))

	lostMeals = max(0, (freeLunches - freeBreakfasts) + (rpLunches - rpBreakfasts) + (paidLunches - paidBreakfasts))

	frpmBreafastOverLunch = PERCENT_MULTIPLYING_FACTOR * (freeBreakfasts + rpBreakfasts)/(freeLunches + rpLunches)

	h.write(frpmRow[0] + "," + frpmRow[1] + "," + frpmRow[2] + "," + frpmRow[3] + "," + frpmRow[4] + "," + frpmRow[5] + ",")
	h.write(mealsRow[2] + "," + mealsRow[3] + "," + mealsRow[4] + "," + mealsRow[5] + "," + mealsRow[6] + "," + mealsRow[7] + ",")
	h.write(str(frpmEligiblePercent) + "," + str(frpmBreakfastServedPercent) + "," + str(frpmLunchServedPercent) + "," + str(totalBreakfastReimbursement) + "," + str(totalLunchReimbursement) + "," + str(totalReimbursement) + "," + str(lostFRPMDollars) + "," + str(lostMeals) + "," + str(frpmBreafastOverLunch))
	h.write('\n')


h.close()
f.close()
g.close()