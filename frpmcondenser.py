import csv

ignoreList = ['Lakeside Joint', 'Hillsborough City Elementary', 'Loma Prieta Joint Union Elementary', 'Los Altos Elementary', 'Los Gatos-Saratoga Joint Union High', 'Las Lomitas Elementary']


specialSchoolsMap = {}

# ACE Charter Schools
specialSchoolsMap['ACE Charter High'] = 'ACE Charter School'
specialSchoolsMap['ACE Empower Academy'] = 'ACE Charter School'
specialSchoolsMap['ACE Inspire Academy'] = 'ACE Charter School'
specialSchoolsMap['ACE Franklin McKinley'] = 'ACE Charter School'

# Alpha Public Schools
specialSchoolsMap['Cornerstone Academy Preparatory'] = 'Alpha Public Schools Inc'
specialSchoolsMap['Alpha: Blanca Alvarado Middle'] = 'Alpha Public Schools Inc'
specialSchoolsMap['Alpha: Jose Hernandez Middle'] = 'Alpha Public Schools Inc'
specialSchoolsMap['Alpha Cindy Avitia High'] = 'Alpha Public Schools Inc'

# Rocketship Education
specialSchoolsMap['Rocketship Alma Academy'] = 'Rocketship Education'
specialSchoolsMap['Rocketship Academy Brilliant Minds'] = 'Rocketship Education'
specialSchoolsMap['Rocketship Discovery Prep'] = 'Rocketship Education'
specialSchoolsMap['Rocketship Fuerza Community Prep'] = 'Rocketship Education'
specialSchoolsMap['Rocketship Los Suenos Academy'] = 'Rocketship Education'
specialSchoolsMap['Rocketship Mateo Sheedy Elementary'] = 'Rocketship Education'
specialSchoolsMap['Rocketship Mosaic Elementary'] = 'Rocketship Education'
specialSchoolsMap['Rocketship Rising Stars'] = 'Rocketship Education'
specialSchoolsMap['Rocketship Si Se Puede Academy'] = 'Rocketship Education'
specialSchoolsMap['Rocketship Spark Academy'] = 'Rocketship Education'


# Summit Public Schools
specialSchoolsMap['Everest Public High'] = 'Summit Public Schools'
specialSchoolsMap['Summit Preparatory Charter High'] = 'Summit Public Schools'
specialSchoolsMap['Summit Public School: Shasta'] = 'Summit Public Schools'

schoolDistrictNameToTotalEnrollmentMap = {}
schoolDistrictNameToFreeEligibleMap = {}
schoolDistrictNameToReducedPriceEligibleMap = {}
schoolDistrictNameToPaidEligibleMap = {}
schoolDistrictNameToCountyMap = {}

f = open('frpm1617.csv')
g = open('frpmcondensed.csv', 'w')
csv_f = csv.reader(f)
rowNum = 0

def isEligibleCounty(countyName):
	return (countyName == 'San Mateo') or (countyName == 'Santa Clara')


for row in csv_f:
  if (rowNum != 0):
  	countyName = row[4]
  	schoolDistrictName = row[5]
  	schoolName = row[6]
  	if (isEligibleCounty(countyName) and not(schoolDistrictName in ignoreList)):
  		if (not(schoolDistrictName in schoolDistrictNameToTotalEnrollmentMap)):
  			# Initialize maps for this school district
  			schoolDistrictNameToCountyMap[schoolDistrictName] = countyName
  			schoolDistrictNameToTotalEnrollmentMap[schoolDistrictName] = 0
  			schoolDistrictNameToFreeEligibleMap[schoolDistrictName] = 0
  			schoolDistrictNameToReducedPriceEligibleMap[schoolDistrictName] = 0
  			schoolDistrictNameToPaidEligibleMap[schoolDistrictName] = 0
  		totalEnrollment = long(row[17])
  		freeEligible = long(row[18])
  		FRPMEligible = long(row[20])
  		RPEligible = FRPMEligible - freeEligible
  		paidEligible = totalEnrollment - FRPMEligible

  		schoolDistrictNameToTotalEnrollmentMap[schoolDistrictName] = schoolDistrictNameToTotalEnrollmentMap[schoolDistrictName]  + totalEnrollment
  		schoolDistrictNameToFreeEligibleMap[schoolDistrictName] = schoolDistrictNameToFreeEligibleMap[schoolDistrictName] + freeEligible
  		schoolDistrictNameToReducedPriceEligibleMap[schoolDistrictName] = schoolDistrictNameToReducedPriceEligibleMap[schoolDistrictName] + RPEligible
  		schoolDistrictNameToPaidEligibleMap[schoolDistrictName] = schoolDistrictNameToPaidEligibleMap[schoolDistrictName] + paidEligible

  		if (schoolName in  specialSchoolsMap):
  			# Repeat calculations with this special mapping
  			schoolDistrictName = specialSchoolsMap[schoolName]
  			if (not(schoolDistrictName in schoolDistrictNameToTotalEnrollmentMap)):
	  			# Initialize maps for this school district
	  			schoolDistrictNameToCountyMap[schoolDistrictName] = countyName
	  			schoolDistrictNameToTotalEnrollmentMap[schoolDistrictName] = 0
	  			schoolDistrictNameToFreeEligibleMap[schoolDistrictName] = 0
	  			schoolDistrictNameToReducedPriceEligibleMap[schoolDistrictName] = 0
	  			schoolDistrictNameToPaidEligibleMap[schoolDistrictName] = 0
	  		schoolDistrictNameToTotalEnrollmentMap[schoolDistrictName] = schoolDistrictNameToTotalEnrollmentMap[schoolDistrictName]  + totalEnrollment
	  		schoolDistrictNameToFreeEligibleMap[schoolDistrictName] = schoolDistrictNameToFreeEligibleMap[schoolDistrictName] + freeEligible
	  		schoolDistrictNameToReducedPriceEligibleMap[schoolDistrictName] = schoolDistrictNameToReducedPriceEligibleMap[schoolDistrictName] + RPEligible
	  		schoolDistrictNameToPaidEligibleMap[schoolDistrictName] = schoolDistrictNameToPaidEligibleMap[schoolDistrictName] + paidEligible

  rowNum = rowNum + 1

g.write('County, School District Name, Total Enrollment, Free Eligible, Reduced Price Eligible, Paid Eligible\n')
for key in schoolDistrictNameToTotalEnrollmentMap:
	# Printing county, schoolDistrictName, total, free, RP
	g.write(schoolDistrictNameToCountyMap[key] + "," + key + "," + str(schoolDistrictNameToTotalEnrollmentMap[key]) + "," + str(schoolDistrictNameToFreeEligibleMap[key]) + "," + str(schoolDistrictNameToReducedPriceEligibleMap[key]) + "," + str(schoolDistrictNameToPaidEligibleMap[key]) + '\n')

f.close()
g.close()