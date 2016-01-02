# -*- coding: utf-8 -*-
__version__ = '1.0.1'
__license__ = 'MIT'

import time
import hashlib
import pickle
from functools import wraps

'''
wrapcache: wrap cache

A python Function / Method OUTPUT cache system base on function Decorators.

Auto cache the Funtion OUTPUT for sometime.
'''

_memory_cache = {} # store cache in Memory

def _is_timeout(cache, timeout):
	'''
	whether cache is timeout?
	'''
	if timeout == -1: #never cahce
		return True
	return time.time() - cache.get('time', 0) > timeout

def _wrap_key(function, args, kws):
	'''
	get the key from the function input.
	'''
	return hashlib.md5(pickle.dumps((function.__name__, args, kws))).hexdigest()

def get(function, *args, **kws):
	'''
	Programmatic get the cache value.
	'''
	return _memory_cache.get(_wrap_key(function, args, kws), {}).get('value', None)

def remove(function, *args, **kws):
	'''
	Programmatic remove the cache.
	'''
	return _memory_cache.pop(_wrap_key(function, args, kws), {}).get('value', None)


def wrapcache(timeout = -1, cache = 'memory'):
	'''
	the Decorator to cache Function.
	'''
	def _wrapcache(function):
		@wraps(function)
		def __wrapcache(*args, **kws):
			hash_key = _wrap_key(function, args, kws)
			if cache == 'memory':
				#memory cache
				if hash_key in _memory_cache:
					if not _is_timeout(_memory_cache[hash_key], timeout):
						return _memory_cache[hash_key].get('value', None)

				# no cache or cache timeout, exec function, and cache the function ouput
				result = function(*args, **kws)
				#cache the output into memory
				_memory_cache[hash_key] = {
					'value' : result,
					'time'  : time.time()
				}
			else:
				# cache type is not valid, do not cache.
				result = function(*args, **kws)
			return result
		return __wrapcache
	return _wrapcache
