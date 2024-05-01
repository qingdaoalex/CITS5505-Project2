import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or "smtp.qq.com"
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_DEBUG = os.environ.get('MAIL_DEBUG') == 'True'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "3357763382@qq.com"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or "woddizqutfukcjja"
    # MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or "qq邮箱"
    ADMINS = ['cits5505webapp@qq.com']