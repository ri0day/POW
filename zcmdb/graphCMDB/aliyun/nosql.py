# -*- coding: UTF-8 -*-
"""
    aliyun.nosql
    ~~~~~~~~~~~
"""
from base import *
from aliyunsdkr_kvstore.request.v20150101 import DescribeInstancesRequest as KVStoreRequest


class KVStore(AliyunBase):
    @classmethod
    def get_instances(cls):
        request = KVStoreRequest.DescribeInstancesRequest
        responses = cls.do_request(request,page_size=50)
        ret = []
        for clt, resp in responses:
            access_key = clt.get_access_key()
            if resp.get('Instances', {}).get('KVStoreInstance', {}):
                instances = []
                for i in resp['Instances']['KVStoreInstance']:
                    i['Access_key'] = access_key
                    instances.append(i)
                ret.extend(instances)
        return ret


if __name__ == '__main__':
    r = KVStore.get_instances()
    import json

    print(json.dumps(r, indent=4))