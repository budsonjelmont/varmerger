import numpy as np
import pandas as pd
from celltics.tools import vargroup
#import celltics
import vcf

def df_to_vcf(df):
  vcfreader = vcf.parser.Reader('nofile')
  reqdcols=['chr','pos','id','ref','alt','qual','filter','info','format']
  missingcols = [col for col in reqdcols if col  not in list(df.columns)]
  print(missingcols)
  df[missingcols] = '.'
  print(df.columns)
  print(df)
  return df.apply(lambda x: vcf.model._Record(x.chr, x.pos, x.id, x.ref, [vcfreader._parse_alt(x.alt)], x.qual, x.filter, x.info, x.format, sample_indexes=None, samples=None), axis=1).values.tolist()

def merge_phased_vars(vcf):
  vars_skipped, vars_to_group = vargroup.parse_vcf(vcf, merge_distance, None)
  print(vars_skipped) # if any, need to error out here
  print(vars_to_group)
  n_candidates = len(vars_to_group) # For logging
  records, var_dict = vargroup.bam_and_merge_multiprocess(None, vars_to_group, fq_threshold=0, min_reads=99999, bam_filter_mode='pagb', ref_seq=None, nthreads=10, debug=False)
  print(records)
  print(var_dict)


vcffile='/mnt/c/Users/judson.x.belmont/Documents/Code/varwrangler/test/data/test_2.sort.vcf'
merge_distance=99999999

#with open(vcffile, 'r') as openfile:
#  reader = vcf.Reader(openfile)
#  original_variants = list(reader)
#  print(type(original_variants))
#  vars_skipped, vars_to_group = vargroup.parse_vcf(original_variants, merge_distance, None)
#  print(vars_skipped)
#  print(vars_to_group)
