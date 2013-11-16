import logging
import getpass
import subprocess

from . import config
from ..installer import AppInstaller


class Postfix(AppInstaller):
    """ Postfix installer. """

    log = logging.getLogger(__name__)

    def get_gmail_creds(self):
        """ Ask user to provide gmail relayhost. """

        self.app.stdout.write(('Please provide credentials to your gmail '
                               'account, if you want to use gmail smtp '
                               'as relayhost. Leave them blank in other '
                               'case.\n'))

        umsg = 'Please provide your username.\n'
        uprompt_msg = 'User name:'
        username = self._prompt_user(umsg, uprompt_msg, allow_empty=True)
        if username:
            passwd = getpass.getpass()

        if username and passwd:
            return username, passwd

    def configure_postfix(self):
        """ Configure postfix server."""

        username, passwd = self.get_gmail_creds()
        if username and passwd:
            cmd = 'sudo sh -c "echo {} > {}"'.format(
                config.GMAIL_SMTP_CREDS.format(config.GMAIL_SMTP, username,
                                               passwd),
                config.SASL_PASSWD_FILE)
            subprocess.call(cmd, shell=True)
            subprocess.call('sudo postmap {}'.format(config.SASL_PASSWD_FILE),
                           shell=True)

        for conf_line in config.POSTFIX_CONF_LINES:
            subprocess.call('sudo postconf -e {}'.format(conf_line),
                            shell=True)

    def run(self):
        """ Install and configure postfix. """

        self.install_requires()
        self.configure_postfix()
        subprocess.call('sudo service postfix restart', shell=True)
