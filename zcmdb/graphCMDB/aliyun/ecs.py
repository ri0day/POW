# -*- coding: UTF-8 -*-
"""
    aliyun.ecs
    ~~~~~~~~~~~
"""
from utils import scan_page
from base import *
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest as ECSRequest
from aliyunsdkecs.request.v20140526 import DescribeDisksRequest as DisksRequest


class ECS(AliyunBase):
    @classmethod
    @scan_page
    def get_instances(cls, page_num=1, page_size=50):
        request = ECSRequest.DescribeInstancesRequest
        responses = cls.do_request(request, page_num, page_size)
        ret = []
        for clt, resp in responses:
            access_key = clt.get_access_key()
            if resp.get('Instances', {}).get('Instance', {}):
                instances = []
                for i in resp['Instances']['Instance']:
                    i['Access_key'] = access_key
                    instances.append(i)
                ret.extend(instances)
        return ret


    @classmethod
    @scan_page
    def get_disks(cls, page_num=1, page_size=50):
        request = DisksRequest.DescribeDisksRequest
        responses = cls.do_request(request, page_num, page_size)
        ret = []
        for clt, resp in responses:
            access_key = clt.get_access_key()
            if resp.get('Disks', {}).get('Disk', {}):
                disks = []
                for i in resp['Disks']['Disk']:
                    i['Access_key'] = access_key
                    disks.append(i)
                ret.extend(disks)
        return ret


if __name__ == '__main__':
    r = ECS.get_disks()
    print(len(r))
    # import json
    # print(json.dumps(r, indent=4))
