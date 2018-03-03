from __future__ import print_function
from arango import ArangoClient, ArangoError


def main():
    client = ArangoClient(
        host='192.168.0.37',
        username='root',
        password='zbjf123!@#'
    )

    # create database
    try:
        client.create_database('CMDB')
    except ArangoError:
        print('database already created.')
    db = client.database('CMDB')

    # create collections
    collection_list = [
        # vertex
        'Account', 'Application', 'Disk', 'IpAddress',
        'LoadBalance', 'NoSQL', 'RDBMS', 'Server',
        # edge
        'InstanceAccount', 'InstanceApplication',
        'IpaddrInstance', 'LoadBalanceBackendServers'
    ]
    for col in collection_list:
        try:
            db.create_collection(col)
        except ArangoError:
            print('[%s] collection already created.' % col)

    print('done.')

if __name__ == '__main__':
    main()
