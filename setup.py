# -*- coding: utf-8 -*-
from distutils.core import setup
LONGDOC = """
wrapcache
=====

wrapcache：wrap cache， python方法装饰器缓存系统。

wrapcache: Short for wraps cache. A Function / Method OUTPUT cache system base on function Decorators.

完整文档见 ``README.md``

GitHub: https://github.com/hustcc/wrapcache

特点
====

-  兼容各种版本的python，包括python2和python3的个版本；
-  使用方便：一个装饰器放到方法的头部即可缓存该方法；
-  配置简单：cache指定缓存方式、timeout指定缓存过期时间；
-  MIT 授权协议；


安装说明
========

代码对 Python 2/3 均兼容

-  全自动安装： ``easy_install wrapcache`` 或者 ``pip install wrapcache`` / ``pip3 install wrapcache``
-  半自动安装：先下载 https://pypi.python.org/pypi/wrapcache/ ，解压后运行
   python setup.py install
-  手动安装：将 jieba 目录放置于当前目录或者 site-packages 目录
-  通过 ``import wrapcache`` 来引用

"""

setup(name = 'wrapcache',
      version = '1.0.1',
      description = 'Short for wraps cache. A method cache system base on method Decorators.',
      long_description = LONGDOC,
      author = 'hustcc',
      author_email = 'i@atool.org',
      url = 'https://github.com/hustcc/wrapcache',
      license = "MIT",
      classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Chinese (Traditional)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
        'Topic :: Software Development :: Embedded Systems'
      ],
      keywords = 'wrapcache,Wraps Cache,Cache System,Decorators Cache,Function Cache,Method Cache',
      packages = ['wrapcache'],
      package_dir = {'wrapcache':'wrapcache'},
      package_data = {'wrapcache':['*.*', 'adapter/*']}
)