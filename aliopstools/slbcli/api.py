#!/usr/bin/env python
#coding: utf-8
import json
import collections
from aliyunsdkcore import client
from aliyunsdkslb.request.v20140515 import (DescribeVServerGroupsRequest,
                                            DescribeLoadBalancersRequest,
                                            DescribeVServerGroupAttributeRequest,
                                            DescribeLoadBalancerAttributeRequest,
                                            RemoveBackendServersRequest,
                                            AddVServerGroupBackendServersRequest,
                                            RemoveVServerGroupBackendServersRequest,
                                            AddBackendServersRequest,
                                            SetBackendServersRequest)
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from arango import ArangoClient

class DataSource(object):
    def __init__(self):
        client = ArangoClient(host="192.168.0.37", password="zbjf123!@#")
        self.db = client.database('CMDB')

    def App_to_balancerid(self,appname):
        q ="""
        FOR i IN LoadBalance
          FILTER @value IN i.Tags.Tag[*].TagValue
        RETURN i.LoadBalancerId
        """
        cursor = self.db.aql.execute(q,bind_vars={'value': appname})
        r = list(cursor)
        return r if r else None 

class AliyunSlb(object):
    def __init__(self, accesskey, access_secret, region):
        self.accesskey = accesskey
        self.access_secret = access_secret
        self.region = region
        self.clt = client.AcsClient(self.accesskey, self.access_secret, self.region)


    def slb_status(self, slbid):
        slb = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        slb.set_accept_format('json')
        if slbid:
            slb.set_LoadBalancerId(slbid)
        slb_r = self.clt.do_action(slb)
        slb_json = json.loads(slb_r)
        d = collections.OrderedDict()
        for obj in slb_json.get('LoadBalancers').get('LoadBalancer'):
            slb_name = obj.get('LoadBalancerName')
            slb_id = obj.get('LoadBalancerId').encode('utf-8')
            slb_type = obj.get('AddressType').encode('utf-8')
            slb_regionid = obj.get('RegionId').encode('utf-8')
            slb_status = obj.get('LoadBalancerStatus').encode('utf-8')
            slb_ip = obj.get('Address').encode('utf-8')
            slb_backends = self.list_slb_backends(slb_id)
            slb_vgroups = self.list_vgroups(slb_id)
            vss = []
            if slb_vgroups:
                for vg in slb_vgroups:
                    vgid = vg.get('VServerGroupId')
                    vgservers = self.list_vgroup_servers(vgid)
                    vgsrvinfo = {vgid: vgservers}
                    vss.append(vgsrvinfo)

            d[slb_id] = {'name': slb_name,'type': slb_type,'slb_ip': slb_ip,
                        'slb_status': slb_status, 'slb_regionid': slb_regionid,
                        'backends':slb_backends ,'vgroups':slb_vgroups,'vgroup_servers':vss}
        for k, v in d.items():
            print '%s | %s'%(k, v)

    def list_vgroups(self, slb_id):
        slb = DescribeVServerGroupsRequest.DescribeVServerGroupsRequest()
        slb.set_LoadBalancerId(slb_id)
        slb.set_accept_format('json')
        slb_r = self.clt.do_action(slb)
        slb_json = json.loads(slb_r)
        vgroups = slb_json.get('VServerGroups').get('VServerGroup')
        return vgroups

    def list_vgroup_servers(self, vgroupid):
        slb = DescribeVServerGroupAttributeRequest.DescribeVServerGroupAttributeRequest()
        slb.set_VServerGroupId(vgroupid)
        slb.set_accept_format('json')
        slb_r = self.clt.do_action(slb)
        slb_json = json.loads(slb_r)
        return slb_json.get('BackendServers').get('BackendServer')

    def list_slb_backends(self, slb_id):
        slb = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
        slb.set_LoadBalancerId(slb_id)
        slb.set_accept_format('json')
        slb_r = self.clt.do_action(slb)
        slb_json = json.loads(slb_r)
        return [obj for obj in slb_json.get('BackendServers').get('BackendServer')]
        


    def remove_slb_backends(self, loadbalancer_id, backend_ids):
        slb = RemoveBackendServersRequest.RemoveBackendServersRequest()
        slb.set_accept_format('json')
        slb.set_LoadBalancerId(loadbalancer_id)
        if type(backend_ids) == "list":
            slb.set_BackendServers(backend_ids)
        else:
            slb.set_BackendServers([backend_ids])
        slb_r = self.clt.do_action(slb)
        slb_json = json.loads(slb_r)
        return slb_json

    def add_slb_backends(self, loadbalancer_id, backend_id):
        if isinstance(backend_id, str):
            backend_playload = [{'ServerId': backend_id, "Weight": "100"}]
        else:
            backend_playload = backend_id
        slb = AddBackendServersRequest.AddBackendServersRequest()
        slb.set_accept_format('json')
        slb.set_LoadBalancerId(loadbalancer_id)
        slb.set_BackendServers(backend_playload)
        slb_r = self.clt.do_action(slb)
        slb_json = json.loads(slb_r)
        return slb_json

    def add_vg_servers(self, vgid, backend_id, port):
        if ',' in backend_id:
            backend_playload = [{'ServerId': x, "Weight": "100", "Port": port} for x in backend_id.split(',')]
        else:
            backend_playload = [{'ServerId': backend_id, "Weight": "100", "Port": port}]
        slb = AddVServerGroupBackendServersRequest.AddVServerGroupBackendServersRequest()
        slb.set_accept_format('json')
        slb.set_VServerGroupId(vgid)
        slb.set_BackendServers(backend_playload)
        slb_r = self.clt.do_action(slb)
        slb_json = json.loads(slb_r)
        return slb_json

    def remove_vg_servers(self, vgid, backend_id, port):
        if ',' in backend_id:
            backend_playload = [{'ServerId': x, "Weight": "100", "Port": port} for x in backend_id.split(',')]
        else:
            backend_playload = [{'ServerId': backend_id, "Weight": "100", "Port": port}]
        slb = RemoveVServerGroupBackendServersRequest.RemoveVServerGroupBackendServersRequest()
        slb.set_accept_format('json')
        slb.set_VServerGroupId(vgid)
        slb.set_BackendServers(backend_playload)
        slb_r = self.clt.do_action(slb)
        slb_json = json.loads(slb_r)
        return slb_json

    def disable_backends_by_weight(self,slbid,backendid):
        slb = SetBackendServersRequest.SetBackendServersRequest()
        slb.set_LoadBalancerId(slbid)
        slb.set_accept_format('json')
        backends = self.list_slb_backends(slbid)
        newbackends = []
        if backends:
            for backend in backends:
                if backend['ServerId'] == backendid:
                    backend['Weight'] = "0"
                newbackends.append(backend)
        slb.set_BackendServers(json.dumps(newbackends))
        slb_r = self.clt.do_action(slb)
        return slb_r

    def enable_backends_by_weight(self,slbid,backendid):
        slb = SetBackendServersRequest.SetBackendServersRequest()
        slb.set_LoadBalancerId(slbid)
        slb.set_accept_format('json')
        backends = self.list_slb_backends(slbid)
        newbackends = []
        if backends:
            for backend in backends:
                if backend['ServerId'] == backendid:
                    backend['Weight'] = "100"
                newbackends.append(backend)
        slb.set_BackendServers(json.dumps(newbackends))
        slb_r = self.clt.do_action(slb)
        return slb_r
