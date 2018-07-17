from libs import AliBase
import json
from aliyunsdkecs.request.v20140526.DescribeAvailableResourceRequest import DescribeAvailableResourceRequest
import argparse

account='myram'


def build_req(zone,cores,mem,res_type='InstanceType'):
    req  = DescribeAvailableResourceRequest()
    req.set_DestinationResource(res_type)
    req.set_IoOptimized('optimized')
    req.set_ZoneId(zone)
    req.set_Cores(cores)
    req.set_Memory(mem)
    return req


def query_instance_type():
    c = AliBase(region='cn-hangzhou')
    if all([args.zone, args.cpus, args.mem]):
        req = build_req(zone=args.zone,cores=args.cpus,mem=args.mem)
        resp = c.send_request(account,req)
        AvailableResource = resp.get('AvailableZones').get('AvailableZone')[0].get('AvailableResources').get('AvailableResource')[0]
        SupportedResource = AvailableResource.get('SupportedResources').get('SupportedResource')
        return [d['Value'] for d in SupportedResource]
    else:
        print "Usage: python avaliable_instancetypes.py --zone cn-hangzhou-f --cpus 4 --mem 8"

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--zone", help="zoneid for query", type=str)
    parser.add_argument("--cpus", help="number of cores", type=int)
    parser.add_argument("--mem", help="physical memory (g)", type=int)
    args = parser.parse_args()
    for r in query_instance_type():
        print r
