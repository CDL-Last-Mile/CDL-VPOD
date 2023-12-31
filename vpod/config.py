import os
from dotenv import load_dotenv

# os.environ["WERKZEUG_RUN_MAIN"] = "true"
load_dotenv()

support = []
for r in  os.getenv('SUPPORT').split(','):
    support.append(str(r))

recipients = []
for r in  os.getenv('ADMINS').split(','):
    recipients.append(str(r))

client_master_list = []
for r in  os.getenv("CLIENT_LIST").split(','):
    client_master_list.append(str(r))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.office365.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.getenv("EMAIL")
    MAIL_DEFAULT_SENDER = os.getenv("EMAIL")
    MAIL_PASSWORD = os.getenv("MAIL_PASS")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    RECIPIENTS = recipients
    SUPPORT = support
    SECRET_KEY = "xc8xa9xe3xccx84qxc5xddTWxe9xf4xa6Dxaexcfxed7xe1x9bx10xfb"
    CLIENT_LIST = client_master_list
   

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")


class ProductionConfig(Config):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") 
   


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

config = config[os.getenv('FLASK_ENV')]