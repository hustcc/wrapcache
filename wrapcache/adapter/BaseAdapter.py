#-*-coding: utf-8 -*-
'''
Base cache Adapter object.
'''

class BaseAdapter(object):
	db = None
	def __init__(self, timeout = -1):
		self.timeout = timeout

	def get(self, key):
		raise NotImplementedError()

	def set(self, key, value):
		raise NotImplementedError()

	def remove(self, key):
		raise NotImplementedError()

	def flush(self):
		raise NotImplementedError()