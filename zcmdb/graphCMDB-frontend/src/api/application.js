
import arangojs, { aql } from 'arangojs'

let db = arangojs(process.env.API_URL)
db.useDatabase('CMDB')

export const getApplicationItem = (key) => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  return db.query(aql`
    for x in Application
      FILTER x.Name == ${key}
      LET slb = (
      FOR i IN LoadBalance
        FILTER x.Name IN i.Tags.Tag[*].TagValue
          RETURN i.LoadBalancerId 
      )
      LET servers = (
      FOR i IN Server
        FILTER x.Name IN i.Tags.Tag[*].TagValue
      RETURN i.InstanceName 
      )
     LET rdbms = (
     FOR i IN RDBMS
       FILTER CONTAINS(i.Tags.Tag[*].TagValue,x.Name)
     RETURN i.ConnectionString
      )

    RETURN {
    "APPNAME":x.Name,
    "SLB": slb,
    "SERVERS": servers[**],
    "RDBMS":rdbms[**]
  }
  `)
    .then(
      cursor => cursor.all(),
      err => console.error(err.stack)
    )
}

export const getApplicationList = () => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  return db.query(`
    for x in Application
      LET slb = (
      FOR i IN LoadBalance
        FILTER x.Name IN i.Tags.Tag[*].TagValue
          RETURN i.LoadBalancerId
      )
      LET servers = (
      FOR i IN Server
        FILTER x.Name IN i.Tags.Tag[*].TagValue
      RETURN i.InstanceName 
      )
     LET rdbms = (
     FOR i IN RDBMS
       FILTER CONTAINS(i.Tags.Tag[*].TagValue,x.Name)
     RETURN i.ConnectionString
      )

    RETURN {
    "APPNAME":x.Name,
    "SLB": slb,
    "SERVERS": servers[**],
    "RDBMS":rdbms[**]
    }
  `)

    .then(
      cursor => cursor.all(),
      err => console.error(err.stack)
    )
}

export const expApplicationItem = () => {
  db.useBearerAuth(localStorage.getItem('Authorization'))
  return db.query(aql`
    for x in Application
      LET slb = (
      FOR i IN LoadBalance
        FILTER x.Name IN i.Tags.Tag[*].TagValue
          RETURN i.LoadBalancerId
      )
      LET servers = (
      FOR i IN Server
        FILTER x.Name IN i.Tags.Tag[*].TagValue
      RETURN i.InstanceName
      )
     LET rdbms = (
     FOR i IN RDBMS
       FILTER CONTAINS(i.Tags.Tag[*].TagValue,x.Name)
     RETURN i.ConnectionString
      )

    RETURN {
    "APPNAME":x.Name,
    "SLB": slb,
    "SERVERS": servers[**],
    "RDBMS":rdbms[**]
   }
  `)
    .then(
      cursor => cursor.all(),
      err => console.error(err.stack)
    )
}
