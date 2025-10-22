```bash
k3d cluster create --api-port 6550 -p '9080:80@loadbalancer' -p '9443:443@loadbalancer' --agents 2 --k3s-arg '--disable=traefik@server:*'

k3d cluster list
kubectl config get-contexts

istioctl version
istioctl install -f ./bookinfo/demo-profile-no-gateways.yaml -y
kubectl label namespace default istio-injection=enabled

# install GW API CRDs
kubectl get crd gateways.gateway.networking.k8s.io &> /dev/null || \
{ kubectl kustomize "github.com/kubernetes-sigs/gateway-api/config/crd?ref=v1.3.0" | kubectl apply -f -; }

# deploy
kubectl apply -f ./bookinfo/platform/kube/bookinfo.yaml

kubectl get services
kubectl get pods

kubectl exec "$(kubectl get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}')" -c ratings -- curl -sS productpage:9080/productpage | grep -o "<title>.*</title>"
# <title>Simple Bookstore App</title>
```

