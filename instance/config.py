import os

class Config(object):
    #parent configuration class
    DEBUG= False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

class DevelopmentConfig(Config):
    #configuration for development
    DEBUG = False

class TestingConfig(Config):
    #Configuration for Testing with a separate test database
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/test_db"
    DEBUG = True

class StagingConfig(Config):
    #configuration for staging
    DEBUG = True

class ProductionConfig(Config):
    # Configuration for production.
    DEBUG = False
    TESTING = False

app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
}