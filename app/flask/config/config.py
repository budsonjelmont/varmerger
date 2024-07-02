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
  except IOError as e:
    # TODO: log error
    print('ERROR: Could not read config file ' + yamlfile)
    quit()

class Config:
    
  # Default settings
  ENV = 'development'
  DEBUG = False
  TESTING = False
  DEFAULT_LOG_CONFIG_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
	'standard': {
	    'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
	},
    },
    'handlers': {
	'default': {
	    'level': 'INFO',
	    'formatter': 'standard',
	    'class': 'logging.StreamHandler',
	}
    },
    'loggers': {
	'': {
	    'handlers': ['default'],
	    'level': 'INFO',
	    'propagate': True
	},
    }
  }
  DEFAULT_CORS_CONFIG_DICT = {'/phase/*':{'origins':['*']}}
  # If a path to a config .yaml was passed, read in config values from there 
  LOG_CONFIG_YAML_PATH = getenv('LOG_CONFIG_YAML_PATH')
  if LOG_CONFIG_YAML_PATH:
    LOG_CONFIG_DICT = read_yaml(LOG_CONFIG_YAML_PATH)
  else:
     LOG_CONFIG_DICT = DEFAULT_LOG_CONFIG_DICT
  PHASE_CONFIG_YAML_PATH = getenv('PHASE_CONFIG_YAML_PATH')
  if PHASE_CONFIG_YAML_PATH:
     PHASE_CONFIG_DICT = read_yaml(PHASE_CONFIG_YAML_PATH)
  else:
     PHASE_CONFIG_DICT = None
  CORS_CONFIG_YAML_PATH = getenv('CORS_CONFIG_YAML_PATH')
  if CORS_CONFIG_YAML_PATH:
     CORS_CONFIG_DICT = read_yaml(CORS_CONFIG_YAML_PATH)
  else:
     CORS_CONFIG_DICT = DEFAULT_CORS_CONFIG_DICT

class DevelopmentConfig(Config):
  
  DEBUG = True

class TestingConfig(Config):
    
  TESTING = True

class ProductionConfig(Config):
     
  ENV = 'production'

config = {
  'development': DevelopmentConfig,
  'dev': DevelopmentConfig,
  'production': ProductionConfig,
  'prod': ProductionConfig,
  'default': DevelopmentConfig
}
