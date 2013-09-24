import os
import glob
import shutil
import logging

from cliff.command import Command

logger = logging.getLogger(__name__)


class Dotfiles(Command):
    """ Installs dotfiles to system. """

    def take_action(self, parsed_args):

        self.app.stdout.write('Please specify directory with dotfiles\n')
        dfiles_home = input('Dotfiles dir: ')

        home_dir = os.environ['HOME']
        for f in glob.glob('{0}/_*'.format(dfiles_home)):
            fdest = os.path.join(home_dir, f.replace('_', '.'))
            if os.path.isfile(fdest):
                # backup old configuration file
                logger.info('Backup old {0} file'.format(f))
                shutil.copyfile(f, '{0}.bak'.format(fdest))

            logger.info('Setup {0} configuration file'.format(f))
            os.symlink(os.path.join(os.path.abspath(os.path.dirname(__file__)), f),
                       fdest)

