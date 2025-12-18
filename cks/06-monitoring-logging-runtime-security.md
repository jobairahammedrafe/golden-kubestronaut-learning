# Monitoring, Logging and Runtime Security (20%)

This domain covers runtime security monitoring, audit logging, and threat detection.

## Falco

### Install Falco

```bash
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm install falco falcosecurity/falco --namespace falco --create-namespace
```

### Falco Rules Example

```yaml
- rule: Terminal shell in container
  desc: A shell was spawned in a container
  condition: spawned_process and container and shell_procs
  output: Shell spawned (user=%user.name container=%container.name)
  priority: WARNING

- rule: Write below etc
  desc: Write to /etc directory
  condition: write and container and fd.directory = /etc
  output: File written to /etc (container=%container.name)
  priority: ERROR
```

### Falco Commands

```bash
systemctl status falco
kubectl logs -n falco -l app.kubernetes.io/name=falco
```

## Kubernetes Audit Logging

### Audit Policy

```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
  - level: None
    nonResourceURLs: ["/healthz*", "/version"]
  - level: Metadata
    resources:
      - group: ""
        resources: ["secrets"]
  - level: RequestResponse
    resources:
      - group: ""
        resources: ["pods/exec", "pods/attach"]
  - level: Metadata
```

### Enable Audit Logging

```yaml
# kube-apiserver flags
- --audit-policy-file=/etc/kubernetes/audit-policy.yaml
- --audit-log-path=/var/log/kubernetes/audit/audit.log
- --audit-log-maxage=30
- --audit-log-maxsize=100
```

### Analyze Audit Logs

```bash
cat /var/log/kubernetes/audit/audit.log | jq .
cat /var/log/kubernetes/audit/audit.log | jq 'select(.verb=="delete")'
cat /var/log/kubernetes/audit/audit.log | jq 'select(.objectRef.resource=="secrets")'
```

## Container Immutability

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: immutable-pod
spec:
  containers:
  - name: app
    image: nginx:1.21
    securityContext:
      readOnlyRootFilesystem: true
      allowPrivilegeEscalation: false
    volumeMounts:
    - name: tmp
      mountPath: /tmp
  volumes:
  - name: tmp
    emptyDir: {}
```

## Key Concepts

1. **Falco** - Runtime threat detection
2. **Audit Logging** - Track API server activity
3. **Immutability** - Read-only root filesystem
4. **Audit Levels** - None, Metadata, Request, RequestResponse

---

[← Previous: Supply Chain Security](./05-supply-chain-security.md) | [Back to CKS Overview](./README.md) | [Next: Sample Questions →](./sample-questions.md)
