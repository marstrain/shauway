import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "youwillnotknowaboutit"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SUBJECT_PREFIX = '[Shauway]'
    MAIL_SENDER = 'NO REPLY <noreply@cuiwei.vip>'
    ADMIN = os.environ.get('SHAUWAY_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    MAIL_SERVER = '127.0.0.1'
    MAIL_PORT = 465
    #MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    USER = os.environ.get('USERNAME') or "cmail"
    PASSWORD = os.environ.get('PASSWORD') or "cmail2017GO"
    DATABASE = "blog_dev"
    DATABASEPORT = "3306"
    CHARSET = "utf-8"
    DATABASEHOST = "localhost"
    DIALECT = "mysql"
    DRIVER = "pymysql"
    SQLALCHEMY_DATABASE_URI =\
        "{}+{}://{}:{}@{}:{}/{}?charset=utf8"\
            .format(DIALECT,DRIVER,USER,PASSWORD,DATABASEHOST,DATABASEPORT,DATABASE)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    USER = os.environ.get('USERNAME')
    PASSWORD = os.environ.get('PASSWORD')
    DATABASE = "blog"
    DATABASEPORT = "3306"
    CHARSET = "utf-8"
    DATABASEHOST = "localhost"
    SQLALCHEMY_DATABASE_URI =\
        "mysql://USER:PASSWORD@DATABASEHOST:DATABASEPORT/blog"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

