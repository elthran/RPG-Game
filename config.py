"""
NOTE: this file should be hidden and added to .gitignore!
"""

# Mail config
# MAIL_SERVER = 'localhost'  # default ‘localhost’
# MAIL_PORT = 25  # default 25
# MAIL_USE_TLS = True  # default False
# MAIL_USE_SSL = True  # default False
# MAIL_DEBUG : default app.debug
# MAIL_USERNAME : default None
# MAIL_PASSWORD : default None
# MAIL_DEFAULT_SENDER : default None
# MAIL_MAX_EMAILS : default None
# MAIL_SUPPRESS_SEND : default app.testing
# MAIL_ASCII_ATTACHMENTS : default False

SENDGRID_API_KEY = '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'
LOCAL_DATABASE_URL = 'mysql+mysqldb://elthran:7ArQMuTUSoxXqEfzYfUR@localhost/rpg_database'
SERVER_DATABASE_URL = 'mysql+mysqldb://elthran:7ArQMuTUSoxXqEfzYfUR@elthran.mysql.pythonanywhere-services.com/elthran$rpg_database'
SECRET_KEY = "\xd0'\xb99g\xff\xda\x98)Czp\xfe\xd7\x07_\xa1\x85\xc7\xe8\x8c\x1b}\x0f"
PASSWORD_HASH_COST = 10

# UPDATE_INTERVAL = 3600  # One endurance per hour.
UPDATE_INTERVAL = 30  # One endurance per 30 seconds
