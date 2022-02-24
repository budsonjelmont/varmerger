from flask import Flask, request, redirect
#from flask_cors import CORS, cross_origin
#from OpenSSL import SSL
import logging

import configparser
import pandas as pd

import utils

### Function defs 

def parse_config(configfile):
  config = configparser.ConfigParser()
  try:
    with open(configfile) as f:
      config.read_file(f)
  except IOError:
    print('ERROR: Could not read config file ' + configfile)
    quit()
  originspermitted = config['ORIGINSPERMITTED']
  methodspermitted = config['METHODSPERMITTED']
  logdir = config['LOGDIR']
  return dirconfig, appconfig, logconfig

# Initialize Flask properties from config file
#....

logdir='/tmp'
logfile='flask.log'

originspermitted=['localhost:80','127.0.0.1:80','0.0.0.0:80','localhost:6666','127.0.0.1:6666','0.0.0.0:6666']
methodspermitted=['POST','GET']

server = Flask(__name__)

# Comment out for development
#logging.basicConfig(filename = logdir + '/' + logfile, level = logging.DEBUG, format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

### Test route ###
@server.route('/test', methods=methodspermitted)
def test():
    return 'I\'m listening.'

### Run VarGrouper to produce merged VCF ###
@server.route('/merge_variants', methods=methodspermitted)
def merge_variants():
    data = request.get_json(silent=False, force=False)
    print(data)
    build = data['build']
    vcfdf = pd.DataFrame.from_dict(data['vcf']) 
    dtypes={'chr':'str','pos':'Int64','ref':'str','alt':'str'}
    vcfdf = vcfdf.astype(dtypes)
    print(vcfdf)
    # Data checks
    # No NULL values in df
    if vcfdf.isnull().values.any():
        print("ERROR NULLS")
    # All variants are on the same chromosome 
    if len(vcfdf.chr.unique()) > 1:
        print("ERROR CHR")
    else:
        chr = vcfdf.chr.values[0]
    vcfdf.sort_values(by=['chr','pos'],inplace=True)
    # Convert pandas dataframe to list of VCF Records
    vcf_records = utils.df_to_vcf(vcfdf)
    utils.merge_phased_vars(vcf_records)
    # After varGrp
    #   Check if all have IN_GROUP key & value in INFO field
    #   Look for VCF call that matches IN_GROUP value chr & pos & has lowercase letters
    #       # Consider modifying varGrouper to populate GROUP_ID tag & use this to find merged VCF instead 
    #status_code=200
    #headers={}
    #headers['Content-Type']='application/json'
    #headers['Errors'] = datetime.now()
    #response=Response(jpg_as_text,status_code,headers)
    #return response
    return 'MERGE'

##############################################

#context=(cer,key)
if __name__ == '__main__':
  server.run(host='0.0.0.0')
  #server.run(host='0.0.0.0',ssl_context=context)
