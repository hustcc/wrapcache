#-*-coding: utf-8 -*-
'''
CacheTimeoutException
'''

class CacheTimeoutException(Exception):
	def __init__(self, value):
		self.value = value
		
	def __str__(self):
		return repr(self.value)