#-*-coding: utf-8 -*-
'''
Memory Adapter object.
'''
import time
from wrapcache.adapter.BaseAdapter import BaseAdapter
from wrapcache.adapter.CacheException import CacheExpiredException


class MemoryAdapter(BaseAdapter):
	'''
	use for memory cache
	'''
	def __init__(self, timeout = -1):
		super(MemoryAdapter, self).__init__(timeout = timeout)
		if MemoryAdapter.db is None:
			MemoryAdapter.db = {}

	def get(self, key):
		cache = MemoryAdapter.db.get(key, {})
		if time.time() - cache.get('time', 0) > 0:
			self.remove(key) #timeout, rm key, reduce memory
			raise CacheExpiredException(key)
		else:
			return cache.get('value', None)

	def set(self, key, value):
		cache = {
			'value' : value,
			'time'  : time.time() + self.timeout
		}
		MemoryAdapter.db[key] = cache
		return True

	def remove(self, key):
		return MemoryAdapter.db.pop(key, {}).get('value', None)

	def flush(self):
		MemoryAdapter.db.clear()
		return True

if __name__ == '__main__':
	import unittest

	class TestCase(unittest.TestCase):
		def setUp(self):
			self.test_class = MemoryAdapter(timeout = 3)
		def tearDown(self):
			pass

		def test_init_db_with_singleton(self):
			pre_db = self.test_class.db
			# get a new instance without cache
			new_adapter = MemoryAdapter(timeout = 1)
			cur_db = new_adapter.db
			self.assertEqual(id(pre_db), id(cur_db))

		def test_memory_adapter(self):
			key = 'test_key_1'
			value = str(time.time())

			#test set / get
			self.test_class.set(key, value)
			self.assertEqual(self.test_class.get(key), value)
			time.sleep(4)
			self.assertRaises(CacheExpiredException, self.test_class.get, key)

			#test remove
			self.test_class.set(key, value)
			self.test_class.remove(key)
			self.assertRaises(CacheExpiredException, self.test_class.get, key)

			#test flush
			self.test_class.set(key, value)
			self.test_class.flush()
			self.assertRaises(CacheExpiredException, self.test_class.get, key)

	unittest.main()
