#import pytest #needed if using markers 
import json
import requests

#@pytest.mark.phasing # see https://circleci.com/blog/testing-flask-framework-with-pytest/
class TestPhasing:
  testdir = '../data/'
  baseurl = 'http://127.0.0.1:6666'
  #baseurl = 'http://127.0.0.1:5000'
  #baseurl = 'http://127.0.0.1:80'
  endpoint = '/merge_variants'
  url = baseurl + endpoint
  headers = {'Content-type': 'application/json'} # don't strictly need to set explicitly, requests lib will do it for us

  def get_test_payload(self, jsonfile):
    jsonf = open(self.testdir + '/' + jsonfile,'r')
    testjson = json.load(jsonf) 
    jsonf.close()
    return testjson

  def get_vcf(self, resjson):
    return resjson['result']

  def test_A001(self):
    jsonfile='test_A001.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    assert vcf['ref'] == 'AG'
    assert vcf['alt'] == 'GC'

  def test_A002(self):
    jsonfile='test_A002.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    print(res.text)
    vcf = self.get_vcf(res.json())[0]
    #assert vcf['ref'] == 'CTGC'
    #assert vcf['alt'] == 'CGC'
    assert vcf['ref'] == 'CTGC' # This is the result obtained after L-trimming VCF
    assert vcf['alt'] == 'CCT' # This is the result obtained after L-trimming VCF

  def test_A003(self):
    jsonfile='test_A003.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    assert vcf['ref'] == 'CTG'
    assert vcf['alt'] == 'CGCA'
  
  def test_A004(self):
    jsonfile='test_A004.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    assert vcf['ref'] == 'GCAC'
    assert vcf['alt'] == 'GCACACGGAG'
  
  def test_A005(self):
    jsonfile='test_A005.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())
    assert not vcf
  
  def test_A006(self):
    jsonfile='test_A006.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    print(vcf)
    assert vcf['ref'] == 'TAAGGCTTAATATTGGTAGAGAGAGAAAG'
    assert vcf['alt'] == 'T'
  
  def test_A007(self):
    jsonfile='test_A007.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    print(vcf)
    assert vcf['ref'] == 'TAAGGCTTAATATTGGTA'
    assert vcf['alt'] == 'T'
  
  def test_A008(self):
    jsonfile='test_A008.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    print(vcf)
    assert vcf['ref'] == 'TAAGGCTTAATATT'
    assert vcf['alt'] == 'T'
  
  def test_A009(self):
    jsonfile='test_A009.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    print(vcf)
    #assert vcf['ref'] == 'TAAGGCTTAATATTGGTA' 
    #assert vcf['alt'] == 'CCGTA'
    assert vcf['ref'] == 'TAAGGCTTAATATTG' # After R-trimming 
    assert vcf['alt'] == 'CC' # After R-trimming
  
  def test_A010(self):
    jsonfile='test_A010.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    print(vcf)
    assert vcf['ref'] == 'ATAAACCCTATGCTCTCAGTTCAACACTCTTCAGATGATGTAGCCATTTAACTGTCCTACACAAAATGCTTGTAAAAATCTACTAGATTCAAAAACATTTCACTGG'
    assert vcf['alt'] == 'ACCCTATGCTCTCAGTTCAACACTCTTCAGATGATGTAGCCATTTAACTGTCCTACACAAAATGCTTGTAAAAATCTACTAGATTCAAAAACATTTCACTGGTTTT'
  
  def test_A011(self):
    jsonfile='test_A011.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    out_json = res.json()
    vcf = out_json['result'][0]
    print(vcf)
    assert vcf['ref'] == 'GT'
    assert vcf['alt'] == 'GG'
  
  def test_A012(self):
    jsonfile='test_A012.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    out_json = res.json()
    vcf = out_json['result'][0]
    print(vcf)
    #assert vcf['ref'] == 'AGAGAAATACCCTGGACC'
    #assert vcf['alt'] == 'AATATTAATTTTTCCCATTC'
    # After L&R trimming
    assert vcf['ref'] == 'AGAGAAATACCCTGGAC'
    assert vcf['alt'] == 'AATATTAATTTTTCCCATT'
  
  def test_A013(self):
    jsonfile='test_A013.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    out_json = res.json()
    vcf = out_json['result'][0]
    print(vcf)
    assert vcf['ref']=='TGAA'
    assert vcf['alt']=='GGGG'
  
  def test_A014(self):
    jsonfile='test_A014.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    out_json = res.json()
    vcf = out_json['result'][0]
    print(vcf)
    assert vcf['chr']=='19'
    assert vcf['ref']=='TTTGG'
    assert vcf['alt']=='TAAAAAAATTGC'
  
  def test_A015(self):
    jsonfile='test_A015.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    out_json = res.json()
    vcf = out_json['result'][0]
    print(vcf)
    assert vcf['chr']=='19'
    assert vcf['ref']=='TTTGG'
    assert vcf['alt']=='TAAAAAAAATTGA'
  
  def test_A016(self):
    jsonfile='test_A016.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    out_json = res.json()
    vcf = out_json['result'][0]
    print(vcf)
    assert vcf['chr'] == '16'
    #assert vcf['ref'] == 'TTCCT'
    #assert vcf['alt'] == 'CTTCT'
    assert vcf['ref'] == 'TTC' # This is the result obtained after L/R-trimming VCF
    assert vcf['alt'] == 'CTT' # This is the result obtained after L/R-trimming VCF
  
  def test_A017(self):
    jsonfile='test_A017.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())
    out_json = res.json()
    vcf = out_json['result'][0]
    print(vcf)
    assert vcf['ref'] == 'CA'
    assert vcf['alt'] == 'TG'
  
  def test_A018(self):
    jsonfile='test_A018.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())
    print(vcf)
    assert not vcf

  def test_A019(self):
    jsonfile='test_A019.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    print(vcf)
    assert vcf['ref'] == 'GTGTTCCCA'
    assert vcf['alt'] == 'GGTTGCAC'
  
  def test_A020(self):
    jsonfile='test_A020.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    print(vcf)
    assert vcf['ref'] == 'GTGTTCCCA'
    assert vcf['alt'] == 'GGGTGCAC'
  
  def test_A021(self):
    jsonfile='test_A021.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    print(vcf)
    #assert vcf['ref'] == 'GTGTTCCCA'
    #assert vcf['alt'] == 'GGGTAAACCAC'
    # After L&R trimming
    assert vcf['ref'] == 'GTGTTCCCA'
    assert vcf['alt'] == 'GGGTAAAGCAC'
  
  def test_A022(self):
    jsonfile='test_A022.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    print(vcf)
    assert vcf['ref'] == 'GTGTTCCCA'
    assert vcf['alt'] == 'GGGTAAAGCAC'# Variant skipped in A021 is accounted for
  
  def test_A023(self):
    jsonfile='test_A023.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    print(vcf)
    assert vcf['ref'] == 'GTGTTCCCA'
    assert vcf['alt'] == 'GGGTAAAGCAC'
  
  def test_A024(self):
    jsonfile='test_A024.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    print(vcf)
    assert vcf['ref'] == 'TTGCAAGGAAATGTAGCTCCCTC'
    assert vcf['alt'] == 'GTGCAAGGCGTAGCTCCCTG'
  
  def test_A025(self):
    jsonfile='test_A025.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    print(vcf)
    assert vcf['ref'] == 'GTGTTCCCA'
    assert vcf['alt'] == 'GGTTGCAC'

  def test_A026(self):
    jsonfile='test_A026.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    print(vcf)
    #assert vcf['ref'] == 'GTGTTCCCA'
    #assert vcf['alt'] == 'GGGGTGCAC'
    # After L&R trimming
    assert vcf['ref'] == 'TGTTCCCA'
    assert vcf['alt'] == 'GGGTGCAC'
  
  def test_A027(self):
    jsonfile='test_A027.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    print(vcf)
    #assert vcf['ref'] == 'AATCA'
    #assert vcf['alt'] == 'ACGT'
    assert vcf['ref'] == 'ATCA'
    assert vcf['alt'] == 'CGT'


  def test_A028(self):
    jsonfile='test_A028.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    print(vcf)
    #assert vcf['ref'] == 'AATCAT'
    #assert vcf['alt'] == 'ACGT'
    assert vcf['ref'] == 'ATCA'
    assert vcf['alt'] == 'CGT'
  
  def test_A029(self):
    jsonfile='test_A029.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    print(vcf)
    #assert vcf['ref'] == 'GTGTTCCCA'
    #assert vcf['alt'] == 'GTGTTCCCA'
    assert vcf['ref'] == 'TGTTCCC'
    assert vcf['alt'] == 'CTGT'

  def test_A030(self):
    jsonfile='test_A030.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    vcf1 = self.get_vcf(res.json())[1]
    print(vcf)
    assert vcf['ref'] == 'CTG'
    assert vcf['alt'] == 'CGCA'
    assert vcf1['ref'] == 'AG'
    assert vcf1['alt'] == 'GC'
  
  def test_B001(self):
    in_dict = {'vcf':[]}
    in_json = json.dumps(in_dict)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    print(res.text)
    print(res.headers)
    assert res.status_code == 400

if __name__ == '__main__':
    test = TestPhasing()
    test.test_A015()
