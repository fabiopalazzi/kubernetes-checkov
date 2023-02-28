#Create kube resource declared
kubectl create -f .

#Wait mongo db replica is running
kubectl wait --for=condition=Running pod/mongod-0

#Configure mongodb primary instance
./config/init_mongo.sh

#Show minikube page of flask load balancer
minikube service flask-lb