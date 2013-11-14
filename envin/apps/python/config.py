import os

PYTHONS = {'3.3': ('python-3.3.2',
                   'http://python.org/ftp/python/3.3.2/Python-3.3.2.tgz'),
           '2.7': ('python-2.7.6',
                   'http://python.org/ftp/python/2.7.5/Python-2.7.6.tgz'),
           '2.6': ('python-2.6.9',
                   'http://python.org/ftp/python/2.6.9/Python-2.6.9.tgz'),
           '2.4': ('python-2.4.6',
                   'http://python.org/ftp/python/2.4.6/Python-2.4.6.tgz')}

SETUP_URL = 'http://python-distribute.org/distribute_setup.py'
PATCHES_DIR = '%s/patches' % os.path.dirname(__file__)

SYSC_FLAGS = {'arch':'$(dpkg-architecture -qDEB_HOST_MULTIARCH)',
              'LDFLAGS':'"-L/usr/lib/$arch -L/lib/$arch"',
              'CFLAGS':'"-I/usr/include/$arch"',
              'CPPFLAGS':'"-I/usr/include/$arch"'}

ACTIVATE_SCRIPT_SOURCE = """export WORKON_HOME="%(workon_home)s"
export PROJECT_HOME="%(project_home)s"
export VIRTUALENVWRAPPER_PYTHON="%(python)s"
export VIRTUALENVWRAPPER_VIRTUALENV="%(env)s"
source %(source)s"""
