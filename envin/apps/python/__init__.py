import os
import logging
import tempfile
import subprocess
import urllib.request

##TODO: perhaps we should import it form distribute.
from setuptools.archive_util import unpack_archive

from . import config
from ..installer import AppInstaller

class Python(AppInstaller):
    """ Python installer. """

    log = logging.getLogger(__name__)

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
        # set python compilation flags
        unset = []

        for flag, value in config.SYSC_FLAGS.items():
            subprocess.call('export %s=%s' % (flag, value), shell=True)
            unset.append(flag)

        for p, url in [self.get_pythons_info()[v] for v in pythons_to_install]:
            os.chdir(tempfile.gettempdir())
            source_file = url.split('/')[-1]
            urllib.request.urlretrieve(url, source_file)
            unpack_archive(source_file, '.')
            source_dir = os.path.splitext(source_file)[0]

            if os.path.exists(source_dir):
                os.chdir(source_dir)
                version = p.split('-')[1]
                if version in os.listdir(config.PATCHES_DIR):
                    pdir = '%s/%s' % (config.PATCHES_DIR, version)
                    for patch in os.listdir(pdir):
                        subprocess.call('patch -p0 < %s/%s' % (pdir, patch),
                                        shell=True)

            python_home = '%s/%s' % (install_dir, p)
            os.makedirs(python_home)
            pyinst_cmd = \
                './configure --prefix=%s; make; make install' % python_home
            subprocess.call(pyinst_cmd, shell=True)
            os.chdir(tempfile.gettempdir())

        for flag in unset:
            subprocess.call('unset %s' % flag, shell=True)

        # installing setuptools
        if 'distribute_setup.py' not in os.listdir(tempfile.gettempdir()):
           urllib.request.urlretrieve(config.SETUP_URL, 'distribute_setup.py')
        subprocess.call('%s/bin/python distribute_setup.py' % python_home,
                        shell=True)

        # installing virtualenv
        subprocess.call('%s/bin/easy_install virtualenvwrapper' % python_home,
                        shell=True)

        # install activation script
        user_home = os.environ.get('HOME')
        bindir = os.path.join(user_home, 'bin')
        if not os.path.exists(bindir):
            os.makedirs(bindir)
        script_name = '%s/bin/activate-%s' % (user_home, self.version)
        with open(script_name, 'w') as act_script:
            info = {'workon_home': '%s/envs/python-%s' % (self.home,
                                                          self.version),
                    'project_home': '%s/projects' % self.home,
                    'python': '%s/bin/python' % python_home,
                    'env': '%s/bin/virtualenv' % python_home,
                    'source': '%s/bin/virtualenvwrapper.sh' % python_home}
            act_script.write(config.ACTIVATE_SCRIPT_SOURCE % info)
        os.chmod(script_name, 0o755)
