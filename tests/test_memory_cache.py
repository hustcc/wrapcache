#-*-coding: utf-8 -*-
import sys
sys.path.append(".")
sys.path.append("..")
import wrapcache

from time import sleep
import random

'''
test memory cache
'''

@wrapcache.wrapcache(timeout = 3)
def need_cache_function(i, t = 2, o = 3):
	sleep(2)
	return random.randint(1, 100) + i

if __name__ == "__main__":
	print('##start test memory cache...')
	for i in range(10):
		sleep(1)
		print(need_cache_function(1, t = 2, o = 3))
	print('##end test memory cache...')

	print('##test Programmatic get value.')
	print('get key exist: ', wrapcache.get(wrapcache.keyof(need_cache_function, 1, o = 3, t = 2)))
	print('get key not exist: ', wrapcache.get(wrapcache.keyof(need_cache_function, 2, o = 3, t = 2)))

	print('##test Programmatic rm value.')
	print('remove key exist: ', wrapcache.remove(wrapcache.keyof(need_cache_function, 1, o = 3, t = 2)))
	print('remove key exist: ', wrapcache.remove(wrapcache.keyof(need_cache_function, 1, o = 3, t = 2)))
	print('remove key not exist: ', wrapcache.remove(wrapcache.keyof(need_cache_function, 2, o = 3, t = 2)))
