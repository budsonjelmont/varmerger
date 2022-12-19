from os import path, getenv
from dotenv import load_dotenv

from yaml import safe_load

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
    
def read_yaml(yamlfile):
  try:
    with open(yamlfile) as f:
      configdict = safe_load(f)
    return configdict
  except IOError:
    print('ERROR: Could not read config file ' + yamlfile)
    quit()

class Config:
    
  # Default settings
  FLASK_ENV = 'development'
  DEBUG = False
  TESTING = False
  # If a path to a config .yaml was passed, read in config values from there 
  LOG_CONFIG_YAML_PATH = getenv('LOG_CONFIG_YAML_PATH')
  if LOG_CONFIG_YAML_PATH:
    LOG_CONFIG_DICT = read_yaml(LOG_CONFIG_YAML_PATH)
  else:
     LOG_CONFIG_DICT = None
  PHASE_CONFIG_YAML_PATH = getenv('PHASE_CONFIG_YAML_PATH')
  if PHASE_CONFIG_YAML_PATH:
     PHASE_CONFIG_DICT = read_yaml(PHASE_CONFIG_YAML_PATH)
  else:
     PHASE_CONFIG_DICT = None

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    FLASK_ENV = 'production'


config = {
  'development': DevelopmentConfig,
  'dev': DevelopmentConfig,
  'production': ProductionConfig,
  'prod': ProductionConfig,
  'default': DevelopmentConfig
}
