# GitOps Principles

Comprehensive guide to GitOps for CGOA certification.

---

## What is GitOps?

GitOps is a set of practices that uses Git as the single source of truth for declarative infrastructure and applications:

- **Declarative** - System state described declaratively
- **Versioned** - Desired state stored in Git
- **Automated** - Changes automatically applied
- **Auditable** - Git history provides audit trail

---

## Core Principles

### 1. Declarative Configuration

All system configuration is declarative:

```yaml
# Infrastructure as Code
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:v1.0.0
```

### 2. Version Controlled

- All configuration stored in Git
- Changes tracked through commits
- Pull requests for review
- Branches for environments

### 3. Automated Reconciliation

- Continuous sync between Git and cluster
- Drift detection and correction
- Self-healing infrastructure

### 4. Software Agents

- Operators watch Git repositories
- Pull changes automatically
- Apply to target systems

---

## GitOps Workflow

```
Developer → Git Commit → Pull Request → Merge → GitOps Agent → Kubernetes
                              ↓
                         Code Review
                              ↓
                         CI Pipeline
                              ↓
                         Image Build
```

---

## GitOps Tools

### Flux CD

```bash
# Install Flux
curl -s https://fluxcd.io/install.sh | sudo bash

# Bootstrap
flux bootstrap github \
  --owner=<github-user> \
  --repository=fleet-infra \
  --branch=main \
  --path=./clusters/my-cluster \
  --personal
```

### Argo CD

```bash
# Install Argo CD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

---

## Repository Structure

### Monorepo

```
fleet-infra/
├── apps/
│   ├── base/
│   │   └── myapp/
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       └── kustomization.yaml
│   ├── dev/
│   │   └── kustomization.yaml
│   ├── staging/
│   │   └── kustomization.yaml
│   └── production/
│       └── kustomization.yaml
├── infrastructure/
│   ├── controllers/
│   └── configs/
└── clusters/
    ├── dev/
    ├── staging/
    └── production/
```

### Multi-repo

```
# App repos
myapp-repo/
├── src/
├── Dockerfile
└── k8s/
    └── base/

# Config repo
gitops-config/
├── apps/
│   └── myapp/
└── clusters/
```

---

## Flux CD Resources

### GitRepository

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/myorg/myapp
  ref:
    branch: main
  secretRef:
    name: github-token
```

### Kustomization

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 10m
  targetNamespace: default
  sourceRef:
    kind: GitRepository
    name: myapp
  path: ./k8s/overlays/production
  prune: true
  healthChecks:
  - apiVersion: apps/v1
    kind: Deployment
    name: myapp
    namespace: default
```

### HelmRelease

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
  name: nginx
  namespace: default
spec:
  interval: 5m
  chart:
    spec:
      chart: nginx
      version: '15.x'
      sourceRef:
        kind: HelmRepository
        name: bitnami
        namespace: flux-system
  values:
    replicaCount: 2
```

---

## Best Practices

### 1. Environment Promotion

```
dev → staging → production

# Use branches or directories
main branch → dev cluster
release branch → staging cluster
tags → production cluster
```

### 2. Secrets Management

- Use Sealed Secrets or SOPS
- External secrets operators
- Never commit plain secrets

```yaml
# Sealed Secret
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: mysecret
spec:
  encryptedData:
    password: AgBy8hCi...
```

### 3. Image Automation

```yaml
apiVersion: image.toolkit.fluxcd.io/v1beta1
kind: ImagePolicy
metadata:
  name: myapp
spec:
  imageRepositoryRef:
    name: myapp
  policy:
    semver:
      range: '>=1.0.0'
```

### 4. Notifications

```yaml
apiVersion: notification.toolkit.fluxcd.io/v1beta1
kind: Alert
metadata:
  name: slack-alert
spec:
  providerRef:
    name: slack
  eventSeverity: error
  eventSources:
  - kind: Kustomization
    name: '*'
```

---

## GitOps vs Traditional CI/CD

| Aspect | Traditional CI/CD | GitOps |
|--------|------------------|--------|
| Deployment | Push-based | Pull-based |
| Source of Truth | CI/CD pipeline | Git repository |
| Drift Detection | Manual | Automatic |
| Rollback | Re-run pipeline | Git revert |
| Audit | CI/CD logs | Git history |

---

[← Back to CGOA Overview](./README.md)
