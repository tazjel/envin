#####################################
Envin - environment installation tool
#####################################

Envin is extensible environment installation tool for the developers.
The main idea is to be able to install/compile and configure desired
application to the specific place (user's home folder). Instead of executing
step by step commands from installation instruction you just run appropriate
installer and all work will be done automatically.

Envin is based on cliff package and allows to implement additional app
installers as separate packages. This organization gives developers the
opportunity organize source code in any way they like.

Installers
----------

Application isntaller class is where all installation and configuration
process happens. This class based on cliff 'Command' class and should be
subclassed. Each subcluss should implement 'run' method. It is the main
app installer method that does all work.

Currnetly Envin supports the following applications:
 - Python (2.4.6, 2.6.9, 2.7.6, 3.3.2)
 - Vim (7.4)
 - Postfix

Tested with Ubuntu 12.04


Installation
============

     python3 setup.py install

Note: by default package will be installed in user's home.


Usage
=====

     envin install [app]

app - application installer name. For example: vim
