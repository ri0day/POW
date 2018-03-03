import arangojs, { aql } from 'arangojs'

let db = arangojs(process.env.API_URL)
db.useDatabase('CMDB')

export const getServerItem = (key) => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  return db.query(aql`
    FOR i IN Server
      FILTER i._key == ${key}
      LET disk = (
        FOR j IN Disk
          FILTER j.InstanceId == i.InstanceId
          RETURN CONCAT(j.Size, "/", j.Type)
      )
      LET tags = (
        FOR t IN InstanceApplication
          FILTER DOCUMENT(t._to).InstanceId == i.InstanceId
          RETURN DOCUMENT(t._from).Name
      )
      RETURN {
        'InstanceId': i.InstanceId,
        'InstanceName': i.InstanceName,
        'InstanceChargeType': i.InstanceChargeType,
        'InstanceNetworkType': i.InstanceNetworkType,
        'InternetMaxBandwidthOut': i.InternetMaxBandwidthOut,
        'InnerIpAddress': LENGTH(i.InnerIpAddress.IpAddress) ? i.InnerIpAddress.IpAddress : i.VpcAttributes.PrivateIpAddress.IpAddress,
        'PublicIpAddress': i.PublicIpAddress.IpAddress,
        'ZoneId': i.ZoneId,
        'Cpu': i.Cpu,
        'Memory': i.Memory,
        'Disk': disk,
        'OSType': i.OSType,
        'ExpiredTime': i.ExpiredTime,
        'CreationTime': i.CreationTime,
        'Description': i.Description,
        'State': i.State ? 'Online' : 'Offline',
        'Tags': tags
      }
  `)
    .then(
      cursor => cursor.all(),
      err => console.error(err.stack)
    )
}

export const getServerList = () => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  return db.query(`
    FOR i IN Server
      LET disk = (
        FOR j IN Disk
          FILTER j.InstanceId == i.InstanceId
          RETURN CONCAT(j.Size, "/", j.Type)
      )
      LET tags = (
        FOR t IN InstanceApplication
          FILTER DOCUMENT(t._to).InstanceId == i.InstanceId
          RETURN DOCUMENT(t._from).Name
      )
      RETURN {
        'InstanceId': i.InstanceId,
        'InstanceName': i.InstanceName,
        'InnerIpAddress': LENGTH(i.InnerIpAddress.IpAddress) ? i.InnerIpAddress.IpAddress : i.VpcAttributes.PrivateIpAddress.IpAddress,
        'PublicIpAddress': i.PublicIpAddress.IpAddress,
        'ZoneId': i.ZoneId,
        'Cpu': i.Cpu,
        'Memory': i.Memory,
        'Disk': disk,
        'ExpiredTime': i.ExpiredTime,
        'State': i.State ? 'Online' : 'Offline',
        'Tags': tags,
        'Access_key': i.Access_key,
        '_key': i._key
      }
  `)
    .then(
      cursor => cursor.all(),
      err => console.error(err.stack)
    )
}

export const expServerItem = () => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  return db.query(aql`
    FOR i IN Server
      LET disk = (
        FOR j IN Disk
          FILTER j.InstanceId == i.InstanceId
          RETURN CONCAT(j.Size, "/", j.Type)
      )
      LET tags = (
        FOR t IN InstanceApplication
          FILTER DOCUMENT(t._to).InstanceId == i.InstanceId
          RETURN DOCUMENT(t._from).Name
      )
      LET account = (
        FOR a IN Account 
          FILTER a._key == i.Access_key
          RETURN a.Name
      )
      RETURN {
        'InstanceId': i.InstanceId,
        'InstanceName': i.InstanceName,
        'InstanceChargeType': i.InstanceChargeType,
        'InstanceNetworkType': i.InstanceNetworkType,
        'InternetMaxBandwidthOut': i.InternetMaxBandwidthOut,
        'InnerIpAddress': LENGTH(i.InnerIpAddress.IpAddress) ? i.InnerIpAddress.IpAddress : i.VpcAttributes.PrivateIpAddress.IpAddress,
        'PublicIpAddress': i.PublicIpAddress.IpAddress,
        'ZoneId': i.ZoneId,
        'Cpu': i.Cpu,
        'Memory': i.Memory,
        'Disk': CONCAT_SEPARATOR("| ",disk),
        'OSType': i.OSType,
        'ExpiredTime': i.ExpiredTime,
        'CreationTime': i.CreationTime,
        'Description': i.Description,
        'State': i.State ? 'Online' : 'Offline',
        'Tags': tags,
        'Account': CONCAT(account)
      }
  `)
    .then(
      cursor => cursor.all(),
      err => console.error(err.stack)
    )
}
