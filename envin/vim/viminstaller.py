import os
import re
import urllib
import tempfile
import logging
import subprocess
from setuptools.archive_util import unpack_archive

from cliff.command import Command

from .config import SOURCE, INSTALL_COMMAND, CONFIG_CMD


class VimInstall(Command):
    """ Command to compile vim editor. """

    requirements = os.path.join(os.path.dirname(__file__),
                                'requirements.txt')
    log = logging.getLogger(__name__)

    def install_requires(self):
        self.package_collection = []
        with open(self.requirements, 'r') as packages:
            package_collection = \
                    [package.strip() for package in packages.readlines()]

        self.log.info('Install packages.')
        subprocess.call('%s %s' % (INSTALL_COMMAND,
            ' '.join(package_collection)), shell=True)

    def is_python_3(self, python_path):
        """ Checks if specified python path is python 3 or not.

        :param python_path: path to python binary
        :type python_path: string
        :returns: Boolean

        """
        cmd = "{} -c 'import sys; print(sys.version)'".format(python_path)

        try:
             out = subprocess.check_output(cmd, stderr=subprocess.STDOUT,
                                           shell=True)
        except subprocess.CalledProcessError:
            raise ValueError("Bad python path specified!")

        match = re.match(b'^(\d)\.', out)
        if match:
            if match.group(0) == '3':
                return True
            else:
                return False

        raise ValueError("Bad python path specified!")


    def take_action(self, parsed_args):

        self.app.stdout.write('Please specify where you want to install vim\n')
        vim_home = input('>')

        self.app.stdout.write('Please specify python path for vim\n')
        python_binary_path= input('>')
        self.is_python_3(python_binary_path)

        self.app.stdout.write('Please specify python config dir path\n')
        python_config_dir = input('>')

        self.install_requires()
        os.chdir(tempfile.gettempdir())
        source_file = SOURCE.split('/')[-1]
        urllib.request.urlretrieve(SOURCE, source_file)
        unpack_archive(source_file, '.')
        os.chdir('vim74')

        if not os.path.exists(vim_home):
            os.makedirs(vim_home)

        conf_cmd = CONFIG_CMD.format(home=vim_home,
                                     vi_cv_path_python3=python_binary_path,
                                     pconfig_path=python_config_dir)
        make_install = 'make; make install'
        subprocess.call('%s %s' % (conf_cmd, make_install), shell=True)



