import numpy as np
import pandas as pd
from celltics.tools import vargroup, datasource
#import celltics
import vcf
from vcf import utils

def trim_common_prefix(*sequences):
  if not sequences:
    return []
  reverses = [seq[::-1] for seq in sequences]
  rev_min = min(reverses)
  rev_max = max(reverses)
  if len(rev_min) < 2:
    return sequences
  for i, c in enumerate(rev_min[:-1]):
    if c != rev_max[i]:
      if i == 0:
        return sequences
      return [seq[:-i] for seq in sequences]
    return [seq[:-(i + 1)] for seq in sequences]

def df_to_vcf(df, l_trim=True, r_trim=True):
  vcfreader = vcf.parser.Reader('nofile')
  reqdcols=['chr','pos','id','ref','alt','qual','filter','info','format']
  missingcols = [col for col in reqdcols if col not in list(df.columns)]
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
  # Rewrite '.' in ALT field
  df['alt'] = df['alt'].replace({'.':None}).fillna(df['ref'])
  # Perform left- and right-trimmming, if requested
  print(df)
  if r_trim:
    df['ref'],df['alt'] = zip(*df.apply(lambda x: utils.trim_common_suffix(x['ref'],x['alt']), axis=1))
  if l_trim:
    rng = np.random.default_rng()
    ref_tmp_col = 'ref_' + str(rng.integers(low=0, high=77777777777, size=None, dtype=np.int64)) 
    alt_tmp_col = 'alt_' + str(rng.integers(low=0, high=77777777777, size=None, dtype=np.int64)) 
    df[ref_tmp_col], df[alt_tmp_col] = zip(*df.apply(lambda x: utils.trim_common_suffix(x['ref'][::-1],x['alt'][::-1]), axis=1))
    # Adjust POS for any rows that were left-trimmed
    df['pos'] = df['pos'] + (df['ref'].str.len() - df[ref_tmp_col].str.len())
    # Assign new REF & ALT alleles
    # TODO REF & ALT trimming below works, but vectorized doesn't
    df['ref'] = df.apply(lambda x: x['ref'][len(x['ref']) - len(x[ref_tmp_col]):], axis=1)
    df['alt'] = df.apply(lambda x: x['alt'][len(x['alt']) - len(x[alt_tmp_col]):], axis=1)
    print(df['ref'].str.len())
    print(df[ref_tmp_col].str.len())
    #print(df['ref'].str.len() - df[ref_tmp_col].str.len())
    print(df['ref'].str.slice(df['ref'].str.len() - df[ref_tmp_col].str.len(),))
    #df['ref'] = df['ref'].str[(df['ref'].str.len() - df[ref_tmp_col].str.len()):]
    #df['alt'] = df['alt'].str[(df['alt'].str.len() - df[alt_tmp_col].str.len()):]
    # Re-sort dataframe
    df.sort_values('pos', ascending=True, inplace=True)
    print(df)
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
  records, var_dict, skipped = vargroup.bam_and_merge_multiprocess(None, vars_to_group, fq_threshold=0, min_reads=99999, bam_filter_mode='pagb', ref_seq=None, nthreads=1, debug=False, datasource=sr)
  df = vcf_to_df(records)
  df['skipped'] = skipped
  return df

def package_df(df, err):
    payload = {'result': df.to_dict(orient='records'), 'err': err}
    return payload
