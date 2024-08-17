import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 6

    # Mail configuration
    MAIL_SERVER = ''
    MAIL_PORT = 
    MAIL_USE_SSL = 
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    ADMINS = ['']
    # Upload configuration
    UPLOAD_PATH = os.path.join(basedir, 'app', 'static', 'avatar')
    MAX_FILE_SIZE_BYTES = 500 * 1024

class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
