# Application Environment, Configuration and Security (25%)

This domain covers configuring applications, managing secrets, and implementing security in Kubernetes.

## ConfigMaps

### Creating ConfigMaps

```bash
# From literal values
kubectl create configmap app-config --from-literal=ENV=production --from-literal=LOG_LEVEL=info

# From file
kubectl create configmap app-config --from-file=config.properties

# From directory
kubectl create configmap app-config --from-file=config/

# From env file
kubectl create configmap app-config --from-env-file=app.env
```

### ConfigMap YAML

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  ENV: production
  LOG_LEVEL: info
  config.json: |
    {
      "database": "mysql",
      "port": 3306
    }
```

### Using ConfigMaps

**As Environment Variables:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
  - name: app
    image: myapp:v1
    env:
    - name: ENVIRONMENT
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: ENV
    envFrom:
    - configMapRef:
        name: app-config
```

**As Volume:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
  - name: app
    image: myapp:v1
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: app-config
      items:
      - key: config.json
        path: app-config.json
```

## Secrets

### Creating Secrets

```bash
# From literal values
kubectl create secret generic db-secret --from-literal=username=admin --from-literal=password=secret123

# From file
kubectl create secret generic tls-secret --from-file=tls.crt --from-file=tls.key

# Docker registry secret
kubectl create secret docker-registry regcred \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=user \
  --docker-password=pass \
  --docker-email=user@example.com

# TLS secret
kubectl create secret tls tls-secret --cert=tls.crt --key=tls.key
```

### Secret YAML

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  username: YWRtaW4=      # base64 encoded
  password: c2VjcmV0MTIz  # base64 encoded
---
# Using stringData (auto-encoded)
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
stringData:
  username: admin
  password: secret123
```

### Secret Types

| Type | Description |
|------|-------------|
| `Opaque` | Generic secret (default) |
| `kubernetes.io/dockerconfigjson` | Docker registry credentials |
| `kubernetes.io/tls` | TLS certificate and key |
| `kubernetes.io/basic-auth` | Basic authentication |
| `kubernetes.io/ssh-auth` | SSH authentication |

### Using Secrets

**As Environment Variables:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
  - name: app
    image: myapp:v1
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: password
    envFrom:
    - secretRef:
        name: db-secret
```

**As Volume:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
  - name: app
    image: myapp:v1
    volumeMounts:
    - name: secret-volume
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: db-secret
      defaultMode: 0400
```

## ServiceAccounts

### Creating ServiceAccounts

```bash
kubectl create serviceaccount my-sa
```

### ServiceAccount YAML

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-sa
automountServiceAccountToken: false
```

### Using ServiceAccounts

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  serviceAccountName: my-sa
  automountServiceAccountToken: true
  containers:
  - name: app
    image: myapp:v1
```

## Security Context

### Pod-level Security Context

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
    runAsNonRoot: true
  containers:
  - name: app
    image: myapp:v1
```

### Container-level Security Context

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  containers:
  - name: app
    image: myapp:v1
    securityContext:
      runAsUser: 1000
      runAsNonRoot: true
      readOnlyRootFilesystem: true
      allowPrivilegeEscalation: false
      capabilities:
        drop:
        - ALL
        add:
        - NET_BIND_SERVICE
```

### Security Context Fields

| Field | Level | Description |
|-------|-------|-------------|
| `runAsUser` | Pod/Container | UID to run as |
| `runAsGroup` | Pod/Container | GID to run as |
| `runAsNonRoot` | Pod/Container | Must run as non-root |
| `fsGroup` | Pod | Group for volumes |
| `readOnlyRootFilesystem` | Container | Read-only root FS |
| `allowPrivilegeEscalation` | Container | Prevent privilege escalation |
| `capabilities` | Container | Linux capabilities |

## Resource Requirements

### Requests and Limits

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
  - name: app
    image: myapp:v1
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

### CPU Units

| Value | Description |
|-------|-------------|
| `1` | 1 CPU core |
| `500m` | 0.5 CPU core (500 millicores) |
| `100m` | 0.1 CPU core |

### Memory Units

| Value | Description |
|-------|-------------|
| `128Mi` | 128 Mebibytes |
| `1Gi` | 1 Gibibyte |
| `256M` | 256 Megabytes |

### QoS Classes

| Class | Condition |
|-------|-----------|
| **Guaranteed** | requests = limits for all containers |
| **Burstable** | At least one request or limit set |
| **BestEffort** | No requests or limits set |

## LimitRange

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: resource-limits
spec:
  limits:
  - type: Container
    default:
      cpu: "500m"
      memory: "256Mi"
    defaultRequest:
      cpu: "100m"
      memory: "128Mi"
    max:
      cpu: "2"
      memory: "1Gi"
    min:
      cpu: "50m"
      memory: "64Mi"
```

## ResourceQuota

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
spec:
  hard:
    requests.cpu: "4"
    requests.memory: "8Gi"
    limits.cpu: "8"
    limits.memory: "16Gi"
    pods: "10"
    configmaps: "10"
    secrets: "10"
    persistentvolumeclaims: "5"
```

## Admission Controllers

### Pod Security Standards

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: secure-ns
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

| Level | Description |
|-------|-------------|
| `privileged` | Unrestricted |
| `baseline` | Minimally restrictive |
| `restricted` | Highly restrictive |

## Key Concepts to Remember

1. **ConfigMaps** - Non-sensitive configuration data
2. **Secrets** - Sensitive data (base64 encoded, not encrypted)
3. **SecurityContext** - Pod/container security settings
4. **Resources** - requests (scheduling) vs limits (enforcement)
5. **ServiceAccounts** - Identity for pods

## Practice Questions

1. How do you create a ConfigMap from a file?
2. What is the difference between `data` and `stringData` in Secrets?
3. How do you mount a Secret as a volume with specific permissions?
4. What QoS class is assigned when requests equal limits?
5. How do you prevent a container from running as root?

---

[← Previous: Application Observability and Maintenance](./03-application-observability-maintenance.md) | [Back to CKAD Overview](./README.md) | [Next: Services and Networking →](./05-services-networking.md)
