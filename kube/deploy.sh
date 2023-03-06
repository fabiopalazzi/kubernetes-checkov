#Create kube resource declared
kubectl create -f .

#Wait mongo db replica is running
kubectl wait --for=condition=Ready pod/mongod-0
kubectl wait --for=condition=Ready pod/mongod-1
kubectl wait --for=condition=Ready pod/mongod-2

#Configure mongodb primary instance
kubectl exec -it mongod-0 -- mongosh <<EOF
rs.initiate({ _id: "MainRepSet", version: 1, members: [ 
 { _id: 0, host: "mongod-0.mongodb-service.default.svc.cluster.local:27017" }, 
 { _id: 1, host: "mongod-1.mongodb-service.default.svc.cluster.local:27017" }, 
 { _id: 2, host: "mongod-2.mongodb-service.default.svc.cluster.local:27017" }
]});
EOF

#Show minikube page of flask load balancer
minikube service flask-lb