# Kubetcl and docker commands:
1. docker push <local:image>
  * Before run: docker login to access to docker hub repo
2. minikube start
  * Init minikube to install kubernetes configuration locally
3. Bash script:
  * cd kube
  * execute: ```./deploy.sh``` to deploy cluster
  * execute: ```./destroy.sh``` to destroy cluster
4. Util commands:
  * how created pods with: kubectl get pods
  * ```minikube service <service-name>```: get url and port of service specified
7. Checkov command to find misconfigurations(first install checkov with pip): ```checkov -d . --framework kubernetes```