import csv

def removeWordDistrict(someName):
	return someName.replace(' School District', '')

def removeWhitespaces(someString):
	return someString.lstrip().rstrip().replace('\xef\xbb\xbf','')


f = open('frpmmealscondensed.csv')
g = open('schooldays.csv')
csv_f = csv.reader(f)
csv_g = csv.reader(g)


schoolDaysMap = {}
for mapping in csv_g:
	if (len(mapping) == 2 and (mapping[1])):
		schoolDistrictName = mapping[0]
		schoolDistrictName = removeWhitespaces(removeWordDistrict(schoolDistrictName))
		schoolDaysMap[schoolDistrictName] = int(mapping[1])

rowNum = 0
totalStudents = 0
freeEligibleTotal = 0
rpEligibleTotal = 0
frpBreakfastPotential = 0
frpBreakfastTotal = 0
frpLunchPotential = 0
frpLunchTotal = 0
for row in csv_f:
	if (rowNum != 0):
		countyNameStr = row[0]
		if (countyNameStr == 'Santa Clara'):
			totalStudents = totalStudents + int(row[2])
			freeEligible = int(row[3])
			freeEligibleTotal = freeEligibleTotal + freeEligible
			rpEligible = int(row[4])
			rpEligibleTotal = rpEligibleTotal + rpEligible
			schoolDistrictName = row[1].rstrip()
			schoolDays = schoolDaysMap[schoolDistrictName]
			frpPotential = (schoolDays * (freeEligible + rpEligible))
			frpBreakfastPotential = frpBreakfastPotential + frpPotential
			frpLunchPotential = frpLunchPotential + frpPotential
			freeBreakfast = int(row[6])
			RPBreakfast = int(row[7])
			frpBreakfast = freeBreakfast + RPBreakfast
			frpBreakfastTotal = frpBreakfastTotal + frpBreakfast

			freeLunch = int(row[9])
			RPLunch = int(row[10])
			frpLunch = freeLunch + RPLunch
			frpLunchTotal = frpLunchTotal + frpLunch
			print schoolDistrictName
			frpBreakfastParticipationHere = 100 *(float(frpBreakfast) / float(frpPotential))
			frpLunchParticipationHere = 100 * (float(frpLunch) / float(frpPotential))
			print frpBreakfastParticipationHere
			print frpLunchParticipationHere

	rowNum = rowNum + 1

frpEligibleTotal = freeEligibleTotal + rpEligibleTotal
frpEligiblePercent = 100 * (float(frpEligibleTotal) / float(totalStudents))
frpBreakfastParticipation = 100 *(float(frpBreakfastTotal) / float(frpBreakfastPotential))
frpLunchParticipation = 100 * (float(frpLunchTotal) / float(frpLunchPotential))
print 'Total Students: ' + str(totalStudents)
print 'Free Eligible: ' + str(freeEligibleTotal)
print 'RP Eligible: ' + str(rpEligibleTotal)
print 'FRP Eligible: ' + str(frpEligibleTotal)
print 'FRP Eligible(%): ' + str(frpEligiblePercent)
print 'FRP Breakfast Participation: ' + str(frpBreakfastParticipation)
print 'FRP Lunch Participation: ' + str(frpLunchParticipation)