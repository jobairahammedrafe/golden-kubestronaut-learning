# Minimize Microservice Vulnerabilities (20%)

This domain covers securing containerized applications and implementing Pod security.

## Pod Security Standards

### Pod Security Admission

```yaml
# Apply to namespace
apiVersion: v1
kind: Namespace
metadata:
  name: secure-ns
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### Security Levels

| Level | Description |
|-------|-------------|
| `privileged` | Unrestricted, allows all |
| `baseline` | Minimally restrictive, prevents known privilege escalations |
| `restricted` | Heavily restricted, follows security best practices |

### Restricted Pod Example

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: restricted-pod
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
    image: nginx
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
    volumeMounts:
    - name: tmp
      mountPath: /tmp
    - name: cache
      mountPath: /var/cache/nginx
    - name: run
      mountPath: /var/run
  volumes:
  - name: tmp
    emptyDir: {}
  - name: cache
    emptyDir: {}
  - name: run
    emptyDir: {}
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
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: nginx
```

### Container-level Security Context

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: container-secure
spec:
  containers:
  - name: app
    image: nginx
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
| `seccompProfile` | Pod/Container | seccomp profile |

## OPA Gatekeeper

### Install Gatekeeper

```bash
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml
```

### Constraint Template

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("Missing required labels: %v", [missing])
        }
```

### Constraint

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-team-label
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    labels: ["team"]
```

### Deny Privileged Containers

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8sdenyprivileged
spec:
  crd:
    spec:
      names:
        kind: K8sDenyPrivileged
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8sdenyprivileged

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          container.securityContext.privileged == true
          msg := sprintf("Privileged containers are not allowed: %v", [container.name])
        }
```

## Secrets Management

### Create Secrets

```bash
# From literal
kubectl create secret generic db-secret \
  --from-literal=username=admin \
  --from-literal=password=secret123

# From file
kubectl create secret generic tls-secret \
  --from-file=tls.crt \
  --from-file=tls.key
```

### Use Secrets as Environment Variables

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-env-pod
spec:
  containers:
  - name: app
    image: nginx
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: password
```

### Use Secrets as Volumes

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-vol-pod
spec:
  containers:
  - name: app
    image: nginx
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

### Encrypt Secrets at Rest

```yaml
# /etc/kubernetes/encryption-config.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: <base64-encoded-32-byte-key>
      - identity: {}
```

## Container Runtime Sandboxing

### gVisor (runsc)

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor
handler: runsc
---
apiVersion: v1
kind: Pod
metadata:
  name: sandboxed-pod
spec:
  runtimeClassName: gvisor
  containers:
  - name: app
    image: nginx
```

### Kata Containers

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: kata
handler: kata-qemu
---
apiVersion: v1
kind: Pod
metadata:
  name: kata-pod
spec:
  runtimeClassName: kata
  containers:
  - name: app
    image: nginx
```

## mTLS with Service Mesh

### Istio Strict mTLS

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
```

## Key Concepts to Remember

1. **Pod Security Standards** - privileged, baseline, restricted
2. **Security Context** - runAsNonRoot, readOnlyRootFilesystem, capabilities
3. **OPA Gatekeeper** - Policy enforcement
4. **Secrets** - Encrypt at rest, mount as volumes with restrictive permissions
5. **Runtime Sandboxing** - gVisor, Kata Containers

## Practice Questions

1. How do you enforce the restricted Pod Security Standard on a namespace?
2. What security context fields prevent privilege escalation?
3. How do you create an OPA Gatekeeper constraint?
4. What is the recommended way to mount secrets in pods?
5. How do you use a sandboxed runtime for a pod?

---

[← Previous: System Hardening](./03-system-hardening.md) | [Back to CKS Overview](./README.md) | [Next: Supply Chain Security →](./05-supply-chain-security.md)
