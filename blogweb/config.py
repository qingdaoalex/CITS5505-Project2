import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # Mail configuration
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'cits5505webapp@qq.com'
    MAIL_PASSWORD = 'woddizqutfukcjja'
    MAIL_USE_TLS = False
    MAIL_USE_TLS = True
    ADMINS = ['cits5505webapp@qq.com']