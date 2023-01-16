from flask import Flask, Blueprint, request, current_app
from flask_cors import CORS
#from OpenSSL import SSL

from . import validate

import pandas as pd

from varmerger import utils

import logging
from logging.config import dictConfig

from werkzeug.exceptions import BadRequest, BadRequestKeyError

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

##############################################
### Routes ###################################
##############################################

### Test route ###
@api.route('/test', methods=methodspermitted)
def test():
    return 'I\'m listening.'

### Run VarGrouper to produce merged VCF ###
@api.route('/phase/<string:build>/merge_vars', methods=methodspermitted)
def merge_vars(build):
    if build.lower() in current_app.phasors.keys():
      phasor = current_app.phasors[build.lower()]
    else:
        pass # return error
    data = request.get_json(silent=False, force=False)
    validate.check_phasing_payload(data)
    if 'mergedist' in data:
      merge_distance = int(data['mergedist'])
    else:
      merge_distance = 999999
    vcfdf = pd.DataFrame.from_dict(data['vcf'])
    dtypes={'chr':'str','pos':'Int64','id':'str','ref':'str','alt':'str'}
    try:
      vcfdf = vcfdf.astype(dtypes)
    except KeyError as e:
      raise BadRequest('Invalid request.')
    validate.check_prephasing_vcf(vcfdf)
    #print(vcfdf)
    # Data checks
    chr = vcfdf.chr.values[0]
    vcfdf.sort_values(by=['chr','pos'],inplace=True)
    # Convert pandas dataframe to list of VCF Records
    vcf_records = utils.df_to_vcf(vcfdf)
    #print(vcf_records)
    mergedf = phasor.merge_phased_vars(vcf_records, merge_distance)
    #print(mergedf)
    # Add warning for merges in which 1 or more variants were skipped
    mergedf['warn'] = mergedf['skipped'].apply(lambda x: 'These variants in the phase group could not be merged and were omitted: ' + ';'.join(x) if x  else None)
    # Drop columns that won't be returned to client
    mergedf.drop(columns=['skipped'], inplace=True, axis=1)
    err = ''
    return utils.package_df(mergedf, err), 200, {'ContentType':'application/json'} 

##############################################
##############################################
##############################################
