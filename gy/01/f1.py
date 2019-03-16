#!/usr/bin/python
# -*- coding: UTF-8 -*-

# F1
# Írjunk függvényt ami megadja egy bemenetben kapott évszámról, hogy szökőév-e.
# Egy év szökőév, ha osztható néggyel, de akkor nem, ha osztható százzal, hacsak nem osztható négyszázzal.
# Példák: 1992,1996,2000,2400 szökőév, de 1993, 1900 nem.

# import sys
# num = sys.argv[1] # 0. a script neve
# def is_leap_year(num):
#	if (num % 4) != 0 || ((num % 100) == 0 && (num % 400) != 0):
# 		return False
#	else:
#		return True
	
def is_leap_year(num):
	try:
		retValue = True
		if (num % 4) == 0:
			if ((num % 100) == 0) and ((num % 400) != 0):
				retValue = False
		else:
			retValue = False
		return retValue
	except TypeError:
		print "Error: num is not integer"
		
print is_leap_year(1992) # True
print is_leap_year(1993) # False
print is_leap_year(1900) # False
print is_leap_year(2000) # True