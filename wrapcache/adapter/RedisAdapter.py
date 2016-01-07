#-*-coding: utf-8 -*-
'''
Memory Adapter object.
'''
import time
from wrapcache.adapter.BaseAdapter import BaseAdapter
from wrapcache.adapter.CacheException import CacheTimeoutException, DBNotSetException


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
			raise CacheTimeoutException(key)
		return value

	def set(self, key, value):
		RedisAdapter.db.setex(key, value, self.timeout)
		return True

	def remove(self, key):
		self._check_db_instanse()
		return RedisAdapter.db.delete(key)

	def flush(self):
		self._check_db_instanse()
		RedisAdapter.db.flushdb() 
		return True