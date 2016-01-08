#!/bin/bash
coverage run tests/test_unitest.py
coverage run wrapcache/adapter/MemoryAdapter.py
coverage run wrapcache/adapter/RedisAdapter.py
