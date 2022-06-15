import argparse as ap

from flask import Flask, request
#from flask_cors import CORS, cross_origin
#from OpenSSL import SSL

from yaml import safe_load

import pandas as pd

from varchemist import utils
from varchemist import phasing

import logging
from logging.config import dictConfig

from werkzeug.exceptions import BadRequest, BadRequestKeyError

### Function defs ### TODO move to another module 

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
        print(logconfig)
        logging.config.dictConfig(logconfig)
    except IOError:
      print('ERROR: Could not read config file ' + configfile)
      quit()
    logging.config.dictConfig(logconfig)

def check_phasing_payload(payload):
    reqdkeys = ['build','vcf']
    if not all(key in payload for key in reqdkeys):
      raise BadRequestKeyError('Invalid request.')
    build = payload['build']
    if 'mergedist' in payload:
        try:
          int(payload['mergedist'])
        except ValueError as e:
          raise BadRequest('Invalid request.')

def check_prephasing_vcf(vcfdf):
  # Check for NULL values in df, that all variants are on the same chromosome, and that more than one variant was passed in
  if vcfdf.isnull().values.any() or len(vcfdf.chr.unique()) > 1 or vcfdf.shape[0] == 1:
    raise BadRequest('Invalid request.')

# Initialize Flask properties from config file

originspermitted=['localhost:80','127.0.0.1:80','0.0.0.0:80','localhost:6666','127.0.0.1:6666','0.0.0.0:6666']
methodspermitted=['POST','GET']

app = Flask(__name__)

### Error handling ###
@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return 'Invalid request. Check the structure of the payload.', 400

@app.errorhandler(BadRequestKeyError)
def handle_bad_requestkey(e):
    return 'Invalid request. Check that all required keys are present in payload.', 400

##############################################
### Routes ###################################
##############################################

### Test route ###
@app.route('/test', methods=methodspermitted)
def test():
    return 'I\'m listening.'

### Run VarGrouper to produce merged VCF ###
@app.route('/merge_variants', methods=methodspermitted)
def merge_variants():
    data = request.get_json(silent=False, force=False)
    check_phasing_payload(data)
    build = data['build']
    if 'mergedist' in data:
      merge_distance = int(data['mergedist'])
    else:
      merge_distance = 999999
    vcfdf = pd.DataFrame.from_dict(data['vcf'])
    dtypes={'chr':'str','pos':'Int64','id':'str','ref':'str','alt':'str'}
    vcfdf = vcfdf.astype(dtypes)
    check_prephasing_vcf(vcfdf)
    #print(vcfdf)
    # Data checks
    chr = vcfdf.chr.values[0]
    vcfdf.sort_values(by=['chr','pos'],inplace=True)
    # Convert pandas dataframe to list of VCF Records
    vcf_records = utils.df_to_vcf(vcfdf)
    #print(vcf_records)
    mergedf = phasing.merge_phased_vars(vcf_records, build, merge_distance)
    #print(mergedf)
    # Add warning for merges in which 1 or more variants were skipped
    mergedf['warn'] = mergedf['skipped'].apply(lambda x: 'These variants in the phase group could not be merged and were omitted: ' + ';'.join(x) if x  else None)
    # Drop columns that won't be returned to client
    mergedf.drop(columns=['skipped'], inplace=True, axis=1)
    err = ''
    resjson = utils.package_df(mergedf, err)
    print(resjson)
    rescode = 200
    return resjson, rescode, {'ContentType':'application/json'}

##############################################
##############################################
##############################################

#context=(cer,key)
if __name__ == '__main__':
  
  parser = ap.ArgumentParser(description='')
  parser.add_argument('logconfigfile',type=str,nargs='?',help='YAML file containing the logging configuration parameters.')

  args = parser.parse_args()

  logconfigfile = args.logconfigfile
  
  setup_logging(logconfigfile)
  app.run(host='0.0.0.0')
  #app.run(host='0.0.0.0',ssl_context=context)
