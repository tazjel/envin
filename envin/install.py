import sys

from cliff.command import Command


class Install(Command):
    """ Installs specified application """

    def get_parser(self, prog_name):
        parser = super(Install, self).get_parser(prog_name)
        parser.add_argument('app',
                            nargs='*',
                            help='name of the application installer',
                            )
        return parser

    def take_action(self, parsed_args):
        if parsed_args.app:
            app = self.app.app_cmd_manager.find_command(parsed_args.app)
            app_factory, app_name, search_args = app
            app_installer = app_factory(self.app, search_args)
            app_installer.run()
            return 0
        else:
            cmd_parser = self.get_parser(' '.join([self.app.NAME, 'install']))
            cmd_parser.print_help(self.app.stdout)
            self.app.stdout.write('\nApp installers:\n')
            app_manager = self.app.app_cmd_manager
            for name, ep in sorted(app_manager):
                try:
                    factory = ep.load()
                except Exception as err:
                    self.app.stdout.write('Could not load %r\n' % ep)
                    continue
                try:
                    cmd = factory(self, None)
                except Exception as err:
                    self.app.stdout.write('Could not instantiate %r: %s\n' % (ep, err))
                    continue
                one_liner = cmd.get_description().split('\n')[0]
                self.app.stdout.write('  %-13s  %s\n' % (name, one_liner))
            sys.exit(0)
        return 0
