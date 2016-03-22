# -*- coding: utf-8 -*-
__version__ = '1.0.8'
__license__ = 'MIT'

import time
import sys
import hashlib
try:
	import cPickle as pickle
except:
	import pickle
from functools import wraps
from wrapcache.adapter.CacheException import CacheExpiredException
from wrapcache.adapter.MemoryAdapter import MemoryAdapter

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
	try:
		return pickle.loads(adapter().get(key))
	except CacheExpiredException:
		return None

def remove(key, adapter = MemoryAdapter):
	'''
	remove cache by key 
	'''
	return pickle.loads(adapter().remove(key))

def set(key, value, timeout = -1, adapter = MemoryAdapter):
	'''
	set cache by code, must set timeout length
	'''
	if adapter(timeout = timeout).set(key, pickle.dumps(value)):
		return value
	else:
		return None

def flush(adapter = MemoryAdapter):
	'''
	clear all the caches
	'''
	return adapter().flush()


def wrapcache(timeout = -1, adapter = MemoryAdapter):
	'''
	the Decorator to cache Function.
	'''
	def _wrapcache(function):
		@wraps(function)
		def __wrapcache(*args, **kws):
			hash_key = _wrap_key(function, args, kws)
			try:
				adapter_instance = adapter()
				return pickle.loads(adapter_instance.get(hash_key))
			except CacheExpiredException:
				#timeout
				value = function(*args, **kws)
				set(hash_key, value, timeout, adapter)
				return value
		return __wrapcache
	return _wrapcache