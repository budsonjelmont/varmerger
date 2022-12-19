import pandas as pd

def check_phasing_payload(payload):
    reqdkeys = ['vcf']
    if not all(key in payload for key in reqdkeys):
      raise BadRequestKeyError('Invalid request.')
    if 'mergedist' in payload:
        try:
          int(payload['mergedist'])
        except ValueError as e:
          raise BadRequest('Invalid request.')

def check_prephasing_vcf(vcfdf):
  # Check for NULL values in df, that all variants are on the same chromosome, and that more than one variant was passed in
  if vcfdf.isnull().values.any() or len(vcfdf.chr.unique()) > 1 or vcfdf.shape[0] < 2:
    raise BadRequest('Invalid request.')
