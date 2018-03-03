import arangojs, { aql } from 'arangojs'

let db = arangojs(process.env.API_URL)
db.useDatabase('CMDB')

export const getIpAddressItem = (iid) => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  return db.query(aql`
    FOR i IN IpAddress
      FILTER i._id == ${iid}
      LET instance = (
        FOR j IN IpaddrInstance
          FILTER j._from == ${iid}
          RETURN j._to
      )
      RETURN {
        'IpAddress': i.IpAddress,
        'Type': i.Type,
        'Instance': instance
      }
  `)
    .then(
      cursor => cursor.all(),
      err => console.error(err.stack)
    )
}

export const getIpAddressList = () => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  return db.query(`
    FOR i IN IpAddress
      RETURN {
        'IpAddress': i.IpAddress,
        'Type': i.Type,
        '_id': i._id
      }
  `)
    .then(
      cursor => cursor.all(),
      err => console.error(err.stack)
    )
}
