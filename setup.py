#!/usr/bin/env python

PROJECTNAME = 'envin'

VERSION = '0.1.0'

import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

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

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['distribute', 'cliff'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={'console_scripts': ['envin = envin.envin:main']},

)
