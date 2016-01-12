# wrapcache

一个基于Python装饰器Decorators的方法缓存系统，用于缓存Python方法的输出值，可以支持复杂数据类型，可以缓存到Redis中、Python dict、LUR算法存储中。[English README.md](README.md)

[![Build Status](https://travis-ci.org/hustcc/wrapcache.svg)](https://travis-ci.org/hustcc/wrapcache) [![codecov Status](https://codecov.io/github/hustcc/wrapcache/coverage.svg?branch=master)](https://codecov.io/github/hustcc/wrapcache?branch=master) [![PyPi Status](https://img.shields.io/pypi/v/wrapcache.svg)](https://pypi.python.org/pypi/wrapcache) [![Python Versions](https://img.shields.io/pypi/pyversions/wrapcache.svg)](https://pypi.python.org/pypi/wrapcache) [![PyPi Downloads](https://img.shields.io/pypi/dm/wrapcache.svg)](https://pypi.python.org/pypi/wrapcache)

Github地址: [https://github.com/hustcc/wrapcache](https://github.com/hustcc/wrapcache)

Issue & Bug: [https://github.com/hustcc/wrapcache/issues/new](https://github.com/hustcc/wrapcache/issues/new)


## 什么是 wrapcache?

`wrapcache` 是一个可以缓存方法输出的装饰器，即简单的缓存方法的输出值。

缓存数据的键值Key完全依赖于方法和传入方法的参数，这部分完全透明，使用起来非常方便。

同时还提供部分API方法来通过代码获取缓存、删除缓存，`支持Python2.6 ~ Python3.5`。

看了下面的一个示例，你就明白如何使用了：

### DEMO

```python

import wrapcache

from time import sleep
import random

@wrapcache.wrapcache(timeout = 3)
def need_cache_function(input, t = 2, o = 3):
    sleep(2)
    return random.randint(1, 100)

if __name__ == "__main__":
	print(need_cache_function(1, t = 2, o = 3)) #会在2秒之后打印随机数（例如59）
	print(need_cache_function(1, t = 2, o = 3)) #会很快就数据缓存数据59，不需要等待2秒
	sleep(3) # cache timeout
	print(need_cache_function(1, t = 2, o = 3)) #会在2秒后打印另外一个随机数，一般不会等于59


```

### 配置项

```python
@wrapcache.wrapcache(timeout = timeout, adapter = adapter)
```

 - **`timeout`**: 缓存会持续多长时间，单位为秒，如果为`-1`，表示不缓存。
 - **`adapter`**: 缓存到何处？`RedisAdapter` 和 `MemoryAdapter` 可选. 默认 `MemoryAdapter`.

### 缓存存储器

当使用`MemoryAdapter`和`RedisAdapter`适配的时候，需要在使用之前设置他们的`数据存储器`。


#### MemoryAdapter存储器

对于`MemoryAdapter`来说，提供两种缓存器：

1. 一种是基本的Python字典`{}`，也是MemoryAdapter存储`器默认的存储器`。可以无限量存储数据，具有最高的效率。但是需要手动进行清理缓存，否则可能导致内存泄露，建议在Key值比较固定的方法是哪个使用，例如无参数的方法。
2. 一种是本项目提供的`LruCacheDB`存储器（加入了`LUR`算法的Python字典）。LUR算法经过优化，所有操作的算法复杂度均为o(1)，使用时需要指定`size`，为缓存的大小，默认为-1，不限定大小，建议按照个人项目需要进行设置。

例如：

```python
from wrapcache.database import LruCacheDB
lruDB = MemoryAdapter.db = LruCacheDB(size = 100)
RedisAdapter.db = lruDB
```

#### RedisAdapter存储器

当使用`RedisAdapter`，必须设置其存储器，否则无法使用，RedisAdapter存储器极为redis连接实例，需要`pip install redis`。例如：

```python
REDIS_POOL = redis.ConnectionPool(host = '10.246.13.1', port = 6379, password = 'redis_pwd', db = 1)
REDIS_INST = redis.Redis(connection_pool = REDIS_POOL, charset = 'utf8')
RedisAdapter.db = REDIS_INST
```

## 如何安装使用?

### 安装

三种方法安装 wrapcache: 

#### 1. 使用PIP工具

 - `pip install wrapcache`

#### 2. 下载安装

 - 从 [https://pypi.python.org/pypi/wrapcache/](https://pypi.python.org/pypi/wrapcache/)下载安装包解压, 并在目录中执行 `python setup.py install`即可。

#### 3. 手动安装使用

 - 将项目中的`wrapcache` 复杂到当前目录，或者 Python的`site-packages`目录, 然后 `import wrapcache` 即可使用。


### 使用方法

#### 装饰器

```python

import wrapcache
@wrapcache.wrapcache(timeout = 3)
def need_cache_function():
	return 'hello wrapcache'

```

#### API方法

1. **`wrapcache.keyof(func, *args, **kws)`**: 获取方法的缓存Key值.
2. **`wrapcache.get(key, adapter = MemoryAdapter)`**: 或者缓存之.
3. **`wrapcache.set(key, value, timeout = -1, adapter = MemoryAdapter)`**: 设置缓存值.
4. **`wrapcache.remove(key, adapter = MemoryAdapter)`**: 移除一个缓存.
5. **`wrapcache.flush(adapter = MemoryAdapter)`**: 移除所有的缓存.

API方法中，第2~5个API在使用的时候，需要传入 `adapter` 来设置需要操作哪一个适配器。


## TODO

 - 增加memcache支持。