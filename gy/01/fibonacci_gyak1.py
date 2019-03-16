#!/usr/bin/python

def fibonacci(num):
  try:
    retValue = 0
    if num == 1:
      retValue = 1
    elif num > 1:
      retValue = fibonacci(num - 2) + fibonacci(num - 1)
    return retValue
  except TypeError:
    print "Error: num is not integer"

print fibonacci(0) # 0
print fibonacci(1) # 1
print fibonacci(2) # 1
print fibonacci(6) # 8