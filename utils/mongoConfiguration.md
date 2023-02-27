### Connect to first mongodb instance using bash
### Run mongo sh
### Paste these two commands that define mongodb replica strucuture
## First commands
```json
rs.initiate({ _id: "MainRepSet", version: 1, 
members: [ 
 { _id: 0, host: "mongod-0.mongodb-service.default.svc.cluster.local:27017" }, 
 { _id: 1, host: "mongod-1.mongodb-service.default.svc.cluster.local:27017" }, 
 { _id: 2, host: "mongod-2.mongodb-service.default.svc.cluster.local:27017" } ]});
{
	"ok" : 1,
	"$clusterTime" : {
		"clusterTime" : Timestamp(1601481520, 1),
		"signature" : {
			"hash" : BinData(0,"AAAAAAAAAAAAAAAAAAAAAAAAAAA="),
			"keyId" : NumberLong(0)
		}
	},
	"operationTime" : Timestamp(1601481520, 1)
}
MainRepSet:SECONDARY>  rs.status();
{
	"set" : "MainRepSet",
	"date" : ISODate("2020-09-30T15:59:04.013Z"),
	"myState" : 1,
	"term" : NumberLong(1),
	"syncSourceHost" : "",
	"syncSourceId" : -1,
	"heartbeatIntervalMillis" : NumberLong(2000),
	"majorityVoteCount" : 2,
	"writeMajorityCount" : 2,
	"votingMembersCount" : 3,
	"writableVotingMembersCount" : 3,
	"optimes" : {
		"lastCommittedOpTime" : {
			"ts" : Timestamp(1601481536, 1),
			"t" : NumberLong(1)
		},
		"lastCommittedWallTime" : ISODate("2020-09-30T15:58:56.243Z"),
		"readConcernMajorityOpTime" : {
			"ts" : Timestamp(1601481536, 1),
			"t" : NumberLong(1)
		},
		"readConcernMajorityWallTime" : ISODate("2020-09-30T15:58:56.243Z"),
		"appliedOpTime" : {
			"ts" : Timestamp(1601481536, 1),
			"t" : NumberLong(1)
		},
		"durableOpTime" : {
			"ts" : Timestamp(1601481536, 1),
			"t" : NumberLong(1)
		},
		"lastAppliedWallTime" : ISODate("2020-09-30T15:58:56.243Z"),
		"lastDurableWallTime" : ISODate("2020-09-30T15:58:56.243Z")
	},
	"lastStableRecoveryTimestamp" : Timestamp(1601481533, 1),
	"electionCandidateMetrics" : {
		"lastElectionReason" : "electionTimeout",
		"lastElectionDate" : ISODate("2020-09-30T15:58:52.739Z"),
		"electionTerm" : NumberLong(1),
		"lastCommittedOpTimeAtElection" : {
			"ts" : Timestamp(0, 0),
			"t" : NumberLong(-1)
		},
		"lastSeenOpTimeAtElection" : {
			"ts" : Timestamp(1601481520, 1),
			"t" : NumberLong(-1)
		},
		"numVotesNeeded" : 2,
		"priorityAtElection" : 1,
		"electionTimeoutMillis" : NumberLong(10000),
		"numCatchUpOps" : NumberLong(0),
		"newTermStartDate" : ISODate("2020-09-30T15:58:53.164Z"),
		"wMajorityWriteAvailabilityDate" : ISODate("2020-09-30T15:58:54.898Z")
	},
	"members" : [
		{
			"_id" : 0,
			"name" : "mongod-0.mongodb-service.default.svc.cluster.local:27017",
			"health" : 1,
			"state" : 1,
			"stateStr" : "PRIMARY",
			"uptime" : 283,
			"optime" : {
				"ts" : Timestamp(1601481536, 1),
				"t" : NumberLong(1)
			},
			"optimeDate" : ISODate("2020-09-30T15:58:56Z"),
			"syncSourceHost" : "",
			"syncSourceId" : -1,
			"infoMessage" : "",
			"electionTime" : Timestamp(1601481532, 1),
			"electionDate" : ISODate("2020-09-30T15:58:52Z"),
			"configVersion" : 1,
			"configTerm" : 1,
			"self" : true,
			"lastHeartbeatMessage" : ""
		},
		{
			"_id" : 1,
			"name" : "mongod-1.mongodb-service.default.svc.cluster.local:27017",
			"health" : 1,
			"state" : 2,
			"stateStr" : "SECONDARY",
			"uptime" : 22,
			"optime" : {
				"ts" : Timestamp(1601481536, 1),
				"t" : NumberLong(1)
			},
			"optimeDurable" : {
				"ts" : Timestamp(1601481536, 1),
				"t" : NumberLong(1)
			},
			"optimeDate" : ISODate("2020-09-30T15:58:56Z"),
			"optimeDurableDate" : ISODate("2020-09-30T15:58:56Z"),
			"lastHeartbeat" : ISODate("2020-09-30T15:59:02.847Z"),
			"lastHeartbeatRecv" : ISODate("2020-09-30T15:59:02.461Z"),
			"pingMs" : NumberLong(0),
			"lastHeartbeatMessage" : "",
			"syncSourceHost" : "mongod-0.mongodb-service.default.svc.cluster.local:27017",
			"syncSourceId" : 0,
			"infoMessage" : "",
			"configVersion" : 1,
			"configTerm" : 1
		},
		{
			"_id" : 2,
			"name" : "mongod-2.mongodb-service.default.svc.cluster.local:27017",
			"health" : 1,
			"state" : 2,
			"stateStr" : "SECONDARY",
			"uptime" : 22,
			"optime" : {
				"ts" : Timestamp(1601481536, 1),
				"t" : NumberLong(1)
			},
			"optimeDurable" : {
				"ts" : Timestamp(1601481536, 1),
				"t" : NumberLong(1)
			},
			"optimeDate" : ISODate("2020-09-30T15:58:56Z"),
			"optimeDurableDate" : ISODate("2020-09-30T15:58:56Z"),
			"lastHeartbeat" : ISODate("2020-09-30T15:59:02.848Z"),
			"lastHeartbeatRecv" : ISODate("2020-09-30T15:59:02.472Z"),
			"pingMs" : NumberLong(0),
			"lastHeartbeatMessage" : "",
			"syncSourceHost" : "mongod-0.mongodb-service.default.svc.cluster.local:27017",
			"syncSourceId" : 0,
			"infoMessage" : "",
			"configVersion" : 1,
			"configTerm" : 1
		}
	],
	"ok" : 1,
	"$clusterTime" : {
		"clusterTime" : Timestamp(1601481536, 1),
		"signature" : {
			"hash" : BinData(0,"AAAAAAAAAAAAAAAAAAAAAAAAAAA="),
			"keyId" : NumberLong(0)
		}
	},
	"operationTime" : Timestamp(1601481536, 1)
}
```
## Second Command
```json
db.getSiblingDB("admin").createUser({
    user : "demoadmin",
    pwd  : "demopwd123",
    roles: [ { role: "root", db: "admin" } ]
});
```