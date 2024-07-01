from flask import Blueprint, request, current_app
from flask_cors import CORS
#from OpenSSL import SSL

import logging
from logging.config import dictConfig

from werkzeug.exceptions import BadRequest, BadRequestKeyError, NotFound

from . import service

# Initialize Flask properties from config file

originspermitted=['localhost:80','127.0.0.1:80','0.0.0.0:80','localhost:6666','127.0.0.1:6666','0.0.0.0:6666']
methodspermitted=['POST','GET']

### Declare this blueprint
api = Blueprint(
    'api', __name__
)

### CORS setup
cors = CORS(current_app, resources=current_app.config['CORS_CONFIG_DICT'])

### Error handling ###
@api.errorhandler(BadRequest)
def handle_bad_request(e):
    return 'Invalid request. Check the structure of the payload.', 400

@api.errorhandler(BadRequestKeyError)
def handle_bad_requestkey(e):
    return 'Invalid request. Check that all required keys are present in payload.', 400

@api.errorhandler(NotFound)
def handle_bad_genomic_build(e):
    return str(e), 404

##############################################
### Routes ###################################
##############################################

### Test route ###
@api.route('/test', methods=methodspermitted)
def test():
    return 'I\'m listening.'

### Run VarGrouper to produce merged VCF ###
@api.route('/phase/<string:build>/merge', methods=methodspermitted)
def merge(build):
    data = request.get_json(silent=False, force=False)
    result = service.process_merge(build, data)
    return result, 200, {'ContentType':'application/json'} 

##############################################
##############################################
##############################################
