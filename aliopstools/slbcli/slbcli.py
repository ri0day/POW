#coding: utf-8
import click
import os
from api import AliyunSlb, DataSource


@click.group()
def cli():
    """
  Example:
  python slbcli.py add --balancerid xxxx --backendid xxxxx
    """
    global accesskey
    global access_secret
    global region
    accesskey = os.environ.get('ACCESSKEY', None)
    access_secret = os.environ.get('ACCESS_SECRET', None)
    region = os.environ.get('REGION', None)
    if all([accesskey, access_secret, region]):
        pass
    else:
        print 'os env ACCESSKEY,ACCESS_SECRET,REGION required.'
        os._exit(1)


@cli.command()
@click.option('--balancerid', help='aliyun load balancer id')
@click.option('--appname', help='aliyun tags')
def status(balancerid=None,appname=None):
    """
    python slbcli.py status
    python slbcli.py status --balancerid lb-xxxx
    :param balancerid: loadbalancerid
    :return: status
    """
    slb = AliyunSlb(accesskey, access_secret, region)
    if balancerid:
        click.echo(slb.slb_status(balancerid))
    elif appname:
        d = DataSource()
        lbids = d.App_to_balancerid(str(appname)) 
        if lbids:
            for id in lbids:
                click.echo(slb.slb_status(id))
        else:
            print 'can not find lbs by tag,check your cmdb data,exit'
    else:
        click.echo(slb.slb_status(None))

@cli.command()
@click.option('--balancerid', help='aliyun load balancer id')
@click.option('--backendid', help='aliyun backends server id')
def add(balancerid, backendid):
    """
    python slbcli.py add --balancerid lb-xxx --backendid ecs-xxxx
    :param balancerid: loadbalancerid
    :param backendid: ecs backendid
    :return:
    """
    slb = AliyunSlb(accesskey, access_secret, region)
    click.echo(slb.add_slb_backends(str(balancerid), str(backendid)))


@cli.command()
@click.option('--balancerid', help='aliyun load balancer id')
@click.option('--backendid', help='aliyun backends server id')
def remove(balancerid, backendid):
    """
    python slbcli.py remove --balancerid lb-xxx --backendid ecs-xxxx
    :param balancerid: loadbalancerid
    :param backendid: ecs backendid
    :return:
    """
    slb = AliyunSlb(accesskey, access_secret, region)
    click.echo(slb.remove_slb_backends(str(balancerid), str(backendid)))


@cli.command()
@click.option('--balancerid', help='aliyun load balancer id')
def lsvg(balancerid):
    """
    python slbcli.py lsvg --balancerid lb-xxx
    :param balancerid: loadbalancerid
    :return:
    """
    slb = AliyunSlb(accesskey, access_secret, region)
    click.echo(slb.list_vgroups(str(balancerid)))


@cli.command()
@click.option('--vgid', help='aliyun loadbalancer virtualgroup id')
@click.option('--backendid', help='aliyun backend ecs id')
@click.option('--port', help='virtualgroup backens backends port')
def vadd(vgid, backendid, port):
    """
    python slbcli.py vadd --vgid rsp-xxx --backendid ecs-xxx --port 8080
    :param vgid: loadbalancer virtualgroupid
    :param backendid: loadbalancerid
    :param port: backends services listen port
    :return:
    """
    slb = AliyunSlb(accesskey, access_secret, region)
    click.echo(slb.add_vg_servers(str(vgid), str(backendid), str(port)))


@cli.command()
@click.option('--vgid', help='aliyun loadbalancer virtualgroup id', type=str)
@click.option('--backendid', help='aliyun backend ecs id', type=str)
@click.option('--port', help='virtualgroup backens backends port', type=str)
def vremove(vgid, backendid, port):
    """
    python slbcli.py vremove --vgid rsp-xxx --backendid ecs-xxx --port 8080
    :param vgid: loadbalancer virtualgroupid
    :param backendid: loadbalancerid
    :param port: backends services listen port
    :return:
    """
    slb = AliyunSlb(accesskey, access_secret, region)
    click.echo(slb.remove_vg_servers(str(vgid), str(backendid), str(port)))

@cli.command()
@click.option('--appname', help='app tag in cmdb and aliyun', type=str)
@click.option('--backendid', help='aliyun backend ecs id', type=str)
def appadd(appname, backendid):
    slb = AliyunSlb(accesskey, access_secret, region)
    d = DataSource()
    lbids = d.App_to_balancerid(str(appname))
    if not lbids:
        print 'can not find lbs by tag,check your cmdb data,exit'
        return None
    else:
        for  id  in lbids:
            click.echo(slb.add_slb_backends(str(id), str(backendid)))

@cli.command()
@click.option('--appname', help='app tag in cmdb and aliyun', type=str)
@click.option('--backendid', help='aliyun backend ecs id', type=str)
def appremove(appname, backendid):
    slb = AliyunSlb(accesskey, access_secret, region)
    d = DataSource()
    lbids = d.App_to_balancerid(str(appname))
    if not lbids:
        print 'can not find lbs by tag,check your cmdb data,exit'
        return None
    else:
        for  id  in lbids:
            click.echo(slb.remove_slb_backends(str(id), str(backendid)))

@cli.command()
@click.option('--balancerid', help='aliyun load balancer id')
@click.option('--backendid', help='aliyun backends server id')
def disablebyweight(balancerid, backendid):
    """
    python slbcli.py blockbyweight --balancerid lb-xxx --backendid ecs-xxxx
    :param balancerid: loadbalancerid
    :param backendid: ecs backendid
    :return:
    """
    slb = AliyunSlb(accesskey, access_secret, region)
    click.echo(slb.disable_backends_by_weight(str(balancerid), str(backendid)))

@cli.command()
@click.option('--balancerid', help='aliyun load balancer id')
@click.option('--backendid', help='aliyun backends server id')
def enablebyweight(balancerid, backendid):
    """
    python slbcli.py blockbyweight --balancerid lb-xxx --backendid ecs-xxxx
    :param balancerid: loadbalancerid
    :param backendid: ecs backendid
    :return:
    """
    slb = AliyunSlb(accesskey, access_secret, region)
    click.echo(slb.enable_backends_by_weight(str(balancerid), str(backendid)))

if __name__ == '__main__':
    cli()

