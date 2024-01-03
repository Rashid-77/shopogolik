
The goal of this project is to experiments with kubernetes.
Python3.10, FastApi, Postgress, docker compose V2 are used.

The project consist of authentication service and a user service

**Deploy to kubernetes cluster**

First of all you need installed Minikube

Then start it:

<code>minikube start</code>

Enalbe ingress

<code>minikube addons enable ingress</code>

<code>minikube addons enable dashboard</code>

Add host name to file /etc/hosts, to resolve a name into an address

<code>echo "$(minikube ip) arch.homework" | sudo tee -a /etc/hosts</code>
 
Spin up your claster using the helm

First install <a href="https://helm.sh/docs/intro/install/"> helm.</a>

From project root run:

<code>helm install postgres helm-postgres-chart/</code>

<code>helm install auth helm-auth-chart/</code>

<code>helm install shopogolik helm-backend-chart/</code>

now you can see its status

<code>helm list</code>

And then check the app using a browser

http://arch.homework/docs  

There is a postman test. To use it install newman, then run:

<code>newman run micriservice-hw5.postman_collection.json</code>

**Testing**

To test use newman:

<code>newman run micriservice-hw5.postman_collection.json --env-var "BASE_URL=arch.homework"</code>


**To shutdown app**:

<code>helm uninstall shopogolik</code>

<code>helm uninstall auth</code>

<code>helm uninstall postgres</code>

