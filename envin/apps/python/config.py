PYTHONS = {'3.2': ('python-3.3.2',
                   'http://python.org/ftp/python/3.3.2/Python-3.3.2.tgz'),
           '2.7': ('python-2.7.6',
                   'http://python.org/ftp/python/2.7.6/Python-2.7.6.tgz'),
           '2.6': ('python-2.6.9',
                   'http://python.org/ftp/python/2.6.9/Python-2.6.9.tgz'),
           '2.4': ('python-2.4.6',
                   'http://python.org/ftp/python/2.4.6/Python-2.4.6.tgz')}

STOOLS_URL = 'https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py'
PIP_SOURCES = {
    '2.4': 'https://pypi.python.org/packages/source/p/pip/pip-1.1.tar.gz',
    '2.6': 'https://pypi.python.org/packages/source/p/pip/pip-1.4.1.tar.gz',
    '2.7': 'https://pypi.python.org/packages/source/p/pip/pip-1.4.1.tar.gz',
    '3.2': 'https://pypi.python.org/packages/source/p/pip/pip-1.4.1.tar.gz'}

PATCHES_DIR = '{}/patches'

SYSC_FLAGS = {'arch':'$(dpkg-architecture -qDEB_HOST_MULTIARCH)',
              'LDFLAGS':'"-L/usr/lib/$arch -L/lib/$arch"',
              'CFLAGS':'"-I/usr/include/$arch"',
              'CPPFLAGS':'"-I/usr/include/$arch"'}

CONF_CMD = './configure --prefix={};'
INSTALL_CMD = 'make; make install;'
ACTIVATE_SCRIPT_SOURCE = """export WORKON_HOME="{workon_home}"
export PROJECT_HOME="{project_home}"
export VIRTUALENVWRAPPER_PYTHON="{python}"
export VIRTUALENVWRAPPER_VIRTUALENV="{env}"
source {source}"""
