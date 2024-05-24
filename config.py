# Configuration file
# AFRILOG SARL
# config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    COMPANY_CEO = os.environ.get('COMPANY_CEO')
    COMPANY_CEO_ASSISTANT = os.environ.get('COMPANY_CEO_ASSISTANT')
    COMPANY_HR_MANAGER = os.environ.get('COMPANY_HR_MANAGER')
    COMPANY_PROJECT_MANAGER = os.environ.get('COMPANY_PROJECT_MANAGER')
    COMPANY_SALES_MANAGER = os.environ.get('COMPANY_SALES_MANAGER')
    COMPANY_IT_ADMINISTRATOR = os.environ.get('COMPANY_IT_ADMINISTRATOR') 
    COMPANY_ACCOUNTANT = os.environ.get('COMPANY_ACCOUNTANT')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
