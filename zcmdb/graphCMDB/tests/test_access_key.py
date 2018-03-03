import os
import ConfigParser

from aliyun.base import AliyunBase
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest as ECSRequest


def main():
    res = AliyunBase.do_request(ECSRequest.DescribeInstancesRequest)
    return res

def test():
    cfg = ConfigParser.ConfigParser()
    cfg.optionxform = str
    cfg_dir = os.path.dirname(__file__)
    cfg.read(os.path.join(cfg_dir, 'config.ini'))
    clts = []
    sections = cfg.sections()
    for section in sections:
        options = dict(cfg.items(section))
        clts.append(client.AcsClient(
            options['ACCESSKEY'],
            options['ACCESS_SECRET'],
            options['REGION'],
        ))
    ret = []
    for c in clts:
        print(c.do_action(ECSRequest.DescribeInstancesRequest()))


if __name__ == '__main__':
    # main()
    test()
