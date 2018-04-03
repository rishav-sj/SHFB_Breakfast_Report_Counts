import csv

NUM_SCHOOL_DAYS_PER_YEAR = 180
PERCENT_MULTIPLYING_FACTOR = 100

f = open('frpmcondensed.csv')
g = open('mealscondensed.csv')
h = open('frpmmealscondensed.csv', 'w')

csv_f = csv.reader(f)
csv_g = csv.reader(g)

frpmMap = {}
mealsMap = {}

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

h.write('County, School District, Total Students, Free Eligible, RP Eligible, Paid Eligible, Total Free Breakfasts, Total RP Breakfasts, Total Paid Breakfasts, Total Free Lunches, Total RP Lunches, Total Paid Lunches, FRPM Eligible Percentage, FRPM Breakfast %, FRPM Lunch %, Total Reimbursement, Lost FRPM Dollars, Lost Meals, FRPM Breakfast/Lunch\n')

for key in frpmMap:
	frpmRow = frpmMap[key]
	mealsRow = mealsMap[key]

	county = frpmRow[0]
	schoolDistrictName = frpmRow[1]
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

	frpmEligiblePercent = PERCENT_MULTIPLYING_FACTOR * (freeEligible + rpEligible)/totalStudents
	frpmBreakfastServedPercent = PERCENT_MULTIPLYING_FACTOR * (freeBreakfasts + rpBreakfasts)/((freeEligible + rpEligible) * NUM_SCHOOL_DAYS_PER_YEAR)
	frpmLunchServedPercent = PERCENT_MULTIPLYING_FACTOR * (freeLunches + rpLunches)/((freeEligible + rpEligible) * NUM_SCHOOL_DAYS_PER_YEAR)

	# Source for Reimbursement Info: https://www.cde.ca.gov/ls/nu/rs/rates1516.asp
	# Expressed here as California reimbursement + Federal reimbursement

	isSevereNeedSchool = frpmEligiblePercent >= 0.6
	isEspeciallyNeedy = frpmEligiblePercent >= 0.4

	freeBreakfastReimbursementRate = (0.2271) + (1.99 if isEspeciallyNeedy else 1.66)
	rpBreakfastReimbursementRate = (0.2271) + (1.69 if isEspeciallyNeedy else 1.36)
	paidBreakfastReimbursementRate = (0) + (0.29)

	freeLunchReimbursementRate = (0.2271) + (3.09 if isSevereNeedSchool else 3.07)
	rpLunchReimbursementRate = (0.2271) + (2.69 if isSevereNeedSchool else 2.67)
	paidLunchReimbursementRate = (0) + (0.31 if isSevereNeedSchool else 0.29)

	totalReimbursement = (freeBreakfastReimbursementRate * freeBreakfasts) + (rpBreakfastReimbursementRate * rpBreakfasts) + (paidBreakfastReimbursementRate * paidBreakfasts) + (freeLunchReimbursementRate * freeLunches) + (rpLunchReimbursementRate * rpLunches) + (paidLunchReimbursementRate * paidLunches)

	totalReimbursementIfServedSameAmountOfBreakfastsAsLunches = (freeBreakfastReimbursementRate * freeLunches) + (rpBreakfastReimbursementRate * rpLunches) + (paidBreakfastReimbursementRate * paidLunches) + (freeLunchReimbursementRate * freeLunches) + (rpLunchReimbursementRate * rpLunches) + (paidLunchReimbursementRate * paidLunches)

	lostFRPMDollars = max(0, (totalReimbursementIfServedSameAmountOfBreakfastsAsLunches - totalReimbursement))

	lostMeals = max(0, (freeLunches - freeBreakfasts) + (rpLunches - rpBreakfasts) + (paidLunches - paidBreakfasts))

	frpmBreafastOverLunch = PERCENT_MULTIPLYING_FACTOR * (freeBreakfasts + rpBreakfasts)/(freeLunches + rpLunches)

	h.write(frpmRow[0] + "," + frpmRow[1] + "," + frpmRow[2] + "," + frpmRow[3] + "," + frpmRow[4] + "," + frpmRow[5] + ",")
	h.write(mealsRow[2] + "," + mealsRow[3] + "," + mealsRow[4] + "," + mealsRow[5] + "," + mealsRow[6] + "," + mealsRow[7] + ",")
	h.write(str(frpmEligiblePercent) + "," + str(frpmBreakfastServedPercent) + "," + str(frpmLunchServedPercent) + "," + str(totalReimbursement) + "," + str(lostFRPMDollars) + "," + str(lostMeals) + "," + str(frpmBreafastOverLunch))
	h.write('\n')


h.close()
f.close()
g.close()