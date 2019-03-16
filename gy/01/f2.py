#!/usr/bin/python
# -*- coding: UTF-8 -*-

# F2
# A hét napjait jelöljük 0-6-ig (Hétfő,...,Vasárnap).
# Írjunk egy függvényt, ami megadja mikor kell kelnünk az adott napon
# (hétköznap ’7:00’ hétvégén ’10:00’),
# kivéve ha vakációzunk, mert akkor
# hétköznap ’10:00’ hétvégén ’OFF’
# alarm_clock(1, False) → '7:00'
# alarm_clock(6, False) → '10:00'
# alarm_clock(0, True) → '10:00‚
# alarm_clock(6, True) → ’OFF'


# def alarm_clock(d,v):
	# if d >= 0 or d <= 4:
		# if v:
			# return '10:00'
		# else:
			# return '7:00'
	# elif d == 5 or d == 6:
		# if v:
			# return 'OFF'
		# else:
			# return '10:00'

def alarm_clock(d,v):
	try:
		retValue = '10:00'
		if (d < 6) and (v == False):
			retValue = '7:00'
		elif (d > 5) and (v == True):
			retValue = 'OFF'
		return retValue
	except TypeError:
		print "Error: day is not integer or vacation is not boolean"

print alarm_clock(1, False),
print alarm_clock(6, False)
print alarm_clock(0, True)
print alarm_clock(6, True)