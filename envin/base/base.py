import subprocess

from cliff.command import Command

from .config import INSTALL_COMMAND


class BaseCommand(Command):
    """ Abstract base command class for envin installation commands."""

    def install_packages(self, packages=None):
        """ Install packages from file.

        :param packages: file name where packages located
        :type packages: string
        """

        with open(packages, 'r') as packages:
            packages_list =  [p.strip() for p in packages.readlines()]

        if packages_list:
            cmd = '{0} {1}'.format(INSTALL_COMMAND, ' '.join(packages_list))
            subprocess.call(cmd, shell=True)

