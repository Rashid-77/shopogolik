
The goal of this project is to experiments with kubernetes.
Python3.10, FastApi, Postgress, docker compose V2 are used.

**How to use with docker compose**

To start project
Build project:

<code>bash build.sh</code>

Run containers:

<code>docker compose up</code>

Create db tables

<code>docker compose exec backend alembic upgrade head</code>

And access it through the browser:

<code>http://127.0.0.1:8000/docs</code>


**Deploy to kubernetes cluster**

You can spin up your claster step by step with kubernetes manifests, and watch the status of every instance. Or you can do it with helm

First of all you need installed Minikube

Then start it:

<code>minikube start</code>


**How to use with kubernetes**

<code>kubectl create -f ./kubernetes/persistent-volume.yml</code>

<code>kubectl get pv</code>

<code>kubectl create -f ./kubernetes/persistent-volume-claim.yml</code>

<code>kubectl get pvc</code>

<code>kubectl create -f ./kubernetes/postgres-secret.yml</code>

<code>kubectl create -f ./kubernetes/server-secret.yml</code>

<code>kubectl get secret</code>

<code>kubectl apply -f ./kubernetes/config_map.yml</code>

<code>kubectl get configmap</code>

<code>kubectl create -f ./kubernetes/postgres-deployment.yml</code>

<code>kubectl get deployment</code>

<code>kubectl create -f ./kubernetes/postgres-service.yml</code>

<code>kubectl get svc</code>

<code>kubectl create -f ./kubernetes/server-deployment.yml</code>

<code>kubectl create -f ./kubernetes/server-service.yml</code>

<code>kubectl create -f ./kubernetes/server-db-migrate.yml</code>

<code>kubectl get job</code>

<code>minikube addons enable ingress</code>      (if not enabled yet)

<code>kubectl apply -f ./kubernetes/minikube-ingress.yml</code>

<code>kubectl get ingress</code>

Add host name to file /etc/hosts, to resolve a name into an address

<code>echo "$(minikube ip) arch.homework" | sudo tee -a /etc/hosts</code>
 
 Now you can check the app with browser

 http://arch.homework/docs  

**How to use with Helm**

First install <a href="https://helm.sh/docs/intro/install/"> helm.</a>

To deploy app use command:

<code>helm install shopogolik ./helm-chart</code>

now you can see its status

<code>helm list</code>

Check the app with browser

http://arch.homework/docs 

To shutdown app:

<code>helm uninstall shopogolik</code>


**Testing**

Use this test to test crud on user.
The test should be conducted on a database with a single user created when the 
application was first launched, and no more users have been created. 

To test use newman:

<code>newman run microservice-03.postman_collection.json --env-var "BASE_URL=http://arch.homework"</code>

To test again drop all tables and restart app.


**Metrics**

Install Prometheus and Grafana

<code>helm repo add prometheus-community https://prometheus-community.github.io/helm-charts</code>

<code>helm repo update</code>

<code>helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
 --create-namespace -n monitoring -f metrics/kube-prometheus-stack.yml</code>

Add dashboard to grafana

<code>kubectl apply  -f metrics/kube-prometheus-stack.yml -f metrics/grafana.yml</code>

Now install ingress nginx:

<code>helm upgrade --install ingress-nginx ingress-nginx \\
  --repo https://kubernetes.github.io/ingress-nginx \\
  --namespace ingress-nginx --create-namespace \\
  --set controller.metrics.enabled=true \\
  --set controller.metrics.serviceMonitor.enabled=true \\
  --set controller.metrics.serviceMonitor.additionalLabels.release="kube-prometheus-stack"</code>

Then install app:

<code>helm install shopogolik ./helm-chart</code>

Make your ingress nginx accesible from outside the cluster.
From your terminal:

<code>kubectl port-forward -n ingress-nginx service/ingress-nginx-controller 8080:80</code>

Then edit your "hosts" file.

127.0.0.1 arch.homework

127.0.0.1 grafana.homework

Now you can check app in browser 

http://arch.homework:8080/api/v1/user/1

And check metrics from app

http://arch.homework:8080/metrics

Then open grafana with credential  admin:admin at http://grafana.homework:8080/

Go to the previously installed dashboard http://grafana.homework:8080/d/nginx/nginx-ingress-controller?orgId=1

Make some requests to app, for example http://arch.homework:8080/api/v1/user/1
then go to grafana and choose in right upper corner time period, 5min for example and set update period 5s in the same corner

If you want to access prometheus UI, you have to expose its port outside of clister
Open another terminal and paste command:

</code>kubectl port-forward -n monitoring service/prometheus-operated  9090</code>

Then go to http://127.0.0.1:9090/