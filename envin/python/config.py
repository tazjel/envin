import os

PYTHONS = {
    'python-3.3.2':'http://python.org/ftp/python/3.3.2/Python-3.3.2.tgz',
    'python-2.7.5':'http://python.org/ftp/python/2.7.5/Python-2.7.5.tgz',
    'python-2.6.8':'http://python.org/ftp/python/2.6.8/Python-2.6.8.tgz',
    'python-2.4.6':'http://python.org/ftp/python/2.4.6/Python-2.4.6.tgz'
    }

SETUP_URL = 'http://python-distribute.org/distribute_setup.py'
PATCHES_DIR = '%s/patches' % os.path.dirname(__file__)

#INSTALL_COMMAND = 'sudo apt-get --assume-yes install'
SYSC_FLAGS = {'arch':'$(dpkg-architecture -qDEB_HOST_MULTIARCH)',
              'LDFLAGS':'"-L/usr/lib/$arch -L/lib/$arch"',
              'CFLAGS':'"-I/usr/include/$arch"',
              'CPPFLAGS':'"-I/usr/include/$arch"'}

ACTIVATE_SCRIPT_SOURCE = """export WORKON_HOME="%(workon_home)s"
export PROJECT_HOME="%(project_home)s"
export VIRTUALENVWRAPPER_PYTHON="%(python)s"
export VIRTUALENVWRAPPER_VIRTUALENV="%(env)s"
source %(source)s"""

INSTALL_COMMAND = 'sudo apt-get --assume-yes install'
