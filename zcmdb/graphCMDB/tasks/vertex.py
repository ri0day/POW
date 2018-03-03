# -*- coding: UTF-8 -*-
"""
    tasks.vertex
    ~~~~~~~~~~~
"""
from __future__ import print_function
import os
import ConfigParser
from arango import ArangoClient
from aliyun import ECS, SLB2 as SLB, KVStore, RDS
from aliyun.utils import print_star_stop


class Vertex(object):
    """sync data from aliyun."""

    def __init__(self):
        client = ArangoClient(host="192.168.0.37", password="zbjf123!@#")
        self.db = client.database('CMDB')

    @print_star_stop
    def sync_server(self):
        """aliyun ECS"""
        server_mapping = {i['InstanceId']: i for i in ECS.get_instances()}
        servers_aliyun = set(server_mapping.keys())
        cursor = self.db.aql.execute("FOR i IN Server RETURN i._key")
        servers_cmdb = set(list(cursor))
        added = servers_aliyun - servers_cmdb
        removed = servers_cmdb - servers_aliyun
        # insert new servers
        insert_list = []
        for iid in added:
            doc = server_mapping[iid]
            doc['_key'] = iid
            doc['State'] = True
            insert_list.append(doc)
        self.db.collection('Server').insert_many(insert_list)
        # delete removed servers
        remove_list = []
        for iid in removed:
            print('remove servers %s'%iid)
            doc = {}
            doc['_key'] = iid
            remove_list.append(doc)
        self.db.collection('Server').delete_many(remove_list)
        # update exist servers
        update_list = []
        for iid in (servers_aliyun - added):
            doc = server_mapping[iid]
            doc['_key'] = iid
            doc['State'] = True
            update_list.append(doc)
        self.db.collection('Server').replace_many(update_list)

    @print_star_stop
    def sync_lb(self):
        """aliyun SLB"""
        lb_mapping = {i['LoadBalancerId']: i for i in SLB.get_instances()}
        lb_aliyun = set(lb_mapping.keys())
        cursor = self.db.aql.execute("FOR i In LoadBalance RETURN i._key")
        lb_cmdb = set(list(cursor))
        added = lb_aliyun - lb_cmdb
        removed = lb_cmdb - lb_aliyun
        # insert new lbs
        insert_list = []
        for iid in added:
            doc = lb_mapping[iid]
            doc['_key'] = iid
            doc['State'] = True
            doc['Tags'] = SLB.get_tags(iid)
            insert_list.append(doc)
        self.db.collection('LoadBalance').insert_many(insert_list)
        # delete removed lbs
        remove_list = []
        for iid in removed:
            doc = {}
            doc['_key'] = iid
            remove_list.append(doc)
        self.db.collection('LoadBalance').delete_many(remove_list)
        # update exist lbs
        update_list = []
        for iid in (lb_aliyun - added):
            doc = lb_mapping[iid]
            doc['_key'] = iid
            doc['State'] = True
            doc['Tags'] = SLB.get_tags(iid)
            update_list.append(doc)
        self.db.collection('LoadBalance').replace_many(update_list)

    @print_star_stop
    def sync_nosql(self):
        """aliyun Redis"""
        kv_mapping = {i['InstanceId']: i for i in KVStore.get_instances()}
        kv_aliyun = set(kv_mapping.keys())
        cursor = self.db.aql.execute("FOR i IN NoSQL RETURN i._key")
        kv_cmdb = set(list(cursor))
        added = kv_aliyun - kv_cmdb
        removed = kv_cmdb - kv_aliyun
        # insert new kvs
        insert_list = []
        for iid in added:
            doc = kv_mapping[iid]
            doc['_key'] = iid
            doc['State'] = True
            insert_list.append(doc)
        self.db.collection('NoSQL').insert_many(insert_list)
        # delete removed kvs
        remove_list = []
        for iid in removed:
            doc = {}
            doc['_key'] = iid
            remove_list.append(doc)
        self.db.collection('NoSQL').delete_many(remove_list)
        # update exist kvs
        update_list = []
        for iid in (kv_aliyun - added):
            doc = kv_mapping[iid]
            doc['_key'] = iid
            doc['State'] = True
            update_list.append(doc)
        self.db.collection('NoSQL').replace_many(update_list)

    @print_star_stop
    def sync_rdbms(self):
        """aliyun RDS"""
        db_mapping = {i['DBInstanceId']: i for i in RDS.get_instances()}
        db_aliyun = set(db_mapping.keys())
        cursor = self.db.aql.execute("FOR i IN RDBMS RETURN i._key")
        db_cmdb = set(list(cursor))
        added = db_aliyun - db_cmdb
        removed = db_cmdb - db_aliyun
        # insert new kvs
        insert_list = []
        for iid in added:
            doc = db_mapping[iid]
            doc['_key'] = iid
            doc['State'] = True
            doc['Tags'] = RDS.get_tags(iid)
            insert_list.append(doc)
        self.db.collection('RDBMS').insert_many(insert_list)
        # delete removed kvs
        remove_list = []
        for iid in removed:
            doc = {}
            doc['_key'] = iid
            remove_list.append(doc)
        self.db.collection('RDBMS').delete_many(remove_list)
        # update exist kvs
        update_list = []
        for iid in (db_aliyun - added):
            doc = db_mapping[iid]
            doc['_key'] = iid
            doc['State'] = True
            doc['Tags'] = RDS.get_tags(iid)
            update_list.append(doc)
        self.db.collection('RDBMS').replace_many(update_list)

    @print_star_stop
    def sync_ip(self):
        cursor = self.db.aql.execute("FOR i IN IpAddress RETURN i._key")
        ip_cmdb = set(list(cursor))

        # server ipaddress
        ip_fields = ["InnerIpAddress", "PublicIpAddress"]
        for ip_field in ip_fields:
            cursor = self.db.aql.execute("""
              RETURN FLATTEN(
                FOR i IN Server
                  RETURN i.{0}.IpAddress
              )
            """.format(ip_field))
            ips = list(cursor)[0]
            # insert new ips
            insert_list = []
            added = set(ips) - ip_cmdb
            for ip in added:
                if ip_field == "InnerIpAddress":
                    doc = {'_key': ip, 'Type': 'intranet', 'IpAddress': ip}
                else:
                    doc = {'_key': ip, 'Type': 'internet', 'IpAddress': ip}
                insert_list.append(doc)
            self.db.collection('IpAddress').insert_many(insert_list)


        # slb ipaddress
        cursor = self.db.aql.execute("""
          FOR i IN LoadBalance
            RETURN {'_key': i.Address, 'Type': i.AddressType, 'IpAddress': i.Address}
        """)
        ip_dict = {i['_key']: i for i in cursor}
        # insert new ips
        insert_list = []
        added = set(ip_dict.keys()) - ip_cmdb
        for ip in added:
            insert_list.append(ip_dict[ip])
        self.db.collection('IpAddress').insert_many(insert_list)

        cursor = self.db.aql.execute("""
          FOR i IN IpAddress
           let server_ip_in = (
            for x in Server
             return FLATTEN([x.PublicIpAddress.IpAddress, LENGTH(x.InnerIpAddress.IpAddress) ? x.InnerIpAddress.IpAddress : x.VpcAttributes.PrivateIpAddress.IpAddress])[0]
          )
           let server_ip_out = (
             for xi in Server
               return FLATTEN([xi.PublicIpAddress.IpAddress, LENGTH(xi.InnerIpAddress.IpAddress) ? xi.InnerIpAddress.IpAddress : xi.VpcAttributes.PrivateIpAddress.IpAddress])[1]
          )
 
          let slb_ip =(
            FOR s IN LoadBalance
              RETURN s.Address
         )
          filter i._key not in server_ip_in and i._key not in slb_ip and i._key not in server_ip_out
           return i._key
            """)
        removed = list(cursor)
        removed_list = []
        for ip in removed:
            doc = {"_key":ip}
            removed_list.append(doc)
        self.db.collection('IpAddress').delete_many(removed_list)


    @print_star_stop
    def sync_account(self):
        cfg = ConfigParser.ConfigParser()
        cfg.optionxform = str
        cfg_dir = os.path.dirname(__file__)
        cfg.read(os.path.join(os.path.dirname(cfg_dir), 'aliyun', 'config.ini'))
        cursor = self.db.aql.execute("FOR i IN Account RETURN i.Name")
        account_cmdb = set(list(cursor))
        account_aliyun = set(cfg.sections())
        added = account_aliyun - account_cmdb
        removed = account_cmdb - account_aliyun
        # insert new account
        insert_list = []
        for section in added:
            ACCESSKEY = cfg.get(section, 'ACCESSKEY')
            doc = {'_key': ACCESSKEY, 'Name': section}
            insert_list.append(doc)
        self.db.collection('Account').insert_many(insert_list)
        # remove old account
        remove_list = []
        for section in removed:
            ACCESSKEY = cfg.get(section, 'ACCESSKEY')
            doc = {'_key': ACCESSKEY, 'Name': section}
            remove_list.append(doc)
        self.db.collection('Account').delete_many(remove_list)

    @print_star_stop
    def sync_app(self):
        cursor = self.db.aql.execute("""
          FOR i IN Application
            RETURN i._key
        """)
        app_cmdb = set(list(cursor))
        app_aliyun = []
        collections = ["Server", "LoadBalance", "RDBMS" ]  # add in the feature
        for col in collections:
            cursor = self.db.aql.execute("""
              FOR i IN {0}
                FILTER 'AppName' IN i.Tags.Tag[*].TagKey OR 'appname' IN i.Tags.Tag[*].TagKey
                RETURN KEEP(i, 'Tags')
            """.format(col))
            rows = list(cursor)
            for row in rows:
                for tag in row['Tags']['Tag']:
                    if tag['TagKey'] in ['AppName', 'appname']:
                        app_aliyun.extend(tag['TagValue'].split(','))
        added = set(app_aliyun) - app_cmdb
        removed = app_cmdb - set(app_aliyun)
        # insert new apps
        insert_list = []
        for iid in added:
            doc = {'_key': iid, 'Name': iid}
            insert_list.append(doc)
        self.db.collection('Application').insert_many(insert_list)
        # remove old apps
        remove_list = []
        for iid in removed:
            remove_list.append({'_key': iid})
        self.db.collection('Application').delete_many(remove_list)

    @print_star_stop
    def sync_disk(self):
        disk_mapping = {i['DiskId']: i for i in ECS.get_disks()}
        disk_aliyun = set(disk_mapping.keys())
        cursor = self.db.aql.execute("FOR i IN Disk RETURN i._key")
        disk_cmdb = set(list(cursor))
        added = disk_aliyun - disk_cmdb
        removed = disk_cmdb - disk_aliyun
        # insert new disk
        insert_list = []
        for iid in added:
            doc = disk_mapping[iid]
            doc['_key'] = iid
            insert_list.append(doc)
        self.db.collection('Disk').insert_many(insert_list)
        # remove old disk
        remove_list = []
        for iid in removed:
            remove_list.append({'_key': iid})
        self.db.collection('Disk').delete_many(remove_list)

    @print_star_stop
    def main(self):
        self.sync_server()
        self.sync_lb()
        self.sync_nosql()
        self.sync_rdbms()
        self.sync_ip()
        self.sync_account()
        self.sync_app()
        self.sync_disk()


if __name__ == '__main__':
    vertex = Vertex()
    vertex.main()
