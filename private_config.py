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
#NOTE: I should modify the database keys at some point too.
LOCAL_DATABASE_URL = 'mysql+mysqldb://elthran:7ArQMuTUSoxXqEfzYfUR@localhost/rpg_database'
SERVER_DATABASE_URL = 'mysql+mysqldb://elthran:7ArQMuTUSoxXqEfzYfUR@elthran.mysql.pythonanywhere-services.com/elthran$rpg_database'
# Should replace on server with custom (not pushed to github).
# import os
# os.urandom(24)
# '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
SECRET_KEY = ']\xf3\xa44\xdc++\x9e\xdd\xa3OR\xd2N\xfc,\x00o\xb6S8]\xcdQ'
PASSWORD_HASH_COST = 10

# UPDATE_INTERVAL = 3600  # One endurance per hour.
UPDATE_INTERVAL = 30  # One endurance per 30 seconds
