# Kyverno Fundamentals

Comprehensive guide to Kyverno policy engine for KCA certification.

---

## Overview

Kyverno is a Kubernetes-native policy engine that can:

- **Validate** - Ensure resources meet requirements
- **Mutate** - Modify resources automatically
- **Generate** - Create additional resources
- **Verify Images** - Check image signatures

---

## Installation

```bash
# Using kubectl
kubectl create -f https://github.com/kyverno/kyverno/releases/download/v1.10.0/install.yaml

# Using Helm
helm repo add kyverno https://kyverno.github.io/kyverno/
helm install kyverno kyverno/kyverno -n kyverno --create-namespace

# Verify
kubectl get pods -n kyverno
```

---

## Policy Structure

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: policy-name
spec:
  validationFailureAction: Enforce  # or Audit
  background: true
  rules:
  - name: rule-name
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Error message"
      pattern:
        spec:
          containers:
          - name: "*"
            resources:
              limits:
                memory: "?*"
```

---

## Validation Policies

### Require Labels

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-labels
spec:
  validationFailureAction: Enforce
  rules:
  - name: check-team-label
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Label 'team' is required"
      pattern:
        metadata:
          labels:
            team: "?*"
```

### Require Resource Limits

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-limits
spec:
  validationFailureAction: Enforce
  rules:
  - name: validate-resources
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "CPU and memory limits are required"
      pattern:
        spec:
          containers:
          - resources:
              limits:
                memory: "?*"
                cpu: "?*"
```

### Disallow Privileged Containers

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-privileged
spec:
  validationFailureAction: Enforce
  rules:
  - name: deny-privileged
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Privileged containers are not allowed"
      pattern:
        spec:
          containers:
          - securityContext:
              privileged: "!true"
```

---

## Mutation Policies

### Add Default Labels

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-labels
spec:
  rules:
  - name: add-default-labels
    match:
      any:
      - resources:
          kinds:
          - Pod
    mutate:
      patchStrategicMerge:
        metadata:
          labels:
            app.kubernetes.io/managed-by: kyverno
```

### Add Resource Defaults

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-resources
spec:
  rules:
  - name: add-default-requests
    match:
      any:
      - resources:
          kinds:
          - Pod
    mutate:
      patchStrategicMerge:
        spec:
          containers:
          - (name): "*"
            resources:
              requests:
                memory: "64Mi"
                cpu: "100m"
```

### Add Sidecar

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-sidecar
spec:
  rules:
  - name: inject-sidecar
    match:
      any:
      - resources:
          kinds:
          - Deployment
          selector:
            matchLabels:
              inject-sidecar: "true"
    mutate:
      patchStrategicMerge:
        spec:
          template:
            spec:
              containers:
              - name: sidecar
                image: busybox
                command: ['sh', '-c', 'sleep infinity']
```

---

## Generate Policies

### Generate NetworkPolicy

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: generate-netpol
spec:
  rules:
  - name: generate-default-deny
    match:
      any:
      - resources:
          kinds:
          - Namespace
    generate:
      apiVersion: networking.k8s.io/v1
      kind: NetworkPolicy
      name: default-deny
      namespace: "{{request.object.metadata.name}}"
      data:
        spec:
          podSelector: {}
          policyTypes:
          - Ingress
          - Egress
```

### Generate ResourceQuota

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: generate-quota
spec:
  rules:
  - name: generate-resourcequota
    match:
      any:
      - resources:
          kinds:
          - Namespace
    generate:
      apiVersion: v1
      kind: ResourceQuota
      name: default-quota
      namespace: "{{request.object.metadata.name}}"
      data:
        spec:
          hard:
            pods: "10"
            requests.cpu: "4"
            requests.memory: "8Gi"
```

---

## Image Verification

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-images
spec:
  validationFailureAction: Enforce
  rules:
  - name: verify-signature
    match:
      any:
      - resources:
          kinds:
          - Pod
    verifyImages:
    - imageReferences:
      - "myregistry.io/*"
      attestors:
      - entries:
        - keys:
            publicKeys: |-
              -----BEGIN PUBLIC KEY-----
              ...
              -----END PUBLIC KEY-----
```

---

## Policy Reports

```bash
# View policy reports
kubectl get policyreport -A
kubectl get clusterpolicyreport

# Describe report
kubectl describe policyreport -n default
```

---

## Useful Commands

```bash
# List policies
kubectl get clusterpolicy
kubectl get policy -A

# Test policy
kubectl apply -f policy.yaml --dry-run=server

# View policy details
kubectl describe clusterpolicy require-labels

# Check admission controller
kubectl get validatingwebhookconfiguration
kubectl get mutatingwebhookconfiguration
```

---

[← Back to KCA Overview](./README.md)
