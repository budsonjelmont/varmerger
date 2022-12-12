from os import path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

default_phase_config = {
 'handlers':
 {
    'grch37':
     {
       'name': 'seqrepo_grch37',
       'build': 'grch37',
       'url': 'http://127.0.0.1:7777'
     },
    'grch38':
    {
      'name': 'seqrepo_grch38',
      'build': 'grch38',
      'url': 'http://127.0.0.1:7777'
    }
  }
}

default_logging_config = {
  'version': 1,
  'formatters':
  {
    'default':
      {'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'}
  },
  'handlers':
  {
    'console':
    {
	'level': 'INFO',
	'class': 'logging.StreamHandler',
	'stream': 'ext://sys.stdout',
	'formatter': 'default'
    },
    'file':
    {
	'level': 'DEBUG',
	'class': 'logging.FileHandler',
	'filename': '/tmp/varmerger.log',
	'formatter': 'default'
    }
  },
  'root':{
      'level': 'INFO',
      'handlers':
      {
	 'console',
	 'file'
      }
  }
}

class Config:
    
    # Default settings
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    # TODO check env var to determine if configs should be read from an external file instead
    LOG_CONFIG = default_logging_config
    PHASE_CONFIG = default_phase_config

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    FLASK_ENV = 'production'


config = {
  'development': DevelopmentConfig,
  'production': ProductionConfig,
  'default': DevelopmentConfig,
}
