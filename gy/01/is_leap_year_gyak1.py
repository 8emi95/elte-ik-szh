#!/usr/bin/python

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