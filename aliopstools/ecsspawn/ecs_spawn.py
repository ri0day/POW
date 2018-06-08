# coding: utf-8

from sys import argv

from libs import SpawnEcs
from libs import get_content


def ecs_gen(filepath):
    j = get_content(filepath)
    for hostid, params in j.items():
        q = SpawnEcs(region=params.get('RegionId'))
        account = params.get('account')
        if 'Amount' in params:
            req = q.build_request_run_ecs(params)
            response = q.send_request(account, req)
            instanceid = response.get('InstanceIdSets').get('InstanceIdSet')
        else:
            req = q.build_request_create_ecs(params)
            response = q.send_request(account, req)
            instanceid = response.get('InstanceId')
            if instanceid:
                   q.bringup_instance(instanceid,account,region=q.region)
  
        if instanceid:
            print "Create ECS Server {hostid}  Success Instanceid: {instanceid}".format(hostid=hostid,
                                                                                        instanceid=instanceid)
        else:
            print "Create ECS Server {hostid}  Failed".format(hostid=hostid)



if __name__ == '__main__':
    jsonfile = argv[1]
    ecs_gen(jsonfile)
