# wrapcache

A python Function / Method OUTPUT cache system base on function Decorators.

[![Build Status](https://travis-ci.org/hustcc/wrapcache.svg)](https://travis-ci.org/hustcc/wrapcache)

Source code: [https://github.com/hustcc/wrapcache](https://github.com/hustcc/wrapcache)


## What's wrapcache?

`wrapcache` is a decorator that enables caching of return values for functions.

The cache keys are dependent completely on the arguments passed to the function. very simple to use. 

Also has some `API` to `Programmatic` get cache or remove cache.

Here's an example of how you might use wrapcache:

```python

import wrapcache

from time import sleep
import random

@wrapcache.wrapcache(timeout = 3)
def need_cache_function(input, t = 2, o = 3):
    sleep(2)
    return random.randint(1, 100)

if __name__ == "__main__":
	for i in range(10):
		sleep(1)
		print(need_cache_function(1, t = 2, o = 3))
	
	#get cache Programmatic
	print(wrapcache.get(need_cache_function, 1, o = 3, t = 2))
	#remove cache Programmatic
	print(wrapcache.remove(need_cache_function, 1, o = 3, t = 2))

```


## How to install?

### 1. Use tool install

 - `easy_install wrapcache`
 
or

 -  `pip install wrapcache` / `pip3 install wrapcache`

### 2. Download to install

 - Download from [https://pypi.python.org/pypi/wrapcache/](https://pypi.python.org/pypi/wrapcache/), and run `python setup.py install`.

### 3. Manual installation

 - Manual installation: Put `wrapcache` folder into current directory or `site-packages`, then `import wrapcache` to use.


## TODO

 - add redis and memcache supported.
 - more test case.