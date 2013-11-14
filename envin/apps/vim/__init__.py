import os
import re
import tempfile
import logging
import subprocess
import urllib.request

from setuptools.archive_util import unpack_archive

from . import config
from ..installer import AppInstaller


class Vim(AppInstaller):
    """ Installer for vim editor appl. """

    log = logging.getLogger(__name__)

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
            if match.group(1).decode('utf-8') == '3':
                return True
            else:
                return False

        raise ValueError("Bad python path specified!")

    def get_vim_home(self, app):
        """ Ask user to provide installation directory.

        :param app: envin application object
        :type app: object
        """
        msg = 'Please specify where you want to install vim\n'
        prompt_msg = 'Installation directory: '
        return self._prompt_user(app, msg, prompt_msg)

    def get_python_binary_path(self, app):
        """ Ask user to provide python binary path.

        :param app: envin application object
        :type app: object
        """
        msg = ("If you want to install vim with python support then please"
               "specify python binary path\n")
        bad_msg = "Bad interpreter path. Please try again."
        prompt_msg = "Python path: "
        path = self._prompt_user(app, msg, prompt_msg, allow_empty=True)
        while path and not os.path.exists(path):
            path = self._prompt_user(app, bad_msg, prompt_msg)
        return path

    def get_python_config_dir(self, app):
        """ Ask user to provide python binary path.

        :param app: envin application object
        :type app: object
        """
        msg = """Please specify python config dir path\n"""
        prompt_msg = "Python config dir path: "
        bad_msg = "Bad python configuration directory path. Please try again."

        path = self._prompt_user(app, msg, prompt_msg)
        while path and not os.path.exists(path):
            path = self._prompt_user(app, bad_msg, prompt_msg)
        return path

    def run(self, app, args):
        """ Compile vim editor app.

        :param app: envin application object
        :type app: object
        :param args: arguments list passed in command line
        :type args: list
        """

        self.setup_path_complete()
        vim_home = self.get_vim_home(app)
        python_binary_path = self.get_python_binary_path(app)
        if python_binary_path:
            python_config_dir = self.get_python_config_dir(app)

        self.install_requires()
        os.chdir(tempfile.gettempdir())
        source_file = config.SOURCE.split('/')[-1]
        urllib.request.urlretrieve(config.SOURCE, source_file)
        unpack_archive(source_file, '.')
        os.chdir(config.VIM_DIR)

        if not os.path.exists(vim_home):
            os.makedirs(vim_home)

        cmd = config.CONFIG_CMD.format(home=vim_home)
        if python_binary_path:
            if self.is_python_3(python_binary_path):
                pversion = 'python3'
            else:
                pversion = 'python'
            cmd = cmd + config.PYTHON_CONFIG.format(
                pversion=pversion,
                vi_cv_path_python=python_binary_path,
                pconfig_path=python_config_dir)

        subprocess.call('%s %s' % (cmd, config.INSTALL_CMD), shell=True)
