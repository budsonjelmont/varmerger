from flask import Flask, request
#from flask_cors import CORS, cross_origin
#from OpenSSL import SSL
import logging

import configparser
import pandas as pd

import utils
import phasing

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

# Directory containing sequence resources
seqdir='TODO'

# Comment out for development
#logging.basicConfig(filename = logdir + '/' + logfile, level = logging.DEBUG, format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

### Test route ###
@server.route('/test', methods=methodspermitted)
def test():
    return 'I\'m listening.'

### Run VarGrouper to produce merged VCF ###
@server.route('/merge_variants', methods=methodspermitted)
def merge_variants():
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    data = request.get_json(silent=False, force=False)
    build = data['build']
    merge_distance = 99999 # TODO make this part of payload
    vcfdf = pd.DataFrame.from_dict(data['vcf'])
    dtypes={'chr':'str','pos':'Int64','id':'str','ref':'str','alt':'str'}
    vcfdf = vcfdf.astype(dtypes)
    #print(vcfdf)
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
    #print(vcf_records)
    mergedf = utils.merge_phased_vars(vcf_records, build, merge_distance)
    print(mergedf)
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

#context=(cer,key)
if __name__ == '__main__':
  server.run(host='0.0.0.0')
  #server.run(host='0.0.0.0',ssl_context=context)
