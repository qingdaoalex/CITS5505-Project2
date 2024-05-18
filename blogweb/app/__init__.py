from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from app.ssl_handlers import SSLSMTPHandler
from logging.handlers import RotatingFileHandler
import os
from flask_mail import Mail
from config import DeploymentConfig, Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'main.login'
mail = Mail()

def create_app(config_class=DeploymentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    login.init_app(app)
    mail.init_app(app)

    from app.blueprints import main
    app.register_blueprint(main)
    db.init_app(app)
    migrate.init_app(app, db) 
    from .forms import SearchForm
    @app.context_processor
    def inject_search_form():
        return dict(search_form=SearchForm())
    configure_logging(app)
    return app


def configure_logging(app):
    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            mail_handler = SSLSMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], 
                subject='Webapp Failure',
                credentials=auth
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/webapp.log', maxBytes=10240,
                                        backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Webapp startup')


from config import TestConfig  

