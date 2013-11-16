import os
import logging
import subprocess

from . import config
from ..installer import AppInstaller


class Python(AppInstaller):
    """ Python installer. """

    log = logging.getLogger(__name__)
    unset = []

    def get_pythons_info(self):
        """ Returns pythons info that are available for compile. """

        return config.PYTHONS

    def get_pythons_versions(self):
        """ Returns pythons versions that are available for compile. """

        versions = list(self.get_pythons_info().keys())
        versions.sort()
        return versions

    def get_pythons_to_install(self):
        """ Ask user to provide python versions to install. """

        msg = ("Please type which python versions (divided by comma) you want "
               "to install. Example: 3.3, 2.4\n"
               "If you want to install all pythons in provided list type *:\n"
               "{}\n").format(', '.join(self.get_pythons_versions()))
        prompt_msg = "Enter python versions: "
        bad_msg = "Bad python versions provided!!!\n"

        versions = self._prompt_user(msg, prompt_msg)
        if versions == "*":
            return self.get_pythons_versions()

        versions = [v.strip() for v in versions.split(',')]
        pythons = self.get_pythons_info()
        py_versions = list(filter(lambda v: v in pythons, versions))
        if not py_versions or len(py_versions) != len(versions):
            self.app.stdout.write(bad_msg)
            return self.get_pythons_to_install()

        return list(py_versions)

    def get_install_dir(self):
        """ Ask user to provide installation directory. """

        msg = 'Please specify where you want to install pythons.\n'
        prompt_msg = 'Installation directory: '
        return self._prompt_user(msg, prompt_msg)

    def set_sys_flags(self):
        """ Set sys flags for python compilation."""

        for flag, value in config.SYSC_FLAGS.items():
            subprocess.call('export {}={}'.format(flag, value), shell=True)
            self.unset.append(flag)

    def unset_sys_flags(self):
        """ Unset sys flags after that was set for python compilation. """

        for flag in self.unset:
            subprocess.call('unset {}'.format(flag), shell=True)

    def _get_pypath(self, python_home, version):
        """ Constructs path to python binary.

        :param python_home: python home directory path
        :type python_home: string

        :param version: python version
        :type version: string
        """

        path = '{}/bin/python'
        if version.startswith('3'):
            path = '{}/bin/python3'
        return path.format(python_home)

    def install_stools(self, python_home, version):
        """ Install setuptools.

        :param python_home: python home directory path
        :type python_home: string

        :param version: python version
        :type version: string
        """

        dst_src = self.download_src(config.STOOLS_URL, archive=False)
        subprocess.call('{} {}'.format(self._get_pypath(python_home, version),
                                       dst_src), shell=True)

    def install_pip(self, python_home, version):
        """ Install pip installer.

        :param python_home: python home directory path
        :type python_home: string

        :param version: python version
        :type version: string
        """

        source_dir = self.download_src(config.PIP_SOURCES[version])
        os.chdir(source_dir)
        pip_cmd = '{} setup.py install'.format(self._get_pypath(python_home,
                                                                version))
        subprocess.call(pip_cmd, shell=True)

    def install_wrapper(self, python_home, version):
        """ Install virtial environment wrapper.

        :param python_home: python home directory path
        :type python_home: string

        :param version: python version
        :type version: string
        """

        if version == '2.4':
            #install specific virtialenv for python 2.4
            ven_cmd = \
                '{}/bin/easy_install virtualenv==1.7.2'.format(python_home)
            subprocess.call(ven_cmd, shell=True)

        venv_cmd = \
            '{}/bin/pip install virtualenvwrapper'.format(python_home)
        if version == '2.4':
            #install specific virtialenvwrapper for python 2.4
            venv_cmd = '{}==2.9'.format(venv_cmd)

        subprocess.call(venv_cmd, shell=True)

    def setup_activation_script(self, install_dir, dirname, version):
        """ Setup activation script for virtualenvwrapper.

        :param install_dir: pythons install directory path
        :type python_home: string

        :param dirname: python installation directory name
        :type dirname: string

        :param version: python version
        :type version: string
        """

        python_home = os.path.join(install_dir, dirname)
        bindir = os.path.join(python_home, 'bin')
        script_name = '{}/activate-{}'.format(bindir, version)
        with open(script_name, 'w') as act_script:
            info = {
                'workon_home': '{}/envs/python-{}'.format(install_dir,
                                                          version),
                'project_home': '{}/projects'.format(python_home),
                'python': self._get_pypath(python_home, version),
                'env': '{}/bin/virtualenv'.format(python_home),
                'source': '{}/bin/virtualenvwrapper.sh'.format(python_home)}
            act_script.write(config.ACTIVATE_SCRIPT_SOURCE.format(**info))
        os.chmod(script_name, 0o755)

    def run(self):
        """ Compile vim editor app. """

        pythons_to_install = self.get_pythons_to_install()
        self.setup_path_complete()
        install_dir = self.get_install_dir()

        self.install_requires()
        for version in pythons_to_install:
            self.set_sys_flags()
            dirname, url = self.get_pythons_info()[version]
            source_dir = self.download_src(url)
            if os.path.exists(source_dir):
                os.chdir(source_dir)
                patches = config.PATCHES_DIR.format(os.path.dirname(__file__))
                if version in os.listdir(patches):
                    pdir = os.path.join(patches, version)
                    for patch in os.listdir(pdir):
                        subprocess.call(
                            'patch -p0 < {}'.format(os.path.join(pdir, patch)),
                            shell=True)

            python_home = os.path.join(install_dir, dirname)
            os.makedirs(python_home)
            cmd = '{} {}'.format(config.CONF_CMD.format(python_home),
                                 config.INSTALL_CMD)
            subprocess.call(cmd, shell=True)
            self.unset_sys_flags()

            self.install_stools(python_home, version)
            self.install_pip(python_home, version)
            self.install_wrapper(python_home, version)
            self.setup_activation_script(install_dir, dirname, version)
