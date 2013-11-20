#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()

from setuptools import setup, find_packages


setup(
    name='envin',
    version='0.1-alpha',
    author='Taras Melnychuk',
    author_email='melnychuktaras@gmail.com',
    url='http://github.com/melta/envin',
    description='Environmen installer tool.',
    long_description=open('README.rst').read(),
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],
    platforms=['Ubuntu 12.04'],
    scripts=[],
    provides=[],
    install_requires=['distribute', 'cliff'],
    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['envin = envin.envin:main'],
        'envin.commands': ['install = envin.install:Install'],
        'envin.apps': ['python = envin.apps.python:Python',
                       'vim = envin.apps.vim:Vim',
                       'postfix = envin.apps.postfix:Postfix'],
    },
)
