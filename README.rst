#####################################
Envin - environment installation tool
#####################################

Envin is extensible environment installation tool for the developers.

The main idea is to be able to install/compile and configure desired
application to the specific place (user's home folder). Instead of executing
step by step commands from installation instruction you just run appropriate
installer and all work will be done automatically.

Currnetly Envin supports the following applications:
 - Python (2.4.6, 2.6.9, 2.7.6, 3.3.2)
 - Vim (7.4)
 - Postfix


Installation
============

     python3 setup.py install

Note: by default will be installed in user's home.


Usage
=====

     envin install [app]

app - application installer name. For example: vim
