#!/usr/bin/env python

#from distutils.core import setup, Command
from setuptools import setup,find_packages
import os
import os.path

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='profiler_online',
    version='2.0',
    description='profile python app online, Display FlameGraph in a browser',
    long_description=open('README.md').read(),
    keywords = ["profiler_online","fengyun"],
    url='http://xiaorui.cc',
    author='ruifengyun',
    author_email='rfyiamcool@163.com',
    install_requires=['gevent','flask'],
    package_data={'profiler_online': ['tools/*',
            'tools/flamegraph.pl'
    ]},
    packages=['profiler_online'],
    include_package_data=True,
#    zip_safe=False,
    license = "MIT",
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Topic :: Software Development :: Libraries :: Python Modules',
            ]
)
