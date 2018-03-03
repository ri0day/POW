import arangojs, { aql } from 'arangojs'

let db = arangojs(process.env.API_URL)
db.useDatabase('CMDB')

export const getNoSQLItem = (key) => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  return db.query(aql`
    FOR i IN NoSQL
      FILTER i._key == ${key}
      RETURN {
        'InstanceId': i.InstanceId,
        'InstanceName': i.InstanceName,
        'InstanceStatus': i.InstanceStatus,
        'InstanceClass': i.InstanceClass,
        'ZoneId': i.ZoneId,
        'EndTime': i.EndTime,
        'Connections': i.Connections,
        'ConnectionDomain': i.ConnectionDomain,
        'Port': i.Port,
        'State': i.State ? 'Online' : 'Offline'
      }
  `)
    .then(
      cursor => cursor.all(),
      err => console.error(err.stack)
    )
}

export const getNoSQLList = () => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  return db.query(`
    FOR i IN NoSQL
      RETURN {
        'InstanceId': i.InstanceId,
        'InstanceName': i.InstanceName,
        'InstanceStatus': i.InstanceStatus,
        'InstanceClass': i.InstanceClass,
        'ZoneId': i.ZoneId,
        'EndTime': i.EndTime,
        'Access_key': i.Access_key,
        'State': i.State ? 'Online' : 'Offline',
        '_key': i._key
      }
  `)
    .then(
      cursor => cursor.all(),
      err => console.error(err.stack)
    )
}

export const expNoSQLItem = () => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  return db.query(aql`
    FOR i IN NoSQL
      RETURN {
        'InstanceId': i.InstanceId,
        'InstanceName': i.InstanceName,
        'InstanceStatus': i.InstanceStatus,
        'InstanceClass': i.InstanceClass,
        'ZoneId': i.ZoneId,
        'EndTime': i.EndTime,
        'Connections': i.Connections,
        'ConnectionDomain': i.ConnectionDomain,
        'Port': i.Port,
        'State': i.State ? 'Online' : 'Offline'
      }
  `)
    .then(
      cursor => cursor.all(),
      err => console.error(err.stack)
    )
}
