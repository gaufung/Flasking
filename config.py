import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDONW = True
    FALSKY_POST_PER_PAGE = 10
    FLASKY_MAIL_SUBJECT_PREFIX = '[FLASKY]'
    SQLALCHEMY_RECORD_QUERIES=True
    FLASKY_DB_QUERY_TIMEOUT=0.5
    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 25
    MAIL_USERNAME='gaofengcumt@126.com'
    MAIL_PASSWORD = 'gaofeng126123'
    FLASKY_MAIL_SENDER = 'FLASKY Admin <gaofengcumt@126.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 25
    MAIL_USE_LTS = True
    MAIL_USERNAME= os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:admin@localhost/dev'

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLE=False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:admin@localhost/test'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:admin@localhost/prodution'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX+' Application Error',
            credentials=credentials,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


config= {
    'development': DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}