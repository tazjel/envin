SASL_PASSWD_FILE = '/etc/postfix/sasl_passwd'
GMAIL_SMTP = 'smtp.gmail.com:587'
GMAIL_SMTP_CREDS = '{} {}:{}'

POSTFIX_CONF_LINES = (
    'relayhost={}'.format(GMAIL_SMTP),
    'inet_interfaces=all',
    'smtp_sasl_auth_enable=yes',
    'smtp_sasl_password_maps=hash:{}'.format(SASL_PASSWD_FILE),
    'smtp_sasl_security_options=',
    'smtp_use_tls=yes',
    'smtp_tls_security_level=encrypt',
    'tls_random_source=dev:/dev/urandom')

SASLAUTHD = """
# This needs to be uncommented before saslauthd will be run automatically
START=yes

PWDIR="/var/spool/postfix/var/run/saslauthd"
PARAMS="-m ${PWDIR}"
PIDFILE="${PWDIR}/saslauthd.pid"

# You must specify the authentication mechanisms you wish to use.
# This defaults to "pam" for PAM support, but may also include
# "shadow" or "sasldb", like this:
# MECHANISMS="pam shadow"

MECHANISMS="pam"

# Other options (default: -c)
# See the saslauthd man page for information about these options.
#
# Example for postfix users: "-c -m /var/spool/postfix/var/run/saslauthd"
# Note: See /usr/share/doc/sasl2-bin/README.Debian
#OPTIONS="-c"

#make sure you set the options here otherwise it ignores params above and will not work
OPTIONS="-c -m /var/spool/postfix/var/run/saslauthd"
"""
SASLAUTHD_FILE = "/etc/default/saslauthd"
SASLAUTHD_OVERRIDE_CMD = ("sudo dpkg-statoverride --force --update --add root "
                          "sasl 755 /var/spool/postfix/var/run/saslauthd")
