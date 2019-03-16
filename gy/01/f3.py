#!/usr/bin/python
# -*- coding: UTF-8 -*-

# F3
# Írjunk függvényt ami megadja az n. fibonacci
# számot
# fibonacci(0) -> 0
# fibonacci(1) -> 1
# fibonacci(2) -> 1
# fibonacci(3) -> 2
# ...
# fibonacci(n) -> fibonacci(n-2) + fibonacci(n-1)

# def fibonacci(n):
	# try:
		# retValue = 0
		# if n == 0:
			# retValue == 0
		# if n == 1 or n == 2:
			# retValue = 1
		# if n > 2:
			# retValue
		# return retValue
	# except TypeError:
		# print "Error: n is not integer"

def fibonacci(n):
	try:
		retValue = 0
		if n > 1:
			retValue = fibonacci(n - 2) + fibonacci(n - 1)
		return retValue
	except TypeError:
		print "Error: n is not integer"

print fibonacci(0) # 0
print fibonacci(1) # 1
print fibonacci(2) # 1
print fibonacci(3) # 2