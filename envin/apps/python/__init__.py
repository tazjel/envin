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
        return config.PYTHONS

    def get_pythons_versions(self):
        versions = list(self.get_pythons_info().keys())
        versions.sort()
        return versions

    def get_pythons_to_install(self, app):
        """ Ask user to provide python versions to install.

        :param app: envin application object
        :type app: object
        """

        msg = ("Please type which python versions (divided by comma) you want "
               "to install. Example: 3.3, 2.4\n"
               "If you want to install all pythons in provided list type *:\n"
               "{}\n").format(', '.join(self.get_pythons_versions()))
        prompt_msg = "Enter python versions: "
        bad_msg = "Bad python versions provided!!!\n"

        versions = self._prompt_user(app, msg, prompt_msg)
        if versions == "*":
            return self.get_pythons_versions()

        versions = [v.strip() for v in versions.split(',')]
        pythons = self.get_pythons_info()
        py_versions = list(filter(lambda v: v in pythons, versions))
        if not py_versions or len(py_versions) != len(versions):
            app.stdout.write(bad_msg)
            return self.get_pythons_to_install(app)

        return list(py_versions)

    def get_install_dir(self, app):
        """ Ask user to provide installation directory.

        :param app: envin application object
        :type app: object
        """
        msg = 'Please specify where you want to install pythons.\n'
        prompt_msg = 'Installation directory: '
        return self._prompt_user(app, msg, prompt_msg)

    def set_sys_flags(self):
        for flag, value in config.SYSC_FLAGS.items():
            subprocess.call('export {}={}'.format(flag, value), shell=True)
            self.unset.append(flag)

    def unset_sys_flags(self):
        for flag in self.unset:
            subprocess.call('unset {}'.format(flag), shell=True)

    def _get_pypath(self, python_home, version):
        path = '{}/bin/python'
        if version.startswith('3'):
            path = '{}/bin/python3'
        return path.format(python_home)

    def install_distribute(self, python_home, version):
        # installing distribute
        dst_src = self.download_src(config.SETUP_URL, archive=False)
        subprocess.call('{} {}'.format(self._get_pypath(python_home, version),
                                       dst_src), shell=True)

    def install_pip(self, python_home, version):
        source_dir = self.download_src(config.PIP_SOURCES[version])
        os.chdir(source_dir)
        pip_cmd = '{} setup.py install'.format(self._get_pypath(python_home,
                                                                version))
        subprocess.call(pip_cmd, shell=True)

    def install_wrapper(self, python_home, version):
        if version == '2.4':
            #install specific virtialenv for python 2.4
            ven_cmd = \
                '{}/bin/easy_install virtualenv==1.7.2'.format(python_home)
            subprocess.call(ven_cmd, shell=True)

        venv_cmd = \
            '{}/bin/pip install virtualenvwrapper'.format(python_home)
        if version == '2.4':
            venv_cmd = '{}==2.9'.format(venv_cmd)
        subprocess.call(venv_cmd, shell=True)

    def setup_activation_script(self, install_dir, dirname, version):
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

    def run(self, app, args):
        """ Compile vim editor app.

        :param app: envin application object
        :type app: object
        :param args: arguments list passed in command line
        :type args: list
        """

        pythons_to_install = self.get_pythons_to_install(app)
        self.setup_path_complete()
        install_dir = self.get_install_dir(app)

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

            self.install_distribute(python_home, version)
            self.install_pip(python_home, version)
            self.install_wrapper(python_home, version)
            self.setup_activation_script(install_dir, dirname, version)
