import argparse as ap

from flask import Flask, request
#from flask_cors import CORS, cross_origin
#from OpenSSL import SSL

from varmerger import phasing

from yaml import safe_load

import logging
from logging.config import dictConfig

### Setup functions ### 

def setup_logging(configfile):
  if configfile is None:
    logging.basicConfig(
      level=logging.DEBUG,
      format='%(asctime)s %(message)s',
      handlers=[logging.StreamHandler()]
    )
  else:
    try:
      with open(configfile) as f:
        logconfig = safe_load(f)
        #print(logconfig)
        logging.config.dictConfig(logconfig)
    except IOError:
      print('ERROR: Could not read config file ' + configfile)
      quit()
    logging.config.dictConfig(logconfig)

def setup_phasing(configfile):
  phasors = {}
  if configfile is None:
    pass
  else:
    with open(configfile) as f:
      phaseconfig = safe_load(f)
      for k,v in phaseconfig['handlers'].items():
        phasors[k] = phasing.Phasing(v['url'],v['build'])
  return phasors

# Initialize Flask properties from config file

originspermitted=['localhost:80','127.0.0.1:80','0.0.0.0:80','localhost:6666','127.0.0.1:6666','0.0.0.0:6666']
methodspermitted=['POST','GET']

phasors = {}

def init_app(logconfigfile, phaseconfigfile):
  """Initialize the application."""
  app = Flask(__name__, instance_relative_config=False)
  #app.config.from_object('config.Config')

  with app.app_context():
    setup_logging(logconfigfile)
    from api.api import api
    app.register_blueprint(api)
    app.phasors = setup_phasing(phaseconfigfile)
    return app

if __name__ == '__main__':
  
  parser = ap.ArgumentParser(description='')
  parser.add_argument('logconfigfile',type=str,nargs='?',help='YAML file containing the logging configuration parameters.')
  parser.add_argument('phaseconfigfile',type=str,nargs='?',help='YAML file containing the phasing configuration parameters.')

  args = parser.parse_args()

  logconfigfile = args.logconfigfile
  phaseconfigfile = args.phaseconfigfile
  
  setup_logging(logconfigfile)
  setup_phasing(phaseconfigfile)

  app.run(host='0.0.0.0')
  #app.run(host='0.0.0.0',ssl_context=context) #TODO
