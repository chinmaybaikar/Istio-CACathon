I have tried creating a custom script to install Istio on a cluster along with a demo application. 

## Usage:
$ python3 Istio-setup.py


## This will give you the following 2 self-explanatory options:

1) Install Istio and the demo application
2) Remove the demo application along with Istio and its addons


## As a part of the install, the following actions are executed:
- Dowload Istio v1.11.4
- Create istio-system and Istio pods
- Add the istio-injection=enabled label to default namespace since Istio reads this label to inject Envoy proxy
- Deploys the Google application from the microservices-demo repo
- Installs add-ons (Prometheus, Grafana, jaeger, and Kiali)
- Sets up port-forwarding to access the Kiali dashboard

## During the uninstall process, all these actions are reverted.
