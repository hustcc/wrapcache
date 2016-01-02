# -*- coding: utf-8 -*-
__version__ = '1.0.1'
__license__ = 'MIT'

import time
import sys
import hashlib
import pickle
from functools import wraps
from adapter.CacheException import CacheTimeoutException
from adapter.MemoryAdapter import MemoryAdapter

'''
wrapcache: wrap cache

A python Function / Method OUTPUT cache system base on function Decorators.

Auto cache the Funtion OUTPUT for sometime.
'''

def _wrap_key(function, args, kws):
	'''
	get the key from the function input.
	'''
	return hashlib.md5(pickle.dumps((function.__name__, args, kws))).hexdigest()

def keyof(function, *args, **kws):
	'''
	get the function cache key
	'''
	return _wrap_key(function, args, kws)

def get(key, adapter = MemoryAdapter):
	'''
	get the cache value
	'''
	adapter_instance = adapter(timeout = sys.maxint)
	try:
		return adapter_instance.get(key)
	except CacheTimeoutException, _:
		return None

def remove(key, adapter = MemoryAdapter):
	'''
	remove cache by key 
	'''
	adapter_instance = adapter()
	return adapter_instance.remove(key)

def set(key, value, timeout = -1, adapter = MemoryAdapter):
	'''
	set cache by code, must set timeout length
	'''
	adapter_instance = adapter(timeout = timeout)
	return adapter_instance.set(key, value)

def flush(adapter = MemoryAdapter):
	'''
	clear all the caches
	'''
	adapter_instance = adapter()
	return adapter_instance.flush()


def wrapcache(timeout = -1, adapter = MemoryAdapter):
	'''
	the Decorator to cache Function.
	'''
	def _wrapcache(function):
		@wraps(function)
		def __wrapcache(*args, **kws):
			hash_key = _wrap_key(function, args, kws)
			adapter_instance = adapter(timeout = timeout)
			try:
				return adapter_instance.get(hash_key)
			except CacheTimeoutException, _:
				#timeout
				value = function(*args, **kws)
				adapter_instance.set(hash_key, value)
				return value
		return __wrapcache
	return _wrapcache