# Security Policy

## Reporting Security Issues

If you discover a security vulnerability in this repository, please report it responsibly.

### What to Report

- Vulnerabilities in any code examples
- Exposed secrets or credentials in documentation
- Security misconfigurations in lab exercises
- Links to malicious or compromised resources

### How to Report

1. **Do NOT** open a public GitHub issue for security vulnerabilities
2. Open a private security advisory on GitHub, or
3. Contact the maintainers directly

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Security Best Practices for Labs

When using the lab exercises in this repository, follow these security practices:

### Kubernetes Cluster Security

```yaml
# Always use resource limits
resources:
  limits:
    cpu: "500m"
    memory: "128Mi"
  requests:
    cpu: "100m"
    memory: "64Mi"
```

### Secrets Management

- Never commit real secrets to the repository
- Use placeholder values in examples
- Reference external secret management solutions

### Network Policies

Always implement network policies in practice environments:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### RBAC

Follow the principle of least privilege:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
```

## Content Security

### NDA Compliance

- Never share actual exam questions
- Do not post screenshots from exams
- Focus on concepts, not specific exam content

### External Links

- Only link to trusted, official sources
- Verify links are not compromised
- Report any suspicious links immediately

## Responsible Disclosure

We follow responsible disclosure practices:

1. **Acknowledgment** - We will acknowledge receipt within 48 hours
2. **Assessment** - We will assess and prioritize the issue
3. **Resolution** - We will work on a fix
4. **Credit** - We will credit reporters (unless anonymity is preferred)

## Contact

For security concerns, please contact the maintainers through GitHub.

Thank you for helping keep this learning resource safe!
