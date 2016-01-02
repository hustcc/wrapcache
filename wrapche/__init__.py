# -*- coding: utf-8 -*-
__version__ = '0.1'
__license__ = 'MIT'

import time
import hashlib
import pickle
from functools import wraps

'''
wrapche: wraps cache

A Function / Method OUTPUT cache system base on function Decorators.

Auto cache the Funtion OUTPUT for something.
'''

_memory_cache = {} # store cache in Memory

CACHE_TYPE = ['memory', 'redis', 'file']

def _is_timeout(cache, timeout):
	'''
	whether cache is timeout?
	'''
	if timeout == -1: #never cahce
		return True
	return time.time() - cache.get('time', 0) > timeout

def _hash_string(s):
	'''
	get the md5 of s, use this to generate the cache key.
	'''
	return hashlib.md5(s).hexdigest()


def _dump_key(function, args, kw):
	'''
	TODO: get the key from the function input.
	'''
	return pickle.dumps((function.func_name, args, kw))

def wrapche(cache = 'memory', timeout = -1):
	'''
	the Decorator to cache Function.
	'''
	def _wrapche(function):
		@wraps(function) # 自动复制函数信息
		def __wrapche(*args, **kw):
			hash_key = _hash_string(_dump_key(function, args, kw))
			if cache == 'memory':
				#memory cache
				if hash_key in _memory_cache:
					if not _is_timeout(_memory_cache[hash_key], timeout):
						return _memory_cache[hash_key].get('value', None)

				# no cache or cache timeout, exec function, and cache the function ouput
				result = function(*args, **kw)
				#cache the output into memory
				_memory_cache[hash_key] = {
					'value' : result,
					'time'  : time.time()
				}
			elif cache == 'redis':
				#TODO
				# no cache or cache timeout, exec function, and cache the function ouput
				result = function(*args, **kw)
			elif cache == 'file':
				#TODO
				# no cache or cache timeout, exec function, and cache the function ouput
				result = function(*args, **kw)
			else:
				# cache type is not valid, do not cache.
				result = function(*args, **kw)
			return result
		return __wrapche
	return _wrapche
