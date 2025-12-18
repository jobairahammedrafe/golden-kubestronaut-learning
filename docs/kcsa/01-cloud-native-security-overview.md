# Overview of Cloud Native Security (14%)

This domain covers the foundational concepts of security in cloud native environments.

## The 4Cs of Cloud Native Security

Cloud native security is built on four layers, each building upon the previous:

```text
┌─────────────────────────────────────┐
│              Code                   │  ← Application security
├─────────────────────────────────────┤
│            Container                │  ← Container security
├─────────────────────────────────────┤
│             Cluster                 │  ← Kubernetes security
├─────────────────────────────────────┤
│              Cloud                  │  ← Infrastructure security
└─────────────────────────────────────┘
```

### Cloud Layer

The foundation of your security posture:

- **Infrastructure security** - Physical and virtual infrastructure
- **Network security** - Firewalls, VPCs, security groups
- **Identity and Access Management (IAM)** - Cloud provider access controls
- **Data encryption** - At rest and in transit

### Cluster Layer

Kubernetes-specific security:

- **API Server security** - Authentication, authorization
- **etcd security** - Encryption, access controls
- **Node security** - OS hardening, kubelet configuration
- **Network policies** - Pod-to-pod communication rules

### Container Layer

Container runtime security:

- **Image security** - Vulnerability scanning, trusted registries
- **Runtime security** - Seccomp, AppArmor, SELinux
- **Resource limits** - CPU, memory constraints
- **Read-only filesystems** - Immutable containers

### Code Layer

Application-level security:

- **Secure coding practices** - Input validation, output encoding
- **Dependency management** - Vulnerability scanning
- **Secrets management** - No hardcoded credentials
- **TLS/mTLS** - Encrypted communications

## Cloud Native Security Principles

### Defense in Depth

Multiple layers of security controls:

```text
┌─────────────────────────────────────────────────┐
│                   Perimeter                      │
│  ┌───────────────────────────────────────────┐  │
│  │                Network                     │  │
│  │  ┌─────────────────────────────────────┐  │  │
│  │  │              Host                    │  │  │
│  │  │  ┌───────────────────────────────┐  │  │  │
│  │  │  │          Application          │  │  │  │
│  │  │  │  ┌─────────────────────────┐  │  │  │  │
│  │  │  │  │         Data            │  │  │  │  │
│  │  │  │  └─────────────────────────┘  │  │  │  │
│  │  │  └───────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### Least Privilege

Grant only the minimum permissions necessary:

- Use specific RBAC roles instead of cluster-admin
- Limit service account permissions
- Restrict network access with Network Policies
- Use read-only file systems where possible

### Zero Trust

Never trust, always verify:

- Authenticate all requests
- Authorize based on identity and context
- Encrypt all communications
- Continuously validate security posture

### Shift Left Security

Integrate security early in the development lifecycle:

```text
Plan → Code → Build → Test → Release → Deploy → Operate
  ↑       ↑      ↑       ↑       ↑         ↑        ↑
  └───────┴──────┴───────┴───────┴─────────┴────────┘
              Security at every stage
```

## Cloud Provider Security

### Shared Responsibility Model

| Layer | Cloud Provider | Customer |
|-------|---------------|----------|
| **Physical Security** | ✓ | |
| **Network Infrastructure** | ✓ | |
| **Hypervisor** | ✓ | |
| **Operating System** | Managed K8s: ✓ | Self-managed: ✓ |
| **Kubernetes Control Plane** | Managed K8s: ✓ | Self-managed: ✓ |
| **Kubernetes Worker Nodes** | | ✓ |
| **Applications** | | ✓ |
| **Data** | | ✓ |

### Cloud Security Services

| Service Type | AWS | GCP | Azure |
|-------------|-----|-----|-------|
| **IAM** | IAM | Cloud IAM | Azure AD |
| **Secrets** | Secrets Manager | Secret Manager | Key Vault |
| **KMS** | KMS | Cloud KMS | Key Vault |
| **Security Scanning** | Inspector | Security Command Center | Defender |

## Security Observability

### Logging

Essential logs to collect:

- API Server audit logs
- Container runtime logs
- Application logs
- Network flow logs

### Monitoring

Key security metrics:

- Failed authentication attempts
- RBAC denials
- Network policy violations
- Resource quota breaches

### Alerting

Critical security alerts:

- Privileged container creation
- Secrets access patterns
- Unusual API activity
- Pod security violations

## Key Concepts to Remember

1. **4Cs model** - Cloud, Cluster, Container, Code
2. **Defense in depth** - Multiple security layers
3. **Least privilege** - Minimum necessary permissions
4. **Zero trust** - Never trust, always verify
5. **Shared responsibility** - Know what you're responsible for

## Practice Questions

1. What are the 4Cs of Cloud Native Security?
2. In the shared responsibility model, who is responsible for application security?
3. What does "shift left" mean in the context of security?
4. Name three principles of zero trust security.
5. What is defense in depth?

---

[Back to KCSA Overview](./README.md) | [Next: Kubernetes Cluster Component Security →](./02-cluster-component-security.md)
