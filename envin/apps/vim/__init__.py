import os
import re
import logging
import subprocess

from . import config
from ..installer import AppInstaller


class Vim(AppInstaller):
    """ Installer for vim editor application. """

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

    def get_vim_home(self):
        """ Ask user to provide installation directory. """

        msg = 'Please specify where you want to install vim\n'
        prompt_msg = 'Installation directory: '
        return self._prompt_user(msg, prompt_msg)

    def get_python_binary_path(self):
        """ Ask user to provide python binary path. """

        msg = ("If you want to install vim with python support then please"
               "specify python binary path\n")
        bad_msg = "Bad interpreter path. Please try again."
        prompt_msg = "Python path: "
        path = self._prompt_user(msg, prompt_msg, allow_empty=True)
        while path and not os.path.exists(path):
            path = self._prompt_user(bad_msg, prompt_msg)
        return path

    def get_python_config_dir(self):
        """ Ask user to provide python binary path. """

        msg = """Please specify python config dir path\n"""
        prompt_msg = "Python config dir path: "
        bad_msg = "Bad python configuration directory path. Please try again."

        path = self._prompt_user(msg, prompt_msg)
        while path and not os.path.exists(path):
            path = self._prompt_user(bad_msg, prompt_msg)
        return path

    def run(self):
        """ Compile vim editor app. """

        self.setup_path_complete()
        vim_home = self.get_vim_home()
        python_binary_path = self.get_python_binary_path()
        if python_binary_path:
            python_config_dir = self.get_python_config_dir()

        self.install_requires()
        source_dir = self.download_src(config.SOURCE,
                                       source=config.VIM_DIR)
        os.chdir(source_dir)

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
