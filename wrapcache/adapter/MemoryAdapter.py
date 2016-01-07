#-*-coding: utf-8 -*-
'''
Memory Adapter object.
'''
import time
from wrapcache.adapter.BaseAdapter import BaseAdapter
from wrapcache.adapter.CacheException import CacheTimeoutException


class MemoryAdapter(BaseAdapter):
	'''
	use for memory cache
	'''
	def __init__(self, timeout = -1):
		super(MemoryAdapter, self).__init__(timeout = timeout)
		if not MemoryAdapter.db:
			MemoryAdapter.db = {}

	def get(self, key):
		cache = MemoryAdapter.db.get(key, {})
		if time.time() - cache.get('time', 0) > 0:
			self.remove(key) #timeout, rm key, reduce memory
			raise CacheTimeoutException(key)
		else:
			return cache.get('value', None)

	def set(self, key, value):
		cache = {
			'value' : value,
			'time'  : time.time() + self.timeout
		}
		MemoryAdapter.db[key] = cache
		return value

	def remove(self, key):
		return MemoryAdapter.db.pop(key, {}).get('value', None)

	def flush(self):
		MemoryAdapter.db = {}
		return True