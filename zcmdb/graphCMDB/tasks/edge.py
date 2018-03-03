# -*- coding: UTF-8 -*-
"""
    tasks.edge
    ~~~~~~~~~~~
"""
from __future__ import print_function
from arango import ArangoClient
from aliyun.utils import print_star_stop


class Edge(object):
    """build relations between vertices."""

    def __init__(self):
        client = ArangoClient(host="192.168.0.37", password="zbjf123!@#")
        self.db = client.database('CMDB')

    @print_star_stop
    def ipaddr_instance(self):
        cursor = self.db.aql.execute("""
          FOR i IN IpaddrInstance
            RETURN i._key
        """)
        keys = set(list(cursor))
        # Server
        cursor = self.db.aql.execute("""
          FOR i IN Server
            return [FLATTEN([i.PublicIpAddress.IpAddress, LENGTH(i.InnerIpAddress.IpAddress) ? i.InnerIpAddress.IpAddress : i.VpcAttributes.PrivateIpAddress.IpAddress]), i._key]
        """)
        docs = []
        ret = list(cursor)
        for ips, server_key in ret:
            for ip in ips:
                if ip:
                    pk = ip + ':' + server_key
                    if pk not in keys:
                        doc = {'_from': "IpAddress/" + ip,
                               '_to': "Server/" + server_key,
                               '_key': pk
                               }
                        docs.append(doc)
        self.db.collection('IpaddrInstance').insert_many(docs)
        # Load Balance
        cursor = self.db.aql.execute("""
          FOR i IN LoadBalance
            RETURN [i.Address, i._key]
        """)
        docs = []
        ret = list(cursor)
        for ip, lb_key in ret:
            if ip:
                pk = ip + ':' + lb_key
                if pk not in keys:
                    doc = {
                        '_from': "IpAddress/" + ip,
                        '_to': "LoadBalance/" + lb_key,
                        '_key': pk
                    }
                    docs.append(doc)
        self.db.collection('IpaddrInstance').insert_many(docs)

    @print_star_stop
    def instance_account(self):
        cursor = self.db.aql.execute("""
          FOR i IN InstanceAccount
            RETURN i._key
        """)
        keys = set(list(cursor))

        collections = ["Server", "LoadBalance", "NoSQL", "RDBMS"]
        for col in collections:
            cursor = self.db.aql.execute("""
              FOR i IN {0}
                RETURN [i.Access_key, i._key]
            """.format(col))
            docs = []
            ret = list(cursor)
            for account, key in ret:
                pk = ':'.join([account, col, key])
                if pk not in keys:
                    doc = {
                        '_from': "Account/" + account,
                        '_to': col + '/' + key,
                        '_key': pk,
                        'Type': col
                    }
                    docs.append(doc)
            self.db.collection('InstanceAccount').insert_many(docs)

    @print_star_stop
    def loadbalance_backendservers(self):
        cursor = self.db.aql.execute("""
          FOR i IN LoadBalanceBackendServers
            RETURN i._key
        """)
        keys = set(list(cursor))
        docs = []
        cursor = self.db.aql.execute("""
          FOR i IN LoadBalance
            FOR sid IN i.BackendServers.BackendServer[*].ServerId
              RETURN [i._key, sid]
        """)
        for lb, serv in cursor:
            pk = ':'.join([lb, serv])
            if pk not in keys:
                doc = {
                    '_from': "LoadBalance/" + lb,
                    '_to': "Server/" + serv,
                    '_key': pk
                }
                docs.append(doc)
        self.db.collection('LoadBalanceBackendServers').insert_many(docs)

    @print_star_stop
    def instance_application(self):
        cursor = self.db.aql.execute("""
          FOR i IN InstanceApplication
            RETURN i._key
        """)
        keys = set(list(cursor))

        docs = []
        collections = ['Server', ]
        for col in collections:
            cursor = self.db.aql.execute("""
              FOR i IN {0}
                FILTER 'AppName' IN i.Tags.Tag[*].TagKey OR 'appname' IN i.Tags.Tag[*].TagKey
                RETURN KEEP(i, '_key', 'Tags')
            """.format(col))
            for row in cursor:
                for tag in row['Tags']['Tag']:
                    if tag['TagKey'] in ['AppName', 'appname']:
                        tag_values = tag['TagValue'].split(',')
                        for app in tag_values:
                            pk = ':'.join([row['_key'], app])
                            doc = {
                                '_from': "Application/" + app,
                                '_to': col + '/' + row['_key'],
                                '_key': pk
                            }
                            docs.append(doc)
        self.db.collection('InstanceApplication').truncate()
        self.db.collection('InstanceApplication').insert_many(docs)

    @print_star_stop
    def clean_dangling_edges(self):
        filter_collections = []
        for col in self.db.collections():
            name = col['name']
            # filter user defined collections
            if name in filter_collections:
                continue
            # filter system collections
            elif name.startswith('_'):
                continue

            if col['type'] == 'edge':
                print("Edge Collection: ", name)
                for doc in self.db.collection(name):
                    li = map(lambda x: self.db.get_document(x), [doc['_from'], doc['_to']])
                    if None in li:
                        print(doc)
                        self.db.collection(name).delete(doc)

    @print_star_stop
    def main(self):
        self.ipaddr_instance()
        self.instance_account()
        self.loadbalance_backendservers()
        self.instance_application()
        self.clean_dangling_edges()


if __name__ == '__main__':
    e = Edge()
    e.main()

