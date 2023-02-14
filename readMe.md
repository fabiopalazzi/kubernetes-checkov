# Kubetcl and docker commands:
1. docker push <local:image>
  * Before run: docker login to access to pdocker hub repo
2. minikube start --memory 2048 --cpus 2
  * Init minikube to install kubernetes configuration locally
3. 
  * cd kube
  * kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=<path/to/.docker/config.json> \
    --type=kubernetes.io/dockerconfigjson
4. create kubectl flask cluster: kubectl create -f flask-config.yaml
  * Show created pods with: kubectl get pods
5. create kubectl lb: kubectl create -f flask-lb-config.yaml
  * Show created lb with: kubectl get svc
6. minikube service <load-balancer-name> to get url and port of load balancer

7. Checkov command (first install checkov with pip)
  * checkov -d . --framework kubernetes