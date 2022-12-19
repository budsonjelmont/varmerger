import argparse as ap

from flask import Flask, request
#from flask_cors import CORS, cross_origin
#from OpenSSL import SSL

from config.config import config 

from extensions import extensions

import logging

# Initialize Flask properties from config file

originspermitted=['localhost:80','127.0.0.1:80','0.0.0.0:80','localhost:6666','127.0.0.1:6666','0.0.0.0:6666']
methodspermitted=['POST','GET']

def create_app(configname='default'):
  app = Flask(__name__, instance_relative_config=False)
  app.config.from_object(config[configname])

  #logging.config.dictConfig(app.config['LOG_CONFIG'])

  with app.app_context():
    from api.api import api
    app.register_blueprint(api)
    for extension in extensions:
      extension.init_app(app)
    return app

if __name__ == '__main__':
  
  parser = ap.ArgumentParser(description='')
  parser.add_argument('configname',type=str,nargs='?',help='Configuration type to use as specified in config object. Must be "development" or "production".')

  args = parser.parse_args()

  configname = args.configname
  app = create_app(configname)
   
  app.run(host='0.0.0.0')
  #app.run(host='0.0.0.0',ssl_context=context) #TODO
