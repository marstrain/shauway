import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SUBJECT_PREFIX = '[Shauway]'
    MAIL_SENDER = 'Shauway Admin <admin@cuiwei.vip>'
    ADMIN = os.environ.get('SHAUWAY_ADMIN')

    @staticmethod
    def init_app(app):
        pass
class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'mail.cuiwei.vip'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

DATABASEHOST = "127.0.0.1"
USER = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
DATABASE = "blog"
DATABASEPORT = "3306"
CHARSET = "utf-8"

SERVERPORT = 8080
SERVERHOST = "0.0.0.0"
