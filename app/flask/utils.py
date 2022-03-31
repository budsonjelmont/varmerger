import numpy as np
import pandas as pd
from celltics.tools import vargroup, datasource
#import celltics
import vcf

def df_to_vcf(df):
  vcfreader = vcf.parser.Reader('nofile')
  reqdcols=['chr','pos','id','ref','alt','qual','filter','info','format']
  missingcols = [col for col in reqdcols if col  not in list(df.columns)]
  df[missingcols] = '.'
  # Troubleshooting: print all methods of vcf reader object:
  #object_methods = [method_name for method_name in dir(vcfreader) if callable(getattr(vcfreader, method_name))]
  #print(object_methods)
  # Special handling for qual column
  try:
    df['qual'] = df['qual'].astype(int)
  except ValueError as e:
    try:
        df['qual'] = df['qual'].astype(float)
    except ValueError as e:
        df['qual'] = None
  # Special handling for filter column
  # TODO enable handling for non-empty FORMAT column
  if (df['format'] == '.').all():
    df['format'] = None
  elif (df['format'] == '.').any():
    print('ERROR: Inconsistent entries in \'FORMAT\' field.')
  #print(df)
  return df.apply(lambda x: vcf.model._Record(x['chr'], x['pos'], x['id'], x['ref'], [vcfreader._parse_alt(x['alt'])], x['qual'], x['filter'], vcfreader._parse_info(x['info']), None, sample_indexes=None, samples=None), axis=1).values.tolist()

def vcf_to_df(vcf):
    # TODO this method doesn't properly handle QUAL or INFO fields
    df = pd.DataFrame([{'chr': var.CHROM, 'pos': var.POS, 'id': var.ID, 'ref': var.REF, 'alt': ','.join([str(alt) for alt in var.ALT]), 'qual': var.QUAL, 'filter': var.FILTER, 'info': None, 'format': var.FORMAT} for var in vcf])
    #print(df)
    return df

def merge_phased_vars(vcf, build, merge_distance=500):
  # TODO payload check
  vars_skipped, vars_to_group = vargroup.parse_vcf(vcf, merge_distance, None)
  print('vars_skipped:') # if any, need to error out here
  print([vargroup.get_id(v) for v in vars_skipped])
  n_candidates = len(vars_to_group) # For logging
  sr = datasource.SeqRepo('http://127.0.0.1:7777', build)
  records, var_dict = vargroup.bam_and_merge_multiprocess(None, vars_to_group, fq_threshold=0, min_reads=99999, bam_filter_mode='pagb', ref_seq=None, nthreads=1, debug=False, datasource=sr)
  df = vcf_to_df(records)
  return df

def package_df(df, err):
    payload = {'result': df.to_dict(orient='records'), 'err': err}
    return payload
