[![pre-commit](https://github.com/Rashid-77/shopogolik/actions/workflows/check.yml/badge.svg)](https://github.com/Rashid-77/shopogolik/actions/workflows/check.yml)


The goal of this project is to experiments with kubernetes.

Python3.10, FastApi, Postgress, docker compose V2, Kubernetes 1.28 were used.

The project consist of: 

- authentication service 
- user service
- order service
- product service
- payment service
- logistic service
- notification service

At this moment Saga pattern realized to make order.
Order depends on the avialability products in order, enough money on in-shop user account and available courier'

**Deploy to kubernetes cluster**

First of all you need installed Minikube

Then start it:

<code>minikube start</code>

Enable ingress

<code>minikube addons enable ingress</code>

<code>minikube addons enable dashboard</code>

Add host name to file /etc/hosts, to resolve a name into an address

<code>echo "$(minikube ip) arch.homework" | sudo tee -a /etc/hosts</code>
 
Spin up your claster using the helm

First install <a href="https://helm.sh/docs/intro/install/"> helm.</a>

All services will be installed in the default namespace.

From project root run:

<code>helm install kafka helm-kafka-chart/</code>

After kafka-job has done its job, check if really topic were created.
Go to kafka pod and run 

<code>kafka-topics --bootstrap-server kafka-service:9092 --list</code>

If there is no topics: "order", "product", "payment", "logistic", then create it manually.

For example, to create topic order paste and run in kafka pod:

<code>kafka-topics --bootstrap-server kafka-service:9092 --create --topic order</code>

After all topics created start all other services.

<code>helm install postgres helm-postgres-chart/</code>

<code>helm install auth helm-auth-chart/</code>

<code>helm install shopogolik helm-backend-chart/</code>

<code>helm install postgr-product helm-product-db-chart/</code>

<code>helm install postgr-payment helm-payment-db-chart/</code>

<code>helm install postgr-order helm-order-db-chart/</code>

<code>helm install postgr-logistic helm-logistic-db-chart/</code>

<code>helm install product helm-product-chart/</code>

<code>helm install payment helm-payment-chart/</code>

<code>helm install order helm-order-chart/</code>

<code>helm install logistic helm-logistic-chart/</code>

now you can see its status

<code>helm list</code>

Then check the app using a postman collections.

To use postman tests install newman:

**Testing**

<code>newman run m-hw9-order-OK.postman_collection.json --delay-request 1000 --env-var BASE_URL=arch.homework</code>

<code>newman run m-hw9-Order-Fail.postman_collection.json --delay-request 1000 --env-var BASE_URL=arch.homework</code>

**To shutdown app**:

Get installed services:

<code>helm list</code>

and shutdown them all.

For example 

<code>helm uninstall shopogolik, order, product</code>
