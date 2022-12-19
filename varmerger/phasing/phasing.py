import numpy as np
import pandas as pd
from celltics.tools import vargroup
from celltics.datasource import datasource, seqrepo
from varmerger import utils

class Phasing:
  def __init__(self, url, build):
    self.datasource = seqrepo.SeqRepo(url, build) # e.g. 'http://127.0.0.1:7777', 'grch37'

  def merge_phased_vars(self, vcf, merge_distance=500):
    vars_skipped, vars_to_group = vargroup.parse_vcf(vcf, merge_distance, None)
    print('vars_skipped:') # TODO if any, need to error out here
    print([vargroup.get_id(v) for v in vars_skipped])
    n_candidates = len(vars_to_group) # For logging
    records, var_dict, skipped = vargroup.bam_and_merge_multiprocess(None, vars_to_group, fq_threshold=0, min_reads=99999, bam_filter_mode='pagb', ref_seq=None, nthreads=1, debug=False, datasource=self.datasource)
    df = utils.vcf_to_df(records)
    df['skipped'] = skipped
    return df
