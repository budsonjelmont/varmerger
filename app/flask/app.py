import argparse as ap

from flask import Flask
#from OpenSSL import SSL

from config.config import config 

from extensions import extensions

import logging

# Initialize Flask properties from config file

def create_app(configname='default'):
  app = Flask(__name__, instance_relative_config=False)
  app.config.from_object(config[configname])

  with app.app_context():
    from api.api import api
    app.register_blueprint(api)
    for extension in extensions:
      try:
        extension.init_app(app)
      except Exception as e:
        logging.error(f'Failed to initialize extension: {extension.__name__}')
        logging.error(e)
    return app

if __name__ == '__main__':
  
  parser = ap.ArgumentParser(description='')
  parser.add_argument('configname',type=str,nargs='?',default='default',help='Configuration type to use as specified in config object. Must be "development" or "production".')

  args = parser.parse_args()

  configname = args.configname
  app = create_app(configname)
   
  app.run(host='0.0.0.0')
  #app.run(host='0.0.0.0',ssl_context=context) #TODO
