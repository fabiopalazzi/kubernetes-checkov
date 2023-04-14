### Connect to first mongodb instance using bash
### Run mongo sh
### Paste these two commands that define mongodb replica strucuture
## First commands
```json
rs.initiate({ _id: "MainRepSet", version: 1, members: [ 
 { _id: 0, host: "mongod-0.mongodb-service.default.svc.cluster.local:27017" }, 
 { _id: 1, host: "mongod-1.mongodb-service.default.svc.cluster.local:27017" }, 
 { _id: 2, host: "mongod-2.mongodb-service.default.svc.cluster.local:27017" } 
]});
```