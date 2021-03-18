#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://dialpad-stats.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='dialpad-stats',
    version='0.1.0',
    description='Retrieve analytics data from the DialPad REST API',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Zak Fama',
    author_email='fama.zachary@gmail.com',
    url='https://github.com/famazak/dialpad-stats',
    packages=[
        'dialpad_stats',
    ],
    package_dir={'dialpad-stats': 'dialpad-stats'},
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False,
    keywords='dialpad-stats',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
