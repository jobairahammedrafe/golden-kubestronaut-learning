# Application Deployment (20%)

<div class="pdf-download">
  <a href="/pdf/02-application-deployment.pdf" class="md-button md-button--primary" download>
    <span class="twemoji">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M5 20h14v-2H5v2zM19 9h-4V3H9v6H5l7 7 7-7z"></path></svg>
    </span>
    Download PDF Version
  </a>
</div>



This domain covers deploying applications in Kubernetes using various strategies and tools.

## Deployments

### Creating Deployments

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```

### Imperative Commands

```bash
# Create deployment
kubectl create deployment nginx --image=nginx:1.21 --replicas=3

# Scale deployment
kubectl scale deployment nginx --replicas=5

# Update image
kubectl set image deployment/nginx nginx=nginx:1.22

# Edit deployment
kubectl edit deployment nginx
```

## Deployment Strategies

### Rolling Update (Default)

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
```

| Parameter | Description |
|-----------|-------------|
| `maxSurge` | Max pods above desired count during update |
| `maxUnavailable` | Max pods unavailable during update |

### Recreate

```yaml
spec:
  strategy:
    type: Recreate
```

All existing pods are killed before new ones are created.

## Rollouts

### Rollout Commands

```bash
# Check rollout status
kubectl rollout status deployment/nginx

# View rollout history
kubectl rollout history deployment/nginx

# View specific revision
kubectl rollout history deployment/nginx --revision=2

# Undo rollout (rollback)
kubectl rollout undo deployment/nginx

# Rollback to specific revision
kubectl rollout undo deployment/nginx --to-revision=2

# Pause rollout
kubectl rollout pause deployment/nginx

# Resume rollout
kubectl rollout resume deployment/nginx

# Restart deployment
kubectl rollout restart deployment/nginx
```

### Recording Changes

```bash
# Record the command in revision history
kubectl set image deployment/nginx nginx=nginx:1.22 --record
```

## Blue-Green Deployment

Manual blue-green deployment using Services:

```yaml
# Blue deployment (current)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: app
        image: myapp:v1
---
# Green deployment (new)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: app
        image: myapp:v2
---
# Service - switch selector to change versions
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
    version: blue  # Change to 'green' to switch
  ports:
  - port: 80
    targetPort: 8080
```

## Canary Deployment

```yaml
# Stable deployment (90% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:v1
---
# Canary deployment (10% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:v2
---
# Service routes to both (based on replica ratio)
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp  # Matches both deployments
  ports:
  - port: 80
    targetPort: 8080
```

## Helm

### Helm Basics

```bash
# Add repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Search charts
helm search repo nginx
helm search hub wordpress

# Install chart
helm install my-nginx bitnami/nginx

# Install with custom values
helm install my-nginx bitnami/nginx -f values.yaml
helm install my-nginx bitnami/nginx --set service.type=NodePort

# List releases
helm list
helm list -A  # All namespaces

# Upgrade release
helm upgrade my-nginx bitnami/nginx --set replicaCount=3

# Rollback
helm rollback my-nginx 1

# Uninstall
helm uninstall my-nginx

# Show chart info
helm show values bitnami/nginx
helm show chart bitnami/nginx
```

### Helm Chart Structure

```text
mychart/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default configuration values
├── charts/             # Chart dependencies
├── templates/          # Template files
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── _helpers.tpl    # Template helpers
│   └── NOTES.txt       # Post-install notes
└── .helmignore         # Files to ignore
```

### Chart.yaml

```yaml
apiVersion: v2
name: mychart
description: A Helm chart for my application
type: application
version: 0.1.0
appVersion: "1.0.0"
```

### values.yaml

```yaml
replicaCount: 3

image:
  repository: nginx
  tag: "1.21"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 100m
    memory: 128Mi
```

### Template Example

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-deployment
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app: {{ .Release.Name }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        ports:
        - containerPort: 80
```

## Kustomize

### Kustomize Structure

```text
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
└── overlays/
    ├── dev/
    │   └── kustomization.yaml
    └── prod/
        └── kustomization.yaml
```

### Base kustomization.yaml

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
```

### Overlay kustomization.yaml

```yaml
# overlays/prod/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base

namePrefix: prod-

replicas:
  - name: myapp
    count: 5

images:
  - name: myapp
    newTag: v2.0.0

patches:
  - patch: |-
      - op: replace
        path: /spec/template/spec/containers/0/resources/limits/memory
        value: 512Mi
    target:
      kind: Deployment
      name: myapp
```

### Kustomize Commands

```bash
# Preview output
kubectl kustomize overlays/prod/

# Apply
kubectl apply -k overlays/prod/

# Delete
kubectl delete -k overlays/prod/
```

## Key Concepts to Remember

1. **Rolling Update** - Default strategy, gradual replacement
2. **Recreate** - Kill all, then create new
3. **Rollout commands** - status, history, undo, pause, resume
4. **Helm** - Package manager for Kubernetes
5. **Kustomize** - Template-free configuration customization

## Practice Questions

1. How do you rollback a deployment to revision 3?
2. What is the difference between maxSurge and maxUnavailable?
3. How do you install a Helm chart with custom values?
4. What command shows the rollout history of a deployment?
5. How do you apply a Kustomize overlay?

---

[← Previous: Application Design and Build](./01-application-design-build.md) | [Back to CKAD Overview](./README.md) | [Next: Application Observability and Maintenance →](./03-application-observability-maintenance.md)
