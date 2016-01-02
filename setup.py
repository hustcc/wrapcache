# -*- coding: utf-8 -*-
from distutils.core import setup
LONGDOC = """
wrapche
=====

wrapche：wraps cache简写， python方法装饰器缓存系统。

wrapche: Short for wraps cache. A Function / Method OUTPUT cache system base on function Decorators.

完整文档见 ``README.md``

GitHub: https://github.com/hustcc/wrapche

特点
====

-  支持三种缓存方式

   -  程序内存缓存：适合于后台运行方式的程序；
   -  redis缓存：将cache缓存到redis服务器中，便于扩展，同时方便对于wsgi运行方式的程序缓存方法；
   -  文件缓存：最简单的模式，将数据缓存到硬盘文件中；

-  使用方便：一个装饰器放到方法的头部即可缓存该方法
-  配置简单：cache指定缓存方式、timeout指定缓存过期时间，加上一些其他的配置项，例如redis连接实例等；
-  MIT 授权协议；


安装说明
========

代码对 Python 2/3 均兼容

-  全自动安装： ``easy_install wrapche`` 或者 ``pip install wrapche`` / ``pip3 install wrapche``
-  半自动安装：先下载 https://pypi.python.org/pypi/wrapche/ ，解压后运行
   python setup.py install
-  手动安装：将 jieba 目录放置于当前目录或者 site-packages 目录
-  通过 ``import wrapche`` 来引用

"""

setup(name = 'wrapche',
      version = '0.1',
      description = 'Short for wraps cache. A method cache system base on method Decorators.',
      long_description = LONGDOC,
      author = 'hustcc',
      author_email = 'i@atool.org',
      url = 'https://github.com/hustcc/wrapche',
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
      keywords = 'wrapche,Wraps Cache,Cache System,Decorators Cache,Function Cache,Method Cache',
      packages = ['wrapche'],
      package_dir = {'wrapche':'wrapche'},
      package_data = {'wrapche':['*.*']}
)