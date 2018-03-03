# -*- coding: UTF-8 -*-
"""
    ArangoDB external inventory script
    ~~~~~~~~~~~
"""
from __future__ import print_function
import json
from arango import ArangoClient


class Inventory(object):

    def __init__(self):
        client = ArangoClient(host="192.168.0.37", password="zbjf123!@#")
        self.db = client.database('CMDB')

    def main(self):
        cursor = self.db.aql.execute("""
        FOR i IN InstanceApplication
          COLLECT app = DOCUMENT(i._from).Name INTO ipaddr = DOCUMENT(i._to).InnerIpAddress.IpAddress
          RETURN {
            "AppName": app,
            "IpAddress": ipaddr[**]
          }
        """)
        ret = {}
        for row in cursor:
           k = row['AppName']
           v = row['IpAddress']
           ret[k] = v
        print(json.dumps(ret))


if __name__ == '__main__':
    i = Inventory()
    i.main()
