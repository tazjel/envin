import os
import urllib
import logging
import tempfile
import subprocess

#TODO: perhaps we should import it form distribute.
from setuptools.archive_util import unpack_archive
#from setuptools.command.easy_install import chmod

from cliff.command import Command

from envin.python.config import PYTHONS
from envin.python.config import SYSC_FLAGS
#from envin.python.config import SETUP_URL
from envin.python.config import PATCHES_DIR
from envin.python.config import INSTALL_COMMAND
#from envin.python.config import ACTIVATE_SCRIPT_SOURCE


class PyInstall(Command):
    """ Command that installs python. """

    pythons = PYTHONS
    log = logging.getLogger(__name__)

    requirements = os.path.join(os.path.dirname(__file__),
                                'requirements.txt')

    def install_requires(self):
        self.package_collection = []
        with open(self.requirements, 'r') as packages:
            package_collection = \
                    [package.strip() for package in packages.readlines()]

        self.log.info('Install packages.')
        subprocess.call('%s %s' % (INSTALL_COMMAND,
            ' '.join(package_collection)), shell=True)

    def take_action(self, parsed_args):
        #self.log.info('sending greeting')
        #self.log.debug('debugging')
        #self.app.stdout.write('hi!\n')

        # install requirements
        self.install_requires()
        # set python compilation flags
        unset = []

        for flag, value in SYSC_FLAGS.items():
            subprocess.call('export %s=%s' % (flag, value), shell=True)
            unset.append(flag)

        home = os.getcwd()
        for p, url in self.pythons.items():
            os.chdir(tempfile.gettempdir())
            source_file = url.split('/')[-1]
            urllib.urlretrieve(url, source_file)
            unpack_archive(source_file, '.')
            source_dir = os.path.splitext(source_file)[0]

            if os.path.exists(source_dir):
                os.chdir(source_dir)
                version = p.split('-')[1]
                if version in os.listdir(PATCHES_DIR):
                    pdir = '%s/%s' % (PATCHES_DIR, version)
                    for patch in os.listdir(pdir):
                        subprocess.call('patch -p0 < %s/%s' % (pdir, patch),
                                        shell=True)

            python_home = '%s/%s' % (home, p)
            os.makedirs(python_home)
            pyinst_cmd = \
                './configure --prefix=%s; make; make install' % python_home
            subprocess.call(pyinst_cmd, shell=True)
            os.chdir(tempfile.gettempdir())

        for flag in unset:
            subprocess.call('unset %s' % flag, shell=True)

        # installing setuptools
        #if 'distribute_setup.py' not in os.listdir(tempfile.gettempdir()):
        #    urllib.urlretrieve(SETUP_URL, 'distribute_setup.py')
        #subprocess.call('%s/bin/python distribute_setup.py' % python_home,
        #                shell=True)

        ## installing virtualenv
        #subprocess.call('%s/bin/easy_install virtualenvwrapper' % python_home,
        #                shell=True)

        ## install activation script
        #user_home = os.environ.get('HOME')
        #bindir = os.path.join(user_home, 'bin')
        #if not os.path.exists(bindir):
        #    os.makedirs(bindir)
        #script_name = '%s/bin/activate-%s' % (user_home, self.version)
        #with open(script_name, 'w') as act_script:
        #    info = {'workon_home': '%s/envs/python-%s' % (self.home,
        #                                                  self.version),
        #            'project_home': '%s/projects' % self.home,
        #            'python': '%s/bin/python' % python_home,
        #            'env': '%s/bin/virtualenv' % python_home,
        #            'source': '%s/bin/virtualenvwrapper.sh' % python_home}
        #    act_script.write(ACTIVATE_SCRIPT_SOURCE % info)
        #chmod(script_name, 0755)
