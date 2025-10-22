```bash
k3d cluster create --api-port 6550 -p '9080:80@loadbalancer' -p '9443:443@loadbalancer' --agents 2 --k3s-arg '--disable=traefik@server:*'

k3d cluster list
kubectl config get-contexts

istioctl version

# install sidecars
istioctl install -f ./bookinfo/demo-profile-no-gateways.yaml -y
kubectl label namespace default istio-injection=enabled

# install GW API CRDs
kubectl get crd gateways.gateway.networking.k8s.io &> /dev/null || \
{ kubectl kustomize "github.com/kubernetes-sigs/gateway-api/config/crd?ref=v1.3.0" | kubectl apply -f -; }

# deploy
kubectl apply -f ./bookinfo/platform/kube/bookinfo.yaml

kubectl get services
kubectl get pods

# kubectl rollout restart deployment details-v1
# kubectl rollout restart deployment productpage-v1
# kubectl rollout restart deployment ratings-v1
# kubectl rollout restart deployment reviews-v1
# kubectl rollout restart deployment reviews-v2
# kubectl rollout restart deployment reviews-v3

# wait until
# NAME                              READY   STATUS    RESTARTS   AGE
# details-v1-77b775f46-v8jwh        2/2     Running   0          4m56s
# productpage-v1-78dfd4688c-kjjfh   2/2     Running   0          4m55s
# ratings-v1-7c4c8d6794-zvrkq       2/2     Running   0          4m56s
# reviews-v1-849f9bc5d6-vdl64       2/2     Running   0          4m56s
# reviews-v2-5c757d5846-kk4jl       2/2     Running   0          4m56s
# reviews-v3-6d5d98f5c4-h5jjj       2/2     Running   0          4m56s

kubectl exec "$(kubectl get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}')" -c ratings -- curl -sS productpage:9080/productpage | grep -o "<title>.*</title>"
# <title>Simple Bookstore App</title>
```
## Open app to outside traffic
```bash
kubectl apply -f ./bookinfo/gateway-api/bookinfo-gateway.yaml

# change the service type to ClusterIP by annotating the gateway
kubectl annotate gateway bookinfo-gateway networking.istio.io/service-type=ClusterIP --namespace=default

# check status
kubectl get gateway

kubectl port-forward svc/bookinfo-gateway-istio 8080:80
# http://localhost:8080/productpage
```

## Dashboard
```bash
kubectl apply -f ./addons
kubectl rollout status deployment/kiali -n istio-system

istioctl dashboard kiali

# send requests to the app
./send_req.sh

```
