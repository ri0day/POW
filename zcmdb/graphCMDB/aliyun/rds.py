# -*- coding: UTF-8 -*-
"""
    aliyun.rds
    ~~~~~~~~~~~
"""
from base import *
from aliyunsdkrds.request.v20140815 import (DescribeDBInstancesRequest as RDSRequest,
                                            DescribeDBInstanceAttributeRequest as RDSAttrRequest,
                                            DescribeTagsRequest as RDSTagsRequest)


class RDS(AliyunBase):
    @classmethod
    def _get_instance_ids(cls):
        """Extract DB instance ids.

        :return: list of [client, instance_ids].
        :rtype: list
        """
        request = RDSRequest.DescribeDBInstancesRequest
        responses = cls.do_request(request)
        ret = []
        for clt, resp in responses:
            if resp.get('Items', {}).get('DBInstance', {}):
                instance_ids = [i['DBInstanceId'] for i in resp['Items']['DBInstance']]
                ret.append([clt, instance_ids])
        return ret

    @classmethod
    def get_instances(cls):
        ret = []
        instance_ids_list = cls._get_instance_ids()
        for clt, instance_ids in instance_ids_list:
            access_key = clt.get_access_key()
            # aliyun API only can accept at most 30 instance ids, so split into chunks
            chunk_instance_ids = [instance_ids[i:i + 30] for i in
                                  range(0, len(instance_ids), 30)]
            for chunk in chunk_instance_ids:
                request = RDSAttrRequest.DescribeDBInstanceAttributeRequest()
                request.set_DBInstanceId(','.join(chunk))
                response = cls.do_single_request(clt, request)
                instances = []
                for i in response['Items']['DBInstanceAttribute']:
                    i['Access_key'] = access_key
                    instances.append(i)
                ret.extend(instances)
        return ret


    @classmethod
    def get_tags(cls,rdsid):
        request = RDSTagsRequest.DescribeTagsRequest()
        request.set_DBInstanceId(rdsid)
        for clt in cls.clts:
            resp = cls.do_single_request(clt,request)
            tags = resp.get('Items',{}).get('TagInfos',{})
            tag = filter(lambda x: x.get('TagKey') in ['appname','AppName'],tags)
            if tag:
                return {"Tag":tag}


if __name__ == '__main__':
    r = RDS.get_instances()
    import json

    print(json.dumps(r, indent=4))
