SASL_PASSWD_FILE = '/etc/postfix/sasl_passwd'
GMAIL_SMTP = 'smtp.gmail.com:587'
GMAIL_SMTP_CREDS = '{} {}:{}'

POSTFIX_CONF_LINES = (
    'relayhost={}'.format(GMAIL_SMTP),
    'smtp_sasl_auth_enable=yes',
    'smtp_sasl_password_maps=hash:{}'.format(SASL_PASSWD_FILE),
    'smtp_sasl_security_options=',
    'smtp_use_tls=yes',
    'smtp_tls_security_level=encrypt',
    'tls_random_source=dev:/dev/urandom')
