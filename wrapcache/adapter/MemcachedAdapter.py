#-*-coding: utf-8 -*-
'''
Memcached Adapter object.
'''
from wrapcache.adapter.BaseAdapter import BaseAdapter
from wrapcache.adapter.CacheException import CacheExpiredException, DBNotSetException

class MemcachedAdapter(BaseAdapter):
    '''
    use for memcached cache
    '''
    def __init__(self, timeout = -1):
        super(MemcachedAdapter, self).__init__(timeout = timeout)
        if not MemcachedAdapter.db:
            MemcachedAdapter.db = None

    def _check_db_instanse(self):
        if MemcachedAdapter.db == None:
            raise DBNotSetException('memcached instanse not set, use MemcachedAdapter.db = memcache_instance before use.')

    def get(self, key):
        self._check_db_instanse()
        value = MemcachedAdapter.db.get(key)
        if value == None:
            raise CacheExpiredException(key)
        return value

    def set(self, key, value):
        MemcachedAdapter.db.set(key, value, time = self.timeout)
        return True

    def remove(self, key):
        try:
            v = self.get(key)
            MemcachedAdapter.db.delete(key)
            return v
        except CacheExpiredException, _:
            return False

    def flush(self):
        self._check_db_instanse()
        MemcachedAdapter.db.flush_all() 
        return True

if __name__ == '__main__':
    import unittest, memcache, time
    
    class TestCase(unittest.TestCase):
        def setUp(self):
            #init redis instance
            self.test_class = MemcachedAdapter(timeout = 3)
        def tearDown(self):
            pass
        
        def test_memory_adapter(self):
            # test redis error
            self.assertRaises(DBNotSetException, self.test_class.get, 'test_key')
            
            memcache_inst = memcache.Client(['10.246.14.164:11211'])
            MemcachedAdapter.db = memcache_inst #初始化装饰器缓存
            self.assertRaises(CacheExpiredException, self.test_class.get, 'test_key') #链接不上
            
            memcache_inst = memcache.Client(['10.246.14.165:11211'])
            MemcachedAdapter.db = memcache_inst #初始化装饰器缓存
            
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