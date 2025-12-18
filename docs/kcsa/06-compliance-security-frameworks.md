# Compliance and Security Frameworks (10%)

This domain covers compliance requirements and security frameworks relevant to Kubernetes environments.

## Compliance Frameworks

### CIS Kubernetes Benchmark

The Center for Internet Security (CIS) provides security benchmarks for Kubernetes:

| Section | Focus Area |
|---------|------------|
| **1** | Control Plane Components |
| **2** | etcd |
| **3** | Control Plane Configuration |
| **4** | Worker Nodes |
| **5** | Policies |

#### Running CIS Benchmarks

```bash
# Using kube-bench
kube-bench run --targets master
kube-bench run --targets node
kube-bench run --targets etcd

# Output specific checks
kube-bench run --targets master --check 1.1.1,1.1.2
```

#### Example CIS Controls

| Control | Description | Remediation |
|---------|-------------|-------------|
| 1.1.1 | API server pod spec permissions | chmod 644 /etc/kubernetes/manifests/kube-apiserver.yaml |
| 1.2.1 | Anonymous auth disabled | --anonymous-auth=false |
| 4.2.1 | Kubelet anonymous auth | --anonymous-auth=false |
| 5.1.1 | RBAC enabled | --authorization-mode=RBAC |

### NIST Cybersecurity Framework

Five core functions:

```text
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│Identify │→ │ Protect │→ │ Detect  │→ │ Respond │→ │ Recover │
└─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘
```

| Function | Kubernetes Application |
|----------|----------------------|
| **Identify** | Asset inventory, risk assessment |
| **Protect** | RBAC, Network Policies, Pod Security |
| **Detect** | Audit logging, runtime security |
| **Respond** | Incident response procedures |
| **Recover** | Backup/restore, disaster recovery |

### SOC 2

Service Organization Control 2 - Trust Service Criteria:

| Criteria | Kubernetes Relevance |
|----------|---------------------|
| **Security** | Access controls, encryption |
| **Availability** | High availability, disaster recovery |
| **Processing Integrity** | Data validation, error handling |
| **Confidentiality** | Secrets management, encryption |
| **Privacy** | Data handling, retention |

### PCI DSS

Payment Card Industry Data Security Standard:

| Requirement | Kubernetes Implementation |
|-------------|--------------------------|
| **Req 1** | Network segmentation (Network Policies) |
| **Req 2** | Secure configurations (CIS benchmarks) |
| **Req 3** | Protect stored data (Encryption at rest) |
| **Req 4** | Encrypt transmission (TLS/mTLS) |
| **Req 7** | Restrict access (RBAC) |
| **Req 10** | Track and monitor (Audit logging) |

### HIPAA

Health Insurance Portability and Accountability Act:

- **Access controls** - RBAC, authentication
- **Audit controls** - Logging, monitoring
- **Integrity controls** - Image signing, admission control
- **Transmission security** - TLS encryption

## Security Standards

### Pod Security Standards

Kubernetes native security standards:

```yaml
# Namespace labels for Pod Security Standards
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    # Enforce restricted standard
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: v1.28
    # Audit baseline violations
    pod-security.kubernetes.io/audit: baseline
    # Warn on privileged violations
    pod-security.kubernetes.io/warn: privileged
```

### NSA/CISA Kubernetes Hardening Guide

Key recommendations:

1. **Scan containers and pods** for vulnerabilities
2. **Run containers as non-root** users
3. **Use immutable container filesystems**
4. **Scan container images** for misconfigurations
5. **Use Pod Security Standards**
6. **Harden all authentication and authorization**
7. **Use network policies** to isolate resources
8. **Encrypt data** in transit and at rest
9. **Enable audit logging**
10. **Restrict access to control plane**

## Audit and Compliance Tools

### Policy Enforcement

#### OPA Gatekeeper

```yaml
# Constraint Template
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

#### Kyverno

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-labels
spec:
  validationFailureAction: Enforce
  rules:
  - name: check-for-labels
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "The label 'app' is required."
      pattern:
        metadata:
          labels:
            app: "?*"
```

### Compliance Scanning

| Tool | Purpose |
|------|---------|
| **kube-bench** | CIS benchmark scanning |
| **Trivy** | Vulnerability and misconfiguration scanning |
| **Polaris** | Best practices validation |
| **Kubescape** | NSA/CISA compliance scanning |
| **Checkov** | Infrastructure as code scanning |

### Continuous Compliance

```text
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Commit    │ ──► │   Scan      │ ──► │   Report    │
│   Code      │     │   Pipeline  │     │   Results   │
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                          ▼
                    ┌─────────────┐
                    │   Block if  │
                    │   Non-      │
                    │   Compliant │
                    └─────────────┘
```

## Documentation and Evidence

### Security Documentation

Required documentation for compliance:

- Security policies and procedures
- Network diagrams
- Access control matrices
- Incident response plans
- Change management procedures
- Audit logs and reports

### Evidence Collection

```bash
# Collect cluster configuration
kubectl get nodes -o yaml > nodes.yaml
kubectl get namespaces -o yaml > namespaces.yaml
kubectl get networkpolicies -A -o yaml > networkpolicies.yaml
kubectl get roles,rolebindings -A -o yaml > rbac.yaml

# Export audit logs
kubectl logs -n kube-system kube-apiserver-* > audit.log
```

### Compliance Reporting

| Report Type | Frequency | Content |
|-------------|-----------|---------|
| **Vulnerability** | Daily/Weekly | CVE findings |
| **Configuration** | Weekly | CIS benchmark results |
| **Access Review** | Monthly | RBAC audit |
| **Incident** | As needed | Security incidents |
| **Compliance** | Quarterly | Framework compliance status |

## Risk Management

### Risk Assessment

| Risk Category | Examples | Mitigation |
|---------------|----------|------------|
| **Technical** | Vulnerabilities, misconfigurations | Scanning, hardening |
| **Operational** | Human error, process failures | Training, automation |
| **Compliance** | Regulatory violations | Policies, audits |
| **Business** | Service disruption | HA, DR planning |

### Risk Prioritization

```text
                    High Impact
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         │   Critical    │    High       │
         │   Priority    │   Priority    │
         │               │               │
Low ─────┼───────────────┼───────────────┼───── High
Likelihood               │               Likelihood
         │               │               │
         │     Low       │   Medium      │
         │   Priority    │   Priority    │
         │               │               │
         └───────────────┼───────────────┘
                         │
                    Low Impact
```

## Key Concepts to Remember

1. **CIS Benchmarks** - Industry standard for Kubernetes security
2. **NIST Framework** - Identify, Protect, Detect, Respond, Recover
3. **Pod Security Standards** - Kubernetes native security levels
4. **Policy engines** - OPA Gatekeeper, Kyverno
5. **Continuous compliance** - Automate scanning and reporting

## Practice Questions

1. What are the five core functions of the NIST Cybersecurity Framework?
2. What tool is commonly used to check CIS Kubernetes benchmarks?
3. What are the three Pod Security Standards levels?
4. Name two policy engines for Kubernetes.
5. What is the purpose of the NSA/CISA Kubernetes Hardening Guide?

---

[← Previous: Platform Security](./05-platform-security.md) | [Back to KCSA Overview](./README.md) | [Next: Sample Practice Questions →](./sample-questions.md)
