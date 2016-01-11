#!/bin/bash
coverage run wrapcache/database/__init__.py
coverage run tests/test_unitest.py
coverage run wrapcache/adapter/MemoryAdapter.py
# coverage run wrapcache/adapter/RedisAdapter.py