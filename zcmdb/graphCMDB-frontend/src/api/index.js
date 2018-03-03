import arangojs, { aql } from 'arangojs'

let db = arangojs(process.env.API_URL)
db.useDatabase('CMDB')

export const getArangoSummary = (collection) => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  let col = db.collection(collection)
  return db.query(aql`
    FOR i IN ${col}
      COLLECT state = i.State
        WITH COUNT INTO number
      RETURN {
        State: state,
        Number: number
      }
  `)
    .then(
      cursor => cursor.all(),
      err => console.error(err.stack)
    )
}

export const getArangoData = (collection, fields = []) => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  let col = db.collection(collection)
  if (fields.length) {
    return db.query(aql`
      FOR doc IN ${col}
        RETURN KEEP(doc, ${fields})
    `)
      .then(
        cursor => cursor.all(),
        err => console.error(err.stack)
      )
  } else {
    return db.query(aql`
      FOR i IN ${col}
        RETURN i 
    `)
      .then(
        cursor => cursor.all(),
        err => console.error(err.stack)
      )
  }
}

export * from './loadbalance'
export * from './nosql'
export * from './rdbms'
export * from './server'
export * from './ipaddress'
export * from './application'
