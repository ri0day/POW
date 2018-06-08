# coding: utf-8
import ConfigParser
import json
import logging
import os
from time import sleep

import requests
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526.CreateInstanceRequest import CreateInstanceRequest
from aliyunsdkecs.request.v20140526.RunInstancesRequest import RunInstancesRequest
from aliyunsdkecs.request.v20140526.StartInstanceRequest import StartInstanceRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest

logging.basicConfig(level=logging.INFO, filename="app.log",
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

config_filename = 'account.ini'

class AliBase(object):
    def __init__(self,config=config_filename):
        cfg = ConfigParser.ConfigParser()
        cfg.optionxform = str
        cfg_dir = os.path.dirname(__file__)
        cfg.read(os.path.join(cfg_dir, config))
        sections = cfg.sections()
        self.accounts = {}
        for section in sections:
            options = dict(cfg.items(section))
            self.accounts[section] = client.AcsClient(options.get('ACCESSKEY'), options.get('ACCESS_SECRET'),
                                                      options.get('REGION'))

    def client(self, account):
        return self.accounts.get(account)


class SpawnEcs(object):
    def build_request_run_ecs(self, params):
        request = RunInstancesRequest()
        request.set_accept_format('json')
        for k in params:
            if k == 'account':
                pass
            else:
                request.add_query_param(k, params[k])
        return request

    def build_request_create_ecs(self, params):
        request = CreateInstanceRequest()
        request.set_accept_format('json')
        for k in params:
            if k == 'account':
                pass
            else:
                request.add_query_param(k, params[k])
        return request

    def startup_ecs(self,instanceid):
        request = StartInstanceRequest()
        request.set_accept_format('json')
        request.set_InstanceId(instanceid)
        return  request

    def instance_status(self,instanceid):
        request = DescribeInstancesRequest()
        request.set_InstanceIds([instanceid])
        request.set_accept_format('json')
        return request

    def send_request(self, account, request):
        try:
            ctl = AliBase().client(account)
            response_str = ctl.do_action(request)
            logging.info(response_str)
            response_detail = json.loads(response_str)
            return response_detail
        except Exception as e:
            logging.info(e)

    def bringup_instance(self,instanceid,account):
        if instanceid:
            g = SpawnEcs()
            req = g.instance_status(instanceid)
            response_str = g.send_request(account,req)
            status = response_str.get('Instances').get('Instance')[0].get('Status')
            while status == 'Pending':
                print 'instance in pending status ,retry in 2s'
                sleep(2)
                return self.bringup_instance(instanceid,account)
        req = g.startup_ecs(instanceid) 
        response_str = g.send_request(account,req)
        return response_str

def get_content(dst):
    if dst.startswith('http'):
        try:
            return json.loads(requests.get(dst).text)
        except Exception as e:
            print e
    elif dst.startswith('/') or dst.startswith('.'):
        with open(dst, 'r') as f:
            return json.loads(f.read())
    else:
        print 'only  url and local file supported'
