# Cluster Hardening (15%)

This domain covers hardening Kubernetes cluster components and implementing access controls.

## RBAC (Role-Based Access Control)

### Role (Namespace-scoped)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get"]
```

### ClusterRole (Cluster-scoped)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: secret-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "watch", "list"]
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list"]
```

### RoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
- kind: ServiceAccount
  name: default
  namespace: kube-system
- kind: Group
  name: developers
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### ClusterRoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: read-secrets-global
subjects:
- kind: Group
  name: managers
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

### RBAC Commands

```bash
# Create role
kubectl create role pod-reader --verb=get,list,watch --resource=pods -n default

# Create clusterrole
kubectl create clusterrole node-reader --verb=get,list --resource=nodes

# Create rolebinding
kubectl create rolebinding read-pods --role=pod-reader --user=jane -n default

# Create clusterrolebinding
kubectl create clusterrolebinding read-nodes --clusterrole=node-reader --group=developers

# Check permissions
kubectl auth can-i create pods --as jane
kubectl auth can-i list nodes --as jane
kubectl auth can-i --list --as jane
kubectl auth can-i --list --as system:serviceaccount:default:mysa
```

### Least Privilege Principle

```yaml
# Bad: Too permissive
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]

# Good: Specific permissions
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list"]
```

## ServiceAccount Security

### Create ServiceAccount

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-sa
  namespace: default
automountServiceAccountToken: false
```

### Disable Token Auto-mount

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  serviceAccountName: my-sa
  automountServiceAccountToken: false
  containers:
  - name: app
    image: nginx
```

### ServiceAccount Token Projection

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-projected-token
spec:
  serviceAccountName: my-sa
  containers:
  - name: app
    image: nginx
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
          audience: api
```

## Restrict API Access

### Disable Anonymous Authentication

```yaml
# /etc/kubernetes/manifests/kube-apiserver.yaml
spec:
  containers:
  - command:
    - kube-apiserver
    - --anonymous-auth=false
```

### Enable RBAC Authorization

```yaml
# /etc/kubernetes/manifests/kube-apiserver.yaml
spec:
  containers:
  - command:
    - kube-apiserver
    - --authorization-mode=Node,RBAC
```

### Restrict kubelet API

```yaml
# /var/lib/kubelet/config.yaml
authentication:
  anonymous:
    enabled: false
  webhook:
    enabled: true
authorization:
  mode: Webhook
```

## Upgrade Kubernetes

### Upgrade Control Plane

```bash
# Check available versions
apt-cache madison kubeadm

# Upgrade kubeadm
apt-mark unhold kubeadm
apt-get update && apt-get install -y kubeadm=1.30.0-1.1
apt-mark hold kubeadm

# Plan upgrade
kubeadm upgrade plan

# Apply upgrade
kubeadm upgrade apply v1.30.0

# Upgrade kubelet and kubectl
apt-mark unhold kubelet kubectl
apt-get update && apt-get install -y kubelet=1.30.0-1.1 kubectl=1.30.0-1.1
apt-mark hold kubelet kubectl

systemctl daemon-reload
systemctl restart kubelet
```

### Upgrade Worker Nodes

```bash
# Drain node
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# On worker node
apt-mark unhold kubeadm
apt-get update && apt-get install -y kubeadm=1.30.0-1.1
apt-mark hold kubeadm

kubeadm upgrade node

apt-mark unhold kubelet kubectl
apt-get update && apt-get install -y kubelet=1.30.0-1.1 kubectl=1.30.0-1.1
apt-mark hold kubelet kubectl

systemctl daemon-reload
systemctl restart kubelet

# Uncordon node
kubectl uncordon <node-name>
```

## Restrict Access to Kubernetes API

### API Server Flags

```yaml
# /etc/kubernetes/manifests/kube-apiserver.yaml
spec:
  containers:
  - command:
    - kube-apiserver
    - --anonymous-auth=false
    - --authorization-mode=Node,RBAC
    - --enable-admission-plugins=NodeRestriction
    - --insecure-port=0
    - --profiling=false
    - --audit-log-path=/var/log/kubernetes/audit/audit.log
```

### Network-level Restrictions

```yaml
# Restrict API server access with NetworkPolicy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: restrict-api-access
  namespace: kube-system
spec:
  podSelector:
    matchLabels:
      component: kube-apiserver
  policyTypes:
  - Ingress
  ingress:
  - from:
    - ipBlock:
        cidr: 10.0.0.0/8
```

## Admission Controllers

### Important Security Admission Controllers

| Controller | Description |
|------------|-------------|
| `NodeRestriction` | Limits kubelet permissions |
| `PodSecurity` | Enforces Pod Security Standards |
| `ImagePolicyWebhook` | External image validation |
| `ValidatingAdmissionWebhook` | Custom validation |
| `MutatingAdmissionWebhook` | Custom mutation |

### Enable Admission Controllers

```yaml
# /etc/kubernetes/manifests/kube-apiserver.yaml
spec:
  containers:
  - command:
    - kube-apiserver
    - --enable-admission-plugins=NodeRestriction,PodSecurity
```

## Key Concepts to Remember

1. **RBAC** - Role, ClusterRole, RoleBinding, ClusterRoleBinding
2. **Least Privilege** - Grant minimum required permissions
3. **ServiceAccount** - Disable auto-mount when not needed
4. **Anonymous Auth** - Disable on API server and kubelet
5. **Admission Controllers** - NodeRestriction, PodSecurity

## Practice Questions

1. How do you check if a user can perform an action?
2. What is the difference between Role and ClusterRole?
3. How do you disable ServiceAccount token auto-mount?
4. What admission controller restricts kubelet permissions?
5. How do you upgrade a Kubernetes cluster securely?

---

[← Previous: Cluster Setup](./01-cluster-setup.md) | [Back to CKS Overview](./README.md) | [Next: System Hardening →](./03-system-hardening.md)
