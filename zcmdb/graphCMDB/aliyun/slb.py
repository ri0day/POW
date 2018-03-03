# -*- coding: UTF-8 -*-
"""
    aliyun.slb
    ~~~~~~~~~~~
"""
import threading

from base import *
from aliyunsdkslb.request.v20140515 import (DescribeLoadBalancersRequest as SLBRequest,
                                            DescribeLoadBalancerAttributeRequest as SLBAttrRequest,
                                            DescribeTagsRequest as SLBTagsRequest)


class SLB(AliyunBase):
    @classmethod
    def get_instances(cls):
        request = SLBRequest.DescribeLoadBalancersRequest
        responses = cls.do_request(request)
        ret = []
        for clt, resp in responses:
            access_key = clt.get_access_key()
            if resp.get('LoadBalancers', {}).get('LoadBalancer', {}):
                instances = []
                for i in resp['LoadBalancers']['LoadBalancer']:
                    i['Access_key'] = access_key
                    instances.append(i)
                ret.extend(instances)
        return ret


class SLB2(AliyunBase):
    @classmethod
    def _get_instance_ids(cls):
        """Extract SLB instance ids, using Threading module.
        
        :return: list of [client, instance_ids]. 
        :rtype:  ist
        """
        request = SLBRequest.DescribeLoadBalancersRequest
        responses = cls.do_request(request)
        ret = []
        for clt, resp in responses:
            if resp.get('LoadBalancers', {}).get('LoadBalancer', {}):
                instance_ids = [i['LoadBalancerId'] for i in
                                resp['LoadBalancers']['LoadBalancer']]
                ret.append([clt, instance_ids])
        return ret

    @classmethod
    def get_instances(cls):
        lock = threading.Lock()
        ret = []
        instance_ids_list = cls._get_instance_ids()
        for clt, instance_ids in instance_ids_list:
            access_key = clt.get_access_key()
            threads = []
            for instance_id in instance_ids:
                with lock:
                    t = threading.Thread(target=cls.do_thread_request,
                                         args=(instance_id, clt, access_key, ret))
                    threads.append(t)
                    t.start()
            for t in threads:
                t.join()
        return ret

    @classmethod
    def do_thread_request(cls, instance_id, clt, access_key, ret):
        request = SLBAttrRequest.DescribeLoadBalancerAttributeRequest()
        request.set_LoadBalancerId(instance_id)
        instance = cls.do_single_request(clt, request)
        instance['Access_key'] = access_key
        ret.append(instance)

    @classmethod
    def get_tags_thread(cls, clt, slbid, ret):
        request = SLBTagsRequest.DescribeTagsRequest()
        request.set_LoadBalancerId(slbid)
        resp = cls.do_single_request(clt,request)
        tags = resp.get('TagSets', {}).get('TagSet', {})
        tag = filter(lambda x: x.get('TagKey') in ['appname','AppName'],tags)
        if tag:
            ret.append({"Tag":tag})

    @classmethod
    def get_tags(cls,slbid):
        ret = []
        threads = []
        for clt in cls.clts:
            t = threading.Thread(target=cls.get_tags_thread,args=(clt,slbid,ret))
            threads.append(t)
        for tx in threads:
            tx.start()
        for t in threads:
            t.join()
        return ret[0] if len(ret) >= 1 else  None


if __name__ == '__main__':
    import time

    st = time.time()
    r = SLB2.get_instances()
    print(len(r))
    print(time.time() - st)
