import arangojs, { aql } from 'arangojs'

let db = arangojs(process.env.API_URL)
db.useDatabase('CMDB')

export const getLoadBalanceItem = (key) => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  return db.query(aql`
    FOR i IN LoadBalance
      FILTER i._key == ${key}
      RETURN {
        'LoadBalancerId': i.LoadBalancerId,
        'LoadBalancerName': i.LoadBalancerName,
        'LoadBalancerStatus': i.LoadBalancerStatus,
        'MasterZoneId': i.MasterZoneId,
        'SlaveZoneId': i.SlaveZoneId,
        'Address': i.Address,
        'AddressType': i.AddressType,
        'Bandwidth': i.Bandwidth,
        'BackendServers': i.BackendServers.BackendServer[*].ServerId,
        'State': i.State ? 'Online' : 'Offline'
      }
  `)
    .then(
      cursor => cursor.all(),
      err => console.error(err.stack)
    )
}

export const getLoadBalanceList = () => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  return db.query(`
    FOR i IN LoadBalance
      RETURN {
        'LoadBalancerId': i.LoadBalancerId,
        'LoadBalancerName': i.LoadBalancerName,
        'MasterZoneId': i.MasterZoneId,
        'Address': i.Address,
        'LoadBalancerStatus': i.LoadBalancerStatus,
        'State': i.State ? 'Online' : 'Offline',
        'Access_key': i.Access_key,
        '_key': i._key
      }
  `)
    .then(
      cursor => cursor.all(),
      err => console.error(err.stack)
    )
}

export const expLoadBalanceItem = () => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  return db.query(aql`
    FOR i IN LoadBalance
      RETURN {
        'LoadBalancerId': i.LoadBalancerId,
        'LoadBalancerName': i.LoadBalancerName,
        'LoadBalancerStatus': i.LoadBalancerStatus,
        'MasterZoneId': i.MasterZoneId,
        'SlaveZoneId': i.SlaveZoneId,
        'Address': i.Address,
        'AddressType': i.AddressType,
        'Bandwidth': i.Bandwidth,
        'BackendServers': i.BackendServers.BackendServer[*].ServerId,
        'State': i.State ? 'Online' : 'Offline'
      }
  `)
    .then(
      cursor => cursor.all(),
      err => console.error(err.stack)
    )
}
