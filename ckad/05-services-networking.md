# Services and Networking (20%)

This domain covers Kubernetes networking concepts, Services, and Ingress.

## Services

### Service Types

| Type | Description |
|------|-------------|
| `ClusterIP` | Internal cluster IP (default) |
| `NodePort` | Exposes on each node's IP at a static port |
| `LoadBalancer` | External load balancer (cloud provider) |
| `ExternalName` | Maps to external DNS name |

### ClusterIP Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
```

### NodePort Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
    nodePort: 30080  # Optional: 30000-32767
```

### LoadBalancer Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
```

### ExternalName Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  type: ExternalName
  externalName: db.example.com
```

### Headless Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: headless-service
spec:
  clusterIP: None
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
```

### Creating Services Imperatively

```bash
# Expose deployment
kubectl expose deployment nginx --port=80 --target-port=8080 --type=ClusterIP

# Expose pod
kubectl expose pod nginx --port=80 --target-port=8080

# Create service without selector
kubectl create service clusterip my-svc --tcp=80:8080

# Generate YAML
kubectl expose deployment nginx --port=80 --dry-run=client -o yaml > svc.yaml
```

## DNS in Kubernetes

### Service DNS

```text
<service-name>.<namespace>.svc.cluster.local

Examples:
- my-service.default.svc.cluster.local
- my-service.default.svc
- my-service.default
- my-service (within same namespace)
```

### Pod DNS

```text
<pod-ip-dashed>.<namespace>.pod.cluster.local

Example:
- 10-244-0-5.default.pod.cluster.local
```

### DNS Resolution Example

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dns-test
spec:
  containers:
  - name: test
    image: busybox:1.36
    command: ['sleep', '3600']
---
# Test DNS
kubectl exec dns-test -- nslookup my-service
kubectl exec dns-test -- nslookup my-service.default.svc.cluster.local
```

## Network Policies

### Default Behavior

By default, all pods can communicate with all other pods.

### Deny All Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```

### Deny All Egress

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-egress
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Egress
```

### Allow Specific Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    - namespaceSelector:
        matchLabels:
          name: production
    ports:
    - protocol: TCP
      port: 8080
```

### Allow Egress to Specific Pods

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-db-egress
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
  - to:  # Allow DNS
    - namespaceSelector: {}
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
```

### Network Policy Selectors

| Selector | Description |
|----------|-------------|
| `podSelector` | Select pods by labels |
| `namespaceSelector` | Select namespaces by labels |
| `ipBlock` | Select by IP CIDR |

```yaml
# IP Block example
ingress:
- from:
  - ipBlock:
      cidr: 10.0.0.0/8
      except:
      - 10.0.1.0/24
```

## Ingress

### Ingress Resource

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

### Multiple Hosts

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: multi-host-ingress
spec:
  ingressClassName: nginx
  rules:
  - host: app1.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app1-service
            port:
              number: 80
  - host: app2.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app2-service
            port:
              number: 80
```

### Path-based Routing

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: path-ingress
spec:
  ingressClassName: nginx
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
      - path: /web
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

### TLS Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-ingress
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - myapp.example.com
    secretName: tls-secret
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

### Path Types

| Type | Description |
|------|-------------|
| `Exact` | Exact match of the URL path |
| `Prefix` | Matches based on URL path prefix |
| `ImplementationSpecific` | Depends on IngressClass |

### Creating Ingress Imperatively

```bash
# Create ingress
kubectl create ingress my-ingress \
  --rule="myapp.example.com/=myapp-service:80" \
  --class=nginx

# With TLS
kubectl create ingress my-ingress \
  --rule="myapp.example.com/=myapp-service:80,tls=tls-secret" \
  --class=nginx
```

## Port Forwarding

```bash
# Forward pod port
kubectl port-forward pod/nginx 8080:80

# Forward service port
kubectl port-forward svc/nginx 8080:80

# Forward deployment port
kubectl port-forward deployment/nginx 8080:80

# Listen on all interfaces
kubectl port-forward --address 0.0.0.0 pod/nginx 8080:80
```

## Key Concepts to Remember

1. **ClusterIP** - Default, internal only
2. **NodePort** - External access via node IP:port
3. **LoadBalancer** - Cloud provider load balancer
4. **Network Policies** - Default allow, explicit deny
5. **Ingress** - HTTP/HTTPS routing, requires controller

## Practice Questions

1. What is the default Service type in Kubernetes?
2. How do you create a Service that exposes a deployment on port 80?
3. What happens to traffic if no Network Policy exists?
4. How do you route traffic based on URL path using Ingress?
5. What is the DNS name format for a Service?

---

[← Previous: Application Environment, Configuration and Security](./04-application-environment-config-security.md) | [Back to CKAD Overview](./README.md) | [Next: Sample Practice Questions →](./sample-questions.md)
