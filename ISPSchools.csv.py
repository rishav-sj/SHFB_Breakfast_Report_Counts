from FRPMDataParserModule import FRPMDataParser

finalList = FRPMDataParser().parseData()
for elem in finalList:
	print str(elem)