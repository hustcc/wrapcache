#-*-coding: utf-8 -*-
import sys
sys.path.append(".")
sys.path.append("../")
from wrapche import wrapche

from time import sleep
import random

'''
test memory cache
'''

@wrapche('memory', 3)
def need_cache_function(input):
    sleep(2)
    return random.randint(1, 100)

if __name__ == "__main__":
	rst = ''
	for i in range(10):
		sleep(1)
		rst = rst + ', ' + str(need_cache_function(2))
	rst = rst[2:]
	print rst