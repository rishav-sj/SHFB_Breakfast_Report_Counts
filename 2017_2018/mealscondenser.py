import csv

oldIgnoreList = ['Across the Bridge Foundation', 'ALL SOULS CHURCH SCHOOL', 'Cristo Rey San Jose High School', 'Design Tech High', 'EE S Residential Group Home Inc.', 'Escuela Popular', 'Escuela Xochitl Tonatiul', 'JT Residential Care Facilities', 'Latino College Prep Academy', 'Navigator Schools', 'Sacred Heart Nativity School', 'SAN MATEO CO JUV HALL SCHS', 'SANTA CLARA CO PROBATION', 'South Valley Charter School', 'St Andrew Residential Programs for Youth (STAR HOUSE)', 'ST ELIZABETH SETON SCHOOL', 'ST PATRICK ELEM CATHOLIC', 'Unity Care Group Inc.', 'Voices College-Bound Language', 'REBEKAH CHILDRENS SERVICES']
newIgnoreList = ['ST SIMONS CATHOLIC SCHOOL', 'Coalition for Better Schools Inc.', 'SAN FRANCISCO YMCA CAMP', 'ST NICHOLAS SCHOOL', 'Oxford Day Academy Inc.', 'BING NURSERY SCHOOL', 'ST MARTIN OF TOURS ELEM CATH', 'Loma Prieta Joint Union Elementary School District']

# Breakfast counts
schoolDistrictToFreeBreakfastsMap = {}
schoolDistrictToRPBreakfastsMap = {}
schoolDistrictToPaidBreakfastsMap = {}


# Lunch Counts
schoolDistrictToFreeLunchesMap = {}
schoolDistrictToRPLunchesMap = {}
schoolDistrictToPaidLunchesMap = {}

schoolDistrictToCountyNameMap = {}


f = open('Input/meals.csv')
g = open('Output/mealscondensed.csv', 'w')
csv_f = csv.reader(f)

def isBreakfast(mealType):
    return ('BREAKFAST' in mealType) and not('SSFO' in mealType);

def isLunch(mealType):
    return ('LUNCH' in mealType) and not('SSFO' in mealType);

def isEligibleCounty(countyName):
    return (countyName == 'SAN MATEO') or (countyName == 'SANTA CLARA')

def removeCommas(somestring):
    return somestring.replace(',', '')

def readNumber(entry):
    if (entry):
        return long(removeCommas(entry))
    return 0
def mapCountyNameToCamelCase(countyName):
    if (countyName == 'SAN MATEO'):
      return 'San Mateo'
    elif (countyName == 'SANTA CLARA'):
      return 'Santa Clara'
    else:
      return countyName

def cleanupSchoolDistrictName(schoolDistrictName):
    if ('School District' in schoolDistrictName):
        schoolDistrictName = schoolDistrictName.replace(' School District', '')

    if (schoolDistrictName == 'GILROY UNIFIED SCHOOL DISTRICT'):
        schoolDistrictName = 'Gilroy Unified'
    if (schoolDistrictName == 'SANTA CLARA COE'):
        schoolDistrictName = 'Santa Clara County Office of Education'
    if (schoolDistrictName == 'MORELAND SCHOOL DISTRICT'):
        schoolDistrictName = 'Moreland'
    if (schoolDistrictName == 'LUTHER BURBANK SCHOOL DISTRICT'):
        schoolDistrictName = 'Luther Burbank'
    if (schoolDistrictName == 'PACIFICA SCHOOL DISTRICT'):
        schoolDistrictName = 'Pacifica'
    return schoolDistrictName

rowNum = 0
ignoreList = oldIgnoreList + newIgnoreList
for row in csv_f:
  if (rowNum != 0):
    countyName = row[0]
    schoolDistrictName = removeCommas(row[4])
    if (isEligibleCounty(countyName) and (not(schoolDistrictName in ignoreList))):
      mealType = row[6]
      schoolDistrictName = cleanupSchoolDistrictName(schoolDistrictName)
      if (not(schoolDistrictName in schoolDistrictToFreeBreakfastsMap)):
        schoolDistrictToFreeBreakfastsMap[schoolDistrictName] = 0
        schoolDistrictToRPBreakfastsMap[schoolDistrictName] = 0
        schoolDistrictToPaidBreakfastsMap[schoolDistrictName] = 0

        schoolDistrictToFreeLunchesMap[schoolDistrictName] = 0
        schoolDistrictToRPLunchesMap[schoolDistrictName] = 0
        schoolDistrictToPaidLunchesMap[schoolDistrictName] = 0

        schoolDistrictToCountyNameMap[schoolDistrictName] = mapCountyNameToCamelCase(countyName)
      if (isBreakfast(mealType)):
        schoolDistrictToFreeBreakfastsMap[schoolDistrictName] = schoolDistrictToFreeBreakfastsMap[schoolDistrictName] + readNumber(row[7])
        schoolDistrictToRPBreakfastsMap[schoolDistrictName] = schoolDistrictToRPBreakfastsMap[schoolDistrictName] + readNumber(row[8])
        schoolDistrictToPaidBreakfastsMap[schoolDistrictName] = schoolDistrictToPaidBreakfastsMap[schoolDistrictName] + readNumber(row[9])

      if (isLunch(mealType)):
        schoolDistrictToFreeLunchesMap[schoolDistrictName] = schoolDistrictToFreeLunchesMap[schoolDistrictName] + readNumber(row[7])
        schoolDistrictToRPLunchesMap[schoolDistrictName] = schoolDistrictToRPLunchesMap[schoolDistrictName] + readNumber(row[8])
        schoolDistrictToPaidLunchesMap[schoolDistrictName] = schoolDistrictToPaidLunchesMap[schoolDistrictName] + readNumber(row[9])

  rowNum = rowNum + 1


g.write('County, School District, Free Breakfasts, RP Breakfasts, Paid Breakfasts, Free Lunches, RP Lunches, Paid Lunches\n');

for key in schoolDistrictToFreeBreakfastsMap:
    strToWrite = schoolDistrictToCountyNameMap[key] + "," + key + "," + str(schoolDistrictToFreeBreakfastsMap[key]) + "," + str(schoolDistrictToRPBreakfastsMap[key]) + "," + str(schoolDistrictToPaidBreakfastsMap[key]) + "," + str(schoolDistrictToFreeLunchesMap[key]) + "," + str(schoolDistrictToRPLunchesMap[key]) + "," + str(schoolDistrictToPaidLunchesMap[key]) + '\n' 
    g.write(strToWrite)




f.close()
g.close()
