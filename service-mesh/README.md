```bash
k3d cluster create --api-port 6550 -p '9080:80@loadbalancer' -p '9443:443@loadbalancer' --agents 2 --k3s-arg '--disable=traefik@server:*'

k3d cluster list
kubectl config get-contexts

istioctl version
istioctl install -f ./bookinfo/demo-profile-no-gateways.yaml -y
```

