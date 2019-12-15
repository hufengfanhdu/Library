import os
# import datetime
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=7)
    SECRET_KEY = 'Shopping'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    sql_config = 'mysql+mysqlconnector://root:root@127.0.0.1/library'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = sql_config


config = {
    'development': DevelopmentConfig
}
