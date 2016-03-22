#-*-coding: utf-8 -*-
'''
Redis Adapter object.
'''
from wrapcache.adapter.BaseAdapter import BaseAdapter
from wrapcache.adapter.CacheException import CacheExpiredException, DBNotSetException

class RedisAdapter(BaseAdapter):
	'''
	use for redis cache
	'''
	def __init__(self, timeout = -1):
		super(RedisAdapter, self).__init__(timeout = timeout)
		if not RedisAdapter.db:
			RedisAdapter.db = None

	def _check_db_instanse(self):
		if RedisAdapter.db == None:
			raise DBNotSetException('redis instanse not set, use RedisAdapter.db = redis_instance before use.')

	def get(self, key):
		self._check_db_instanse()
		value = RedisAdapter.db.get(key)
		if value == None:
			raise CacheExpiredException(key)
		return value

	def set(self, key, value):
		RedisAdapter.db.setex(key, value, self.timeout)
		return True

	def remove(self, key):
		try:
			v = self.get(key)
			RedisAdapter.db.delete(key)
			return v
		except CacheExpiredException, _:
			return False

	def flush(self):
		self._check_db_instanse()
		RedisAdapter.db.flushdb() 
		return True

if __name__ == '__main__':
	import unittest, redis, time
	from redis.exceptions import ConnectionError
	
	class TestCase(unittest.TestCase):
		def setUp(self):
			#init redis instance
			self.test_class = RedisAdapter(timeout = 3)
		def tearDown(self):
			pass
		
		def test_memory_adapter(self):
			# test redis error
			self.assertRaises(DBNotSetException, self.test_class.get, 'test_key')
			
			REDIS_CACHE_POOL = redis.ConnectionPool(host = '162.211.225.208', port = 6739, password = '123456', db = 2)
			REDIS_CACHE_INST = redis.Redis(connection_pool = REDIS_CACHE_POOL, charset = 'utf8')
			RedisAdapter.db = REDIS_CACHE_INST #初始化装饰器缓存
			self.assertRaises(ConnectionError, self.test_class.get, 'test_key')
			
			REDIS_CACHE_POOL = redis.ConnectionPool(host = '162.211.225.209', port = 6739, password = 'wzwacxl', db = 2)
			REDIS_CACHE_INST = redis.Redis(connection_pool = REDIS_CACHE_POOL, charset = 'utf8')
			RedisAdapter.db = REDIS_CACHE_INST #初始化装饰器缓存
			
			key = 'test_key_1'
			value = str(time.time())
			
			#test set / get
			self.test_class.set(key, value)
			self.assertEqual(self.test_class.get(key).decode('utf-8'), value)
			
			#test remove
			self.test_class.set(key, value)
			self.test_class.remove(key)
			self.assertRaises(CacheExpiredException, self.test_class.get, key)
			
			#test flush
			self.test_class.set(key, value)
			self.test_class.flush()
			self.assertRaises(CacheExpiredException, self.test_class.get, key)
			
	unittest.main()