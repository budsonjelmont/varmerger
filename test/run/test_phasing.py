#import pytest #needed if using markers 
import json
import requests

#@pytest.mark.phasing # see https://circleci.com/blog/testing-flask-framework-with-pytest/
class TestPhasing:
  testdir = '../data/'
  baseurl = 'http://127.0.0.1:6666'
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
    print(res.text)
    print(res.json)
    vcf = self.get_vcf(res.json())[0]
    assert 1==1

  def test_A002(self):
    jsonfile='test_A002.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    print(res.text)
    vcf = self.get_vcf(res.json())[0]
    assert 1==1
  
  def test_A003(self):
    jsonfile='test_A003.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    assert vcf['ref'] == 'G'
    assert vcf['alt'] == 'CCA'
  
  def test_A004(self):
    jsonfile='test_A004.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())[0]
    assert vcf['alt'] == 'GCACGGAG'
  
  def test_A005(self):
    jsonfile='test_A005.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())
    print(vcf)
    assert not vcf
  
  def test_A006(self):
    jsonfile='test_A006.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())
    print(vcf)
    assert not vcf
  
  def test_A007(self):
    jsonfile='test_A007.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())
    print(vcf)
    assert not vcf
  
  def test_A008(self):
    jsonfile='test_A008.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())
    print(vcf)
    assert not vcf
  
  def test_A009(self):
    jsonfile='test_A009.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())
    print(vcf)
    assert not vcf
  
  def test_A010(self):
    jsonfile='test_A010.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())
    print(vcf)
    assert not vcf
  
  def test_A011(self):
    jsonfile='test_A011.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())
    print(vcf)
    assert 1==1 
  
  def test_A012(self):
    jsonfile='test_A012.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    out_json = res.json()
    vcf = out_json['result'][0]
    print(vcf)
    assert vcf['chr']=='22'
  
  def test_A013(self):
    jsonfile='test_A013.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    out_json = res.json()
    vcf = out_json['result'][0]
    print(vcf)
    assert vcf['chr']=='22'
  
  def test_A014(self):
    jsonfile='test_A014.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    out_json = res.json()
    vcf = out_json['result'][0]
    print(vcf)
    assert vcf['chr']=='19'
    assert vcf['alt']=='TAAAAAAATTGC'
  
  def test_A015(self):
    jsonfile='test_A015.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    out_json = res.json()
    vcf = out_json['result'][0]
    print(vcf)
    assert vcf['chr']=='22'
  
  def test_A016(self):
    jsonfile='test_A016.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())
    print(vcf)
    assert not vcf
  
  def test_A017(self):
    jsonfile='test_A017.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())
    print(vcf)
    assert not vcf
  
  def test_A018(self):
    jsonfile='test_A018.json'
    in_json = self.get_test_payload(jsonfile)
    res = requests.post(self.url, json=in_json, headers=self.headers)
    vcf = self.get_vcf(res.json())
    print(vcf)
    assert not vcf

if __name__ == '__main__':
    print('yeaaa')
    test = TestPhasing()
    test.test_A008()
