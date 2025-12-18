# Kubernetes Security Fundamentals (22%)

This domain covers core Kubernetes security features and configurations.

## Pod Security

### Security Context

Define security settings at the Pod or container level:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: nginx:1.21
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
          - ALL
```

### Security Context Fields

| Field | Level | Description |
|-------|-------|-------------|
| `runAsUser` | Pod/Container | UID to run as |
| `runAsGroup` | Pod/Container | GID to run as |
| `runAsNonRoot` | Pod/Container | Must run as non-root |
| `fsGroup` | Pod | Group for volumes |
| `allowPrivilegeEscalation` | Container | Prevent privilege escalation |
| `readOnlyRootFilesystem` | Container | Read-only root filesystem |
| `capabilities` | Container | Linux capabilities |
| `seccompProfile` | Pod/Container | Seccomp profile |
| `seLinuxOptions` | Pod/Container | SELinux context |

### Pod Security Standards

Three policy levels:

| Level | Description |
|-------|-------------|
| **Privileged** | Unrestricted, allows known privilege escalations |
| **Baseline** | Minimally restrictive, prevents known privilege escalations |
| **Restricted** | Heavily restricted, follows security best practices |

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
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
    ports:
    - protocol: TCP
      port: 8080
```

### Egress Policy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns-only
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: restricted
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: kube-system
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
| `ipBlock` | Select by IP CIDR range |

## RBAC Deep Dive

### Role vs ClusterRole

| Type | Scope | Use Case |
|------|-------|----------|
| **Role** | Namespace | Namespace-specific permissions |
| **ClusterRole** | Cluster-wide | Cluster resources or aggregation |

### RoleBinding vs ClusterRoleBinding

| Type | Scope | Can Reference |
|------|-------|---------------|
| **RoleBinding** | Namespace | Role or ClusterRole |
| **ClusterRoleBinding** | Cluster-wide | ClusterRole only |

### RBAC Best Practices

```yaml
# Least privilege Role example
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: app-namespace
  name: app-deployer
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "create", "update", "patch"]
  resourceNames: ["my-app"]  # Specific resource
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]
```

### Checking Permissions

```bash
# Check if you can perform an action
kubectl auth can-i create pods
kubectl auth can-i create pods --as=system:serviceaccount:default:my-sa
kubectl auth can-i --list --namespace=default
```

## Service Accounts

### Default Service Account

Every namespace has a default service account.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-service-account
  namespace: default
automountServiceAccountToken: false
```

### Using Service Accounts

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  serviceAccountName: my-service-account
  automountServiceAccountToken: false  # Disable if not needed
  containers:
  - name: app
    image: my-app:v1
```

### Token Projection

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-projected-token
spec:
  containers:
  - name: app
    image: my-app:v1
    volumeMounts:
    - name: token
      mountPath: /var/run/secrets/tokens
  volumes:
  - name: token
    projected:
      sources:
      - serviceAccountToken:
          path: token
          expirationSeconds: 3600
          audience: my-audience
```

## Resource Quotas and Limits

### LimitRange

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: resource-limits
  namespace: default
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

### ResourceQuota

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: default
spec:
  hard:
    requests.cpu: "4"
    requests.memory: "8Gi"
    limits.cpu: "8"
    limits.memory: "16Gi"
    pods: "10"
    secrets: "10"
    configmaps: "10"
```

## Image Security

### Image Pull Policies

| Policy | Behavior |
|--------|----------|
| `Always` | Always pull image |
| `IfNotPresent` | Pull only if not cached |
| `Never` | Never pull, use cached only |

### Private Registry Authentication

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: regcred
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64-encoded-docker-config>
---
apiVersion: v1
kind: Pod
metadata:
  name: private-pod
spec:
  containers:
  - name: app
    image: private-registry.io/my-app:v1
  imagePullSecrets:
  - name: regcred
```

### Image Digest

Use image digests for immutability:

```yaml
spec:
  containers:
  - name: app
    image: nginx@sha256:abc123...
```

## Key Concepts to Remember

1. **Security contexts** - Define at Pod and container level
2. **Pod Security Standards** - Privileged, Baseline, Restricted
3. **Network Policies** - Default allow, explicit deny
4. **RBAC** - Roles, ClusterRoles, Bindings
5. **Service Accounts** - Disable auto-mount when not needed

## Practice Questions

1. What is the difference between `runAsUser` and `runAsNonRoot`?
2. What happens if no Network Policy exists in a namespace?
3. Can a RoleBinding reference a ClusterRole?
4. How do you prevent a container from escalating privileges?
5. What are the three Pod Security Standards levels?

---

[← Previous: Cluster Component Security](./02-cluster-component-security.md) | [Back to KCSA Overview](./README.md) | [Next: Kubernetes Threat Model →](./04-kubernetes-threat-model.md)
