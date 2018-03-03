import arangojs, { aql } from 'arangojs'

let db = arangojs(process.env.API_URL)
db.useDatabase('CMDB')

export const getRDBMSItem = (key) => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  return db.query(aql`
    FOR i IN RDBMS
      FILTER i._key == ${key}
      RETURN {
        'DBInstanceId': i.DBInstanceId,
        'DBInstanceDescription': i.DBInstanceDescription,
        'DBInstanceStatus': i.DBInstanceStatus,
        'DBInstanceCPU': i.DBInstanceCPU,
        'DBInstanceMemory': i.DBInstanceMemory,
        'DBInstanceStorage': i.DBInstanceStorage,
        'DBInstanceType': i.DBInstanceType,
        'ConnectionString': i.ConnectionString,
        'MaxIOPS': i.MaxIOPS,
        'CreationTime': i.CreationTime,
        'ExpireTime': i.ExpireTime,
        'ZoneId': i.ZoneId,
        'State': i.State ? 'Online' : 'Offline'
      }
  `)
    .then(
      cursor => cursor.all(),
      err => console.error(err.stack)
    )
}

export const getRDBMSList = () => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  return db.query(`
    FOR i IN RDBMS
      RETURN {
        'DBInstanceId': i.DBInstanceId,
        'DBInstanceDescription': i.DBInstanceDescription,
        'DBInstanceStatus': i.DBInstanceStatus,
        'DBInstanceCPU': i.DBInstanceCPU,
        'DBInstanceMemory': i.DBInstanceMemory,
        'DBInstanceStorage': i.DBInstanceStorage,
        'DBInstanceType': i.DBInstanceType,
        'ExpireTime': i.ExpireTime,
        'ZoneId': i.ZoneId,
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

export const expRDBMSItem = () => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  return db.query(aql`
    FOR i IN RDBMS
      RETURN {
        'DBInstanceId': i.DBInstanceId,
        'DBInstanceDescription': i.DBInstanceDescription,
        'DBInstanceStatus': i.DBInstanceStatus,
        'DBInstanceCPU': i.DBInstanceCPU,
        'DBInstanceMemory': i.DBInstanceMemory,
        'DBInstanceStorage': i.DBInstanceStorage,
        'DBInstanceType': i.DBInstanceType,
        'ConnectionString': i.ConnectionString,
        'MaxIOPS': i.MaxIOPS,
        'CreationTime': i.CreationTime,
        'ExpireTime': i.ExpireTime,
        'ZoneId': i.ZoneId,
        'State': i.State ? 'Online' : 'Offline'
      }
  `)
    .then(
      cursor => cursor.all(),
      err => console.error(err.stack)
    )
}
