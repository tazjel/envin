import logging
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager


class Envin(App):

    log = logging.getLogger(__name__)

    def __init__(self):
        super(Envin, self).__init__(
            description='Environment installer',
            version='0.1',
            command_manager=CommandManager('envin.tools'),
            )

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
