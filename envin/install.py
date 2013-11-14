from cliff.command import Command


class Install(Command):
    """ Installs specified application """

    def get_parser(self, prog_name):
        parser = super(Install, self).get_parser(prog_name)
        parser.add_argument('app',
                            nargs='*',
                            help='name of the application',
                            )
        return parser

    def take_action(self, parsed_args):
        if parsed_args.app:
            app = self.app.app_cmd_manager.find_command(parsed_args.app)
            app_factory, app_name, search_args = app
            app_installer = app_factory()
            app_installer.run(self.app, search_args)
            return 0
        else:
            cmd_parser = self.get_parser(' '.join([self.app.NAME, 'install']))
        cmd_parser.print_help(self.app.stdout)
        return 0
