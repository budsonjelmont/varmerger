import argparse as ap
import vcf
import json

parser = ap.ArgumentParser(description='Read a VCF file and output a flat .json file.')
parser.add_argument('vcfinfile', type=str, nargs=1, help='VCF input file')
parser.add_argument('jsonoutfile', type=str, nargs=1, help='JSON output file')
parser.add_argument('--g','--build', type=str, dest='genomicbuild', default='GRCh37', help='Genomic build to include in JSON payload. Default: GRCh37')
parser.add_argument('--i','--indents', type=int, dest='indents', default=4, help='Indents to add to make JSON output look nice. Default: 4')
parser.add_argument('--m','--mergedist', type=int, dest='mergedist', help='Optional. Merge distance to include in payload for phase merges.')

#args = parser.parse_args('/mnt/c/Users/judson.x.belmont/Documents/Code/varchemist/test/data/test_8.sort.vcf /mnt/c/Users/judson.x.belmont/Documents/Code/varchemist/test/data/test_A008.json'.split(' '))
args = parser.parse_args()

vcfinfile = args.vcfinfile[0]
jsonoutfile = args.jsonoutfile[0]
genomicbuild = args.genomicbuild # Deprecated. No longer sent in JSON payload.
indents = args.indents
mergedist = args.mergedist

with open(vcfinfile, 'r') as vcffile:
  reader = vcf.Reader(vcffile)
  variants = list(reader)
  vcflist = [] 
  empty_record = vcf.model._Record(None, 0, None, '', '', '', '', '', '', '')
  last_record = empty_record
  for record in variants:
    if last_record is not None and last_record.CHROM != record.CHROM:
      last_record = empty_record
    elif last_record.start > record.start:
      raise ValueError('VCF must be sorted.')
    for alt in record.ALT:
      # TODO add support for other VCF fields
      vcflist.append({"chr": record.CHROM, "pos": record.POS, "id": record.ID, "ref": record.REF, "alt": str(alt)})

jsondict = {'vcf': vcflist}

if mergedist is not None:
    jsondict['mergedist'] = mergedist

with open(jsonoutfile, 'w') as jsonfile:
  json.dump(jsondict, jsonfile, indent=indents)
