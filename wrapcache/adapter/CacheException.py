#-*-coding: utf-8 -*-
'''
Cache Exceptions
'''

class CacheTimeoutException(Exception):
	def __init__(self, value):
		self.value = value
		
	def __str__(self):
		return repr(self.value)

class DBNotSetException(Exception):
	def __init__(self, value):
		self.value = value
		
	def __str__(self):
		return repr(self.value)