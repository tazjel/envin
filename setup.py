#!/usr/bin/env python

PROJECTNAME = 'envin'

VERSION = '0.1.0'

import distribute_setup
distribute_setup.use_setuptools()

from distutils.core import setup

setup(
    name=PROJECTNAME,
    version=VERSION,
    author='Taras Melnychuk',
    author_email='melnychuktaras@gmail.com',
    #packages=['towelstuff', 'towelstuff.test'],
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    #url='http://pypi.python.org/pypi/TowelStuff/',
    #license='LICENSE.txt',
    description='Environmen installer tool.',
    long_description=open('README.txt').read(),
    #install_requires=[
    #    "Django >= 1.1.1",
    #    "caldav == 0.1.4",
    #],
)
