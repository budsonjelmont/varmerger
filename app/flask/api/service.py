from flask import current_app
#from OpenSSL import SSL

from . import validate

import pandas as pd

from varmerger import utils

import logging
from logging.config import dictConfig

from werkzeug.exceptions import BadRequest, BadRequestKeyError, NotFound

def process_merge(build, data):
    if build.lower() not in current_app.phasors.keys():
        raise NotFound('No phase handler was found for genomic build ' + build + '.')
    
    phasor = current_app.phasors[build.lower()]
    validate.check_phasing_payload(data)
    
    merge_distance = int(data.get('mergedist', 999999))
    vcfdf = pd.DataFrame.from_dict(data['vcf'])
    dtypes = {'chr': 'str', 'pos': 'Int64', 'id': 'str', 'ref': 'str', 'alt': 'str'}
    
    try: # TODO either move this to validate or move everything from validate to here
        vcfdf = vcfdf.astype(dtypes)
    except KeyError as e:
        raise BadRequest
    
    validate.check_prephasing_vcf(vcfdf)

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
    return utils.package_df(mergedf, err)