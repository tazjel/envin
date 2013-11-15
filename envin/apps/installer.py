import os
import sys
import tempfile
import readline
import subprocess
import urllib.request

##TODO: perhaps we should import it form distribute.
from setuptools.archive_util import unpack_archive


class AppInstaller(object):
    """ Base application installer class. """

    requirements = 'requirements.txt'
    install_command = 'sudo apt-get --assume-yes install'

    def _file_path(self, file_name):
        """ Build absolute path to specified filename.

        :param file_name file name
        :type file_name: string
        :returns: abs path to the file
        """

        fpath = sys.modules[self.__module__].__file__
        return os.path.join(os.path.dirname(fpath), file_name)

    def install_packages(self, packages=None):
        """ Install packages from file.

        :param packages: file name where packages located
        :type packages: string
        """

        with open(self._file_path(packages), 'r') as packages:
            packages_list = [p.strip() for p in packages.readlines()]

        if packages_list:
            cmd = '{0} {1}'.format(self.install_command,
                                   ' '.join(packages_list))
            subprocess.call(cmd, shell=True)

    def install_requires(self):
        self.log.info('Installing requirements...')
        self.install_packages(packages=self.requirements)

    def _listdir(self, root):
        """ List directory.

        :param root: directory name
        :type root: string
        :returns: list of contained dirs
        """
        res = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
            res.append(name)
        return res

    def _complete_path(self, path=None):
        """ Perform completion of filesystem path.

        :param path: path to complete
        :type path: string
        :returns list of possible directories
        """

        if not path:
            return self._listdir('.')
        dirname, rest = os.path.split(path)
        tmp = dirname if dirname else '.'
        res = [os.path.join(dirname, p)
               for p in self._listdir(tmp) if p.startswith(rest)]
        # more than one match, or single match which does not exist (typo)
        if len(res) > 1 or not os.path.exists(path):
            return res
        # resolved to a single directory, so return list of files below it
        if os.path.isdir(path):
            return [os.path.join(path, p) for p in self._listdir(path)]
        # exact file match terminates this completion
        return [path + ' ']

    def complete(self, text, state):
        """Generic readline completion entry point."""

        line = readline.get_line_buffer().split()
        results = self._complete_path(path=line[0].strip())
        return results[state]

    def setup_path_complete(self):
        """ Setup tab complition for path. """

        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.complete)

    def _prompt_user(self, app, message, prompt_message, allow_empty=False):
        """ Ask user for input.

        :param app: envin application object
        :type app: object

        :param message: user message
        :type message: string

        :param prompt_message: user prompt message
        :type prompt_message: string

        :param allow_empty: allow user to left empty input
        :type allow_empty: boolean
        """

        user_input = None
        while not user_input:
            app.stdout.write(message)
            user_input = input(prompt_message)
            if allow_empty:
                break

        return user_input

    def download_src(self, url, source=None, archive=True):
        """ Download source and return path to it.

        :param url: url to source distribution
        :type url: string

        :param source_dir: source directory after unpacking (optional)
        :type source_dir: string

        :param archive: is source archive file or not
        :type archive: boolean

        :return: path to source directory
        """
        tmp_dir = tempfile.gettempdir()
        source_file = os.path.join(tmp_dir, url.split('/')[-1])
        urllib.request.urlretrieve(url, source_file)

        if source is None:
            source = source_file

        if archive:
            unpack_archive(source_file, tmp_dir)
            source = os.path.splitext(source)[0]
            if 'tar' in source:
                source = os.path.splitext(source)[0]

        return os.path.join(tmp_dir, source)

    def run(self, argv):
        raise NotImplementedError
