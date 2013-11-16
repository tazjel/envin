import logging
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager


class Envin(App):
    """ Envin is environment installer.

    This applications aims to help user to compile different tools and
    applications with custom configuraiton and in custom location.
    """

    log = logging.getLogger(__name__)

    def __init__(self):
        cmanager = CommandManager('envin.commands')
        self.app_cmd_manager = CommandManager('envin.apps')
        super(Envin, self).__init__(description=self.__doc__,
                                    version='0.1',
                                    command_manager=cmanager,)

    def initialize_app(self, argv):
        pass

    def prepare_to_run_command(self, cmd):
        pass

    def clean_up(self, cmd, result, err):
        pass


def main(argv=sys.argv[1:]):
    myapp = Envin()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
