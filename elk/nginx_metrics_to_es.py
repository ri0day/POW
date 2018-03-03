#!/usr/bin/env python
#coding: utf-8
from elasticsearch import Elasticsearch
import time,requests,re,random

NGINX_URL = 'http://127.0.0.1/status'
ES_URL = 'http://10.117.82.4:9200'
INDEX_NAME = 'nginx_status01'
TYPE='qps'

class QPS(object):
    def __init__(self,nginx_url,es_url,index_name,doc_name):
        self.nginx_url = nginx_url
        self.es_url = es_url
        self.index_name = index_name
        self.doc_name = doc_name

    def _fetch(self):
       rsp = requests.get(self.nginx_url)
       accepts, handled, total_requests = re.search(r'\s*(\d+)\s+(\d+)\s+(\d+)',rsp.text).groups()
       return int(total_requests)


    def push_es(self,data):
        es = Elasticsearch(self.es_url)
        body = {'qps':data,'date':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'+0800'}
        print body
        return es.index(index=self.index_name,doc_type=self.doc_name,body=body)

    def run(self):
        before = self._fetch()
        time.sleep(1)
        after = self._fetch()
        data = after - before
        return self.push_es(data)

qps = QPS(NGINX_URL,ES_URL,INDEX_NAME,TYPE)
print qps.run()
