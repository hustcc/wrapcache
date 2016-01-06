#-*-coding: utf-8 -*-

import unittest, time
import sys, random

sys.path.append(".")
sys.path.append("..")
import wrapcache


class TestMemory:
    @wrapcache.wrapcache(timeout = 3)
    def test_cache(self):
        return time.time()

    @wrapcache.wrapcache(timeout = 3)
    def test_input_cache(self, i, j):
        return (time.time() + i, j)

    @wrapcache.wrapcache(timeout = 10)
    def test_input_order_cache(self, i = 1, j = 's'):
        return (time.time() + i, j)

    @wrapcache.wrapcache(timeout = 3)
    def need_cache_function(self):
        time.sleep(2)
        print('cache timeout, new...')
        return random.randint(1, 100)

class MemoryUnitest(unittest.TestCase):
    def setUp(self):
        self.test_class = TestMemory()
    
    def tearDown(self):
        pass
    
    def test_cache(self):
        val_1 = self.test_class.test_cache()
        self.assertEqual(self.test_class.test_cache(), val_1, 'test_cache fail')
        time.sleep(5)
        self.assertNotEqual(self.test_class.test_cache(), val_1, 'test_cache fail')

    def test_input_cache(self):
        val_1 = self.test_class.test_input_cache(1, 'hello world')
        self.assertEqual(self.test_class.test_input_cache(1, 'hello world'), val_1, 'test_input_cache fail')
        time.sleep(5)
        self.assertNotEqual(self.test_class.test_input_cache(1, 'hello world'), val_1, 'test_input_cache fail')
        self.assertNotEqual(self.test_class.test_input_cache(1, 'hello world'), self.test_class.test_input_cache(2, 'hello world'), 'test_input_cache fail')

    def test_input_order_cache(self):
        val_1 = self.test_class.test_input_order_cache(i = 1, j = 'hello world')
        time.sleep(0.1)
        self.assertEqual(self.test_class.test_input_order_cache(j = 'hello world', i = 1), val_1, 'test_input_order_cache fail')
        self.assertNotEqual(self.test_class.test_input_order_cache(j = 'hello world', i = 1), self.test_class.test_input_order_cache(j = 'hello wrapcache', i = 1), 'test_input_order_cache fail')

    def test_keyof_api(self):
        key_1 = wrapcache.keyof(self.test_class.test_input_cache, i = 1, j = 'hello world')
        key_2 = wrapcache.keyof(self.test_class.test_input_cache, i = 1, j = 'hello world')
        key_3 = wrapcache.keyof(self.test_class.test_input_cache, j = 'hello world', i = 1)
        key_4 = wrapcache.keyof(self.test_class.test_input_cache, j = 'hello wrapcache', i = 1)
        self.assertEqual(key_1, key_2, 'test_keyof_api fail')
        self.assertEqual(key_1, key_3, 'test_keyof_api fail')
        self.assertNotEqual(key_1, key_4, 'test_keyof_api fail')

    def test_apis(self):
        wrapcache.flush()
        #get api
        key_1 = wrapcache.keyof(self.test_class.test_input_cache, i = 1, j = 'hello world')
        value_1 = wrapcache.get(key_1)
        if not value_1:
            keyNone = True
        self.assertEqual(keyNone, True, 'test_apis fail')
        #set api
        value_2 =  wrapcache.set(key_1, 'test_value', timeout = 3)
        self.assertEqual(value_2, 'test_value', 'test_keyof_api fail')
        #get api / timeout
        value_3 = wrapcache.get(key_1)
        self.assertEqual(value_3, 'test_value', 'test_keyof_api fail')
        time.sleep(3)
        value_3 = wrapcache.get(key_1)
        if not value_3:
            keyNone = True
        self.assertEqual(keyNone, True, 'test_apis fail')

        #remove api
        value_4 =  wrapcache.set(key_1, 'test_value 4', timeout = 3)
        self.assertEqual(value_4, 'test_value 4', 'test_keyof_api fail')
        value_5 = wrapcache.remove(key_1)
        self.assertEqual(value_4, value_5, 'test_keyof_api fail')

        value_3 = wrapcache.get(key_1)
        if not value_5:
            keyNone = True
        self.assertEqual(keyNone, True, 'test_apis fail')

        #flush api
        value_6 =  wrapcache.set(key_1, 'test_value 4', timeout = 3)
        self.assertEqual(value_6, 'test_value 4', 'test_keyof_api fail')
        self.assertTrue(wrapcache.flush(), 'test_keyof_api fail')

        value_6 = wrapcache.get(key_1)
        if not value_6:
            keyNone = True
        self.assertEqual(keyNone, True, 'test_apis fail')

    def test_need_cache_function(self):
        for i in range(10):
            time.sleep(1)
            print(self.test_class.need_cache_function())

if __name__ =='__main__':
    unittest.main()