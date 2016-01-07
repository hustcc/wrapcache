#-*-coding: utf-8 -*-

import unittest, time
import sys, random

import wrapcache
from wrapcache.adapter.RedisAdapter import RedisAdapter

@wrapcache.wrapcache(timeout = 3)
def need_mem_cache_function():
	time.sleep(2)
	print('mem cache timeout, new...')
	return random.randint(1, 100)

@wrapcache.wrapcache(timeout = 3, adapter = RedisAdapter)
def need_redis_cache_function():
	time.sleep(2)
	print('redis cache timeout, new...')
	return (random.randint(1, 100), 'Hello wrapcache')


if __name__ =='__main__':

	#set redid db before use.
	import redis
	REDIS_POOL = redis.ConnectionPool(host = '10.246.13.189', port = 6379, password = '', db = 1)
	REDIS_INST = redis.Redis(connection_pool = REDIS_POOL, charset = 'utf8')
	RedisAdapter.db = REDIS_INST
	#redis cache
	for i in range(10):
		time.sleep(1)
		print(need_redis_cache_function()[0])

	#memory cache
	for i in range(10):
		time.sleep(1)
		print(need_mem_cache_function())