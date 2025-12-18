# Kubernetes Cluster Component Security (22%)

This domain covers securing the core components of a Kubernetes cluster.

## Control Plane Security

### API Server Security

The API Server is the front door to your cluster:

```text
┌─────────────────────────────────────────────────────┐
│                    API Server                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │Authentication│→│Authorization│→│  Admission  │  │
│  │             │  │             │  │  Control    │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────┘
```

**Security configurations:**

- Enable TLS for all communications
- Use strong authentication methods
- Configure appropriate authorization modes
- Enable audit logging
- Restrict anonymous access

```yaml
# API Server security flags
--anonymous-auth=false
--authorization-mode=Node,RBAC
--enable-admission-plugins=NodeRestriction,PodSecurity
--audit-log-path=/var/log/kubernetes/audit.log
--tls-cert-file=/etc/kubernetes/pki/apiserver.crt
--tls-private-key-file=/etc/kubernetes/pki/apiserver.key
```

### etcd Security

etcd stores all cluster state and secrets:

**Best practices:**

- Enable TLS for client and peer communication
- Encrypt data at rest
- Restrict access to etcd
- Regular backups with encryption
- Run etcd on dedicated nodes

```yaml
# etcd security configuration
--cert-file=/etc/kubernetes/pki/etcd/server.crt
--key-file=/etc/kubernetes/pki/etcd/server.key
--client-cert-auth=true
--trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
--peer-cert-file=/etc/kubernetes/pki/etcd/peer.crt
--peer-key-file=/etc/kubernetes/pki/etcd/peer.key
```

### Controller Manager Security

**Security configurations:**

- Use service account credentials
- Enable TLS
- Rotate service account tokens

### Scheduler Security

**Security configurations:**

- Enable TLS
- Use secure binding address
- Configure authentication

## Node Security

### Kubelet Security

The kubelet runs on every node:

```yaml
# Kubelet security configuration
--anonymous-auth=false
--authorization-mode=Webhook
--client-ca-file=/etc/kubernetes/pki/ca.crt
--tls-cert-file=/etc/kubernetes/pki/kubelet.crt
--tls-private-key-file=/etc/kubernetes/pki/kubelet.key
--rotate-certificates=true
--protect-kernel-defaults=true
--read-only-port=0
```

**Key security settings:**

| Setting | Recommended Value | Purpose |
|---------|------------------|---------|
| `--anonymous-auth` | false | Disable anonymous access |
| `--authorization-mode` | Webhook | Use API server for authorization |
| `--read-only-port` | 0 | Disable read-only port |
| `--protect-kernel-defaults` | true | Protect kernel settings |

### Container Runtime Security

**containerd security:**

- Use seccomp profiles
- Enable AppArmor/SELinux
- Configure runtime class

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: secure-runtime
handler: runsc  # gVisor
```

### Node Hardening

**OS-level security:**

- Minimize installed packages
- Apply security patches regularly
- Configure firewall rules
- Enable audit logging
- Use immutable infrastructure

## Authentication Methods

### X.509 Client Certificates

```bash
# Generate client certificate
openssl genrsa -out user.key 2048
openssl req -new -key user.key -out user.csr -subj "/CN=user/O=group"
# Sign with cluster CA
```

### Service Account Tokens

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-service-account
automountServiceAccountToken: false  # Disable auto-mount
```

### OpenID Connect (OIDC)

```yaml
# API Server OIDC configuration
--oidc-issuer-url=https://accounts.google.com
--oidc-client-id=my-client-id
--oidc-username-claim=email
--oidc-groups-claim=groups
```

### Webhook Token Authentication

External authentication service integration.

## Authorization Modes

### Node Authorization

Authorizes API requests made by kubelets.

### RBAC (Role-Based Access Control)

Most commonly used authorization mode:

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
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### ABAC (Attribute-Based Access Control)

Policy file-based authorization (less common).

### Webhook Authorization

External authorization service.

## Admission Controllers

### Built-in Admission Controllers

| Controller | Purpose |
|------------|---------|
| **PodSecurity** | Enforce Pod Security Standards |
| **NodeRestriction** | Limit kubelet permissions |
| **ResourceQuota** | Enforce resource limits |
| **LimitRanger** | Set default resource limits |
| **ServiceAccount** | Automate service account management |

### Validating vs Mutating

```text
Request → Mutating Webhooks → Validating Webhooks → etcd
              (modify)            (accept/reject)
```

### Pod Security Admission

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: secure-namespace
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

## Secrets Management

### Kubernetes Secrets

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  password: cGFzc3dvcmQ=  # base64 encoded
```

**Security considerations:**

- Secrets are base64 encoded, NOT encrypted by default
- Enable encryption at rest
- Use RBAC to restrict access
- Consider external secret managers

### Encryption at Rest

```yaml
# EncryptionConfiguration
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: <base64-encoded-key>
      - identity: {}
```

### External Secret Managers

- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault
- Google Secret Manager

## Key Concepts to Remember

1. **API Server is the gateway** - Secure it thoroughly
2. **etcd contains all secrets** - Encrypt and restrict access
3. **Kubelet security is critical** - Disable anonymous auth
4. **RBAC is the standard** - Use least privilege
5. **Admission controllers** - Last line of defense

## Practice Questions

1. What are the three stages of API request processing?
2. Why should anonymous authentication be disabled on the kubelet?
3. What is the difference between a Role and a ClusterRole?
4. How are Kubernetes Secrets stored by default?
5. What does the NodeRestriction admission controller do?

---

[← Previous: Cloud Native Security Overview](./01-cloud-native-security-overview.md) | [Back to KCSA Overview](./README.md) | [Next: Kubernetes Security Fundamentals →](./03-kubernetes-security-fundamentals.md)
