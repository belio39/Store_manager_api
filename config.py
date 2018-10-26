# /instance/config.py/

import os

class Config(object):

  DEBUG = True
  CSRF_ENABLED = True
  SECRET = os.getenv('SECRET_KEY')

class DevelopmentConfig(Config):

  DEBUG = True

class TestingConfig(Config):

  TESTING = True
  DEBUG = True

class StagingConfig(Config):

  DEBUG = True

class ProductionConfig(Config):

  DEBUG = True
  TESTING = False

app_config = {
  'development': DevelopmentConfig,
  'testing': TestingConfig,
  'staging': StagingConfig,
  'production': ProductionConfig,
}     


