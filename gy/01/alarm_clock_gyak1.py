#!/usr/bin/python

def alarm_clock(day,vacation):
  try:
    retValue = '10:00'
    if (day < 6) and (vacation == False):
      retValue = '7:00'
    elif (day > 5) and (vacation == True):
      retValue = 'OFF'
    return retValue
  except TypeError:
    print "Error: day is not integer or vacation is not boolean"

print alarm_clock(1, False) # '7:00'
print alarm_clock(6, False) # '10:00'
print alarm_clock(0, True) # '10:00'
print alarm_clock(6, True) # 'OFF'