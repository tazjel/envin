import os
import subprocess

from cliff.command import Command


class VimInstaller(Command):
    """ Command to compile vim editor. """

    install_command = 'sudo apt-get --assume-yes install'
    requirements = os.path.join(os.path.dirname(__file__),
                                'requirements.txt')
    def install_requires(self):
        self.package_collection = []
        with open(self.requirements, 'r') as packages:
            package_collection = \
                    [package.strip() for package in packages.readlines()]

        self.log.info('Install packages.')
        subprocess.call('%s %s' % (self.install_command,
            ' '.join(package_collection)), shell=True)

    def take_action(self, parsed_args):

        self.install_requires(self)

        os.chdir(tempfile.gettempdir())
        source_file = self.url.split('/')[-1]
        urllib.urlretrieve(self.url, source_file)
        unpack_archive(source_file, '.')
        os.chdir('vim73')

        vim_home = '%s/vim' % self.home
        if not os.path.exists(vim_home):
            os.makedirs(vim_home)

        conf_cmd = ('./configure'
                    ' --enable-perlinterp'
                    ' --enable-pythoninterp'
                    ' --enable-rubyinterp'
                    ' --enable-cscope'
                    ' --with-features=huge'
                    ' --prefix="%s"') % vim_home
        make_install = 'make; make install'
        subprocess.call('%s %s' % (conf_cmd, make_install),
                        shell=True)
