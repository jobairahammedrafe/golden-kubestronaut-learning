# KCSA Sample Practice Questions

> **Disclaimer**: These are sample practice questions created for study purposes only. They are NOT actual exam questions and are designed to help you test your understanding of KCSA concepts. Real exam questions may differ in format and content.

## Instructions

- Each question has one correct answer unless otherwise specified
- Try to answer without looking at the solutions first
- Review the explanations to understand the concepts better

---

## Section 1: Cloud Native Security Overview

### Question 1.1

What are the 4Cs of Cloud Native Security in order from the outermost to innermost layer?

A) Code, Container, Cluster, Cloud  
B) Cloud, Cluster, Container, Code  
C) Cluster, Cloud, Code, Container  
D) Container, Code, Cloud, Cluster

<details>
<summary>Show Answer</summary>

**Answer: B) Cloud, Cluster, Container, Code**

The 4Cs represent security layers from infrastructure (Cloud) to application (Code). Each layer builds upon the security of the layer below it.

</details>

### Question 1.2

In the shared responsibility model for managed Kubernetes services, who is typically responsible for securing the worker node operating system?

A) Cloud provider only  
B) Customer only  
C) Both cloud provider and customer  
D) Neither - it's automatically secured

<details>
<summary>Show Answer</summary>

**Answer: B) Customer only**

In managed Kubernetes services (like EKS, GKE, AKS), the cloud provider manages the control plane, but customers are responsible for worker node security, including OS patching and configuration.

</details>

### Question 1.3

Which security principle states that users and processes should only have the minimum permissions necessary to perform their tasks?

A) Defense in depth  
B) Zero trust  
C) Least privilege  
D) Separation of duties

<details>
<summary>Show Answer</summary>

**Answer: C) Least privilege**

The principle of least privilege ensures that access rights are limited to only what is required, reducing the potential impact of a security breach.

</details>

---

## Section 2: Kubernetes Cluster Component Security

### Question 2.1

Which Kubernetes component stores all cluster state and should be encrypted at rest?

A) kube-apiserver  
B) kube-scheduler  
C) etcd  
D) kube-controller-manager

<details>
<summary>Show Answer</summary>

**Answer: C) etcd**

etcd is the key-value store that holds all cluster data, including Secrets. Encrypting etcd at rest is critical for protecting sensitive information.

</details>

### Question 2.2

What is the recommended value for the `--anonymous-auth` flag on the kubelet?

A) true  
B) false  
C) webhook  
D) certificate

<details>
<summary>Show Answer</summary>

**Answer: B) false**

Anonymous authentication should be disabled on the kubelet to prevent unauthorized access to the kubelet API.

</details>

### Question 2.3

Which authentication method uses tokens issued by an external identity provider?

A) X.509 client certificates  
B) Service account tokens  
C) OpenID Connect (OIDC)  
D) Static token file

<details>
<summary>Show Answer</summary>

**Answer: C) OpenID Connect (OIDC)**

OIDC allows Kubernetes to integrate with external identity providers like Google, Azure AD, or Okta for user authentication.

</details>

### Question 2.4

What is the correct order of request processing in the Kubernetes API server?

A) Authorization → Authentication → Admission Control  
B) Authentication → Admission Control → Authorization  
C) Authentication → Authorization → Admission Control  
D) Admission Control → Authentication → Authorization

<details>
<summary>Show Answer</summary>

**Answer: C) Authentication → Authorization → Admission Control**

Requests first authenticate (who are you?), then authorize (what can you do?), and finally pass through admission controllers (should this be allowed/modified?).

</details>

---

## Section 3: Kubernetes Security Fundamentals

### Question 3.1

Which Pod Security Standard level provides the most restrictive security policies?

A) Privileged  
B) Baseline  
C) Restricted  
D) Default

<details>
<summary>Show Answer</summary>

**Answer: C) Restricted**

The Restricted level enforces the most stringent security requirements, following current best practices for pod hardening.

</details>

### Question 3.2

What happens to pod-to-pod traffic in a namespace with no Network Policies defined?

A) All traffic is denied by default  
B) All traffic is allowed by default  
C) Only traffic within the namespace is allowed  
D) Only traffic from the same node is allowed

<details>
<summary>Show Answer</summary>

**Answer: B) All traffic is allowed by default**

Without Network Policies, Kubernetes allows all pod-to-pod communication. Network Policies must be explicitly created to restrict traffic.

</details>

### Question 3.3

Which security context field prevents a container process from gaining more privileges than its parent?

A) runAsNonRoot  
B) readOnlyRootFilesystem  
C) allowPrivilegeEscalation  
D) privileged

<details>
<summary>Show Answer</summary>

**Answer: C) allowPrivilegeEscalation**

Setting `allowPrivilegeEscalation: false` prevents a process from gaining additional privileges through setuid binaries or other mechanisms.

</details>

### Question 3.4

Can a RoleBinding in namespace "app" grant permissions defined in a ClusterRole?

A) No, RoleBindings can only reference Roles  
B) Yes, but only for cluster-scoped resources  
C) Yes, the ClusterRole permissions will be scoped to namespace "app"  
D) Yes, and the permissions will apply cluster-wide

<details>
<summary>Show Answer</summary>

**Answer: C) Yes, the ClusterRole permissions will be scoped to namespace "app"**

A RoleBinding can reference a ClusterRole, but the permissions are limited to the namespace where the RoleBinding exists.

</details>

---

## Section 4: Kubernetes Threat Model

### Question 4.1

In the STRIDE threat model, what does the "E" stand for?

A) Encryption  
B) Exploitation  
C) Elevation of Privilege  
D) Enumeration

<details>
<summary>Show Answer</summary>

**Answer: C) Elevation of Privilege**

STRIDE stands for: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege.

</details>

### Question 4.2

Which of the following is a common container escape technique?

A) Using a ClusterIP service  
B) Mounting the host filesystem  
C) Creating a ConfigMap  
D) Using a Deployment

<details>
<summary>Show Answer</summary>

**Answer: B) Mounting the host filesystem**

Mounting sensitive host paths (like `/`, `/etc`, or the Docker socket) can allow attackers to escape the container and access the host system.

</details>

### Question 4.3

Which tool is commonly used for runtime security monitoring in Kubernetes?

A) Trivy  
B) kube-bench  
C) Falco  
D) kubesec

<details>
<summary>Show Answer</summary>

**Answer: C) Falco**

Falco is a CNCF project that provides runtime security monitoring by detecting anomalous activity in containers and Kubernetes.

</details>

---

## Section 5: Platform Security

### Question 5.1

What is the purpose of signing container images with tools like cosign?

A) To compress the image  
B) To verify the image hasn't been tampered with  
C) To encrypt the image contents  
D) To speed up image pulls

<details>
<summary>Show Answer</summary>

**Answer: B) To verify the image hasn't been tampered with**

Image signing creates a cryptographic signature that can be verified to ensure the image hasn't been modified since it was signed.

</details>

### Question 5.2

In a GitOps workflow, how should Kubernetes Secrets be handled?

A) Store them directly in Git  
B) Use base64 encoding in Git  
C) Use Sealed Secrets or external secret managers  
D) Include them in ConfigMaps instead

<details>
<summary>Show Answer</summary>

**Answer: C) Use Sealed Secrets or external secret managers**

Secrets should never be stored in plain text in Git. Tools like Sealed Secrets, SOPS, or external secret managers (Vault, AWS Secrets Manager) should be used.

</details>

### Question 5.3

What does mTLS provide in a service mesh?

A) Load balancing only  
B) Mutual authentication between services  
C) Service discovery  
D) Rate limiting

<details>
<summary>Show Answer</summary>

**Answer: B) Mutual authentication between services**

mTLS (mutual TLS) ensures both the client and server authenticate each other, providing encrypted and authenticated service-to-service communication.

</details>

---

## Section 6: Compliance and Security Frameworks

### Question 6.1

Which tool is commonly used to check Kubernetes clusters against CIS benchmarks?

A) Trivy  
B) kube-bench  
C) Falco  
D) OPA

<details>
<summary>Show Answer</summary>

**Answer: B) kube-bench**

kube-bench is specifically designed to check Kubernetes clusters against CIS Kubernetes Benchmark recommendations.

</details>

### Question 6.2

What are the five core functions of the NIST Cybersecurity Framework?

A) Plan, Do, Check, Act, Review  
B) Identify, Protect, Detect, Respond, Recover  
C) Assess, Implement, Monitor, Report, Improve  
D) Prevent, Detect, Contain, Eradicate, Recover

<details>
<summary>Show Answer</summary>

**Answer: B) Identify, Protect, Detect, Respond, Recover**

The NIST CSF provides a framework for managing cybersecurity risk through these five core functions.

</details>

### Question 6.3

Which Kubernetes-native policy engine uses YAML-based policies?

A) OPA Gatekeeper  
B) Kyverno  
C) Falco  
D) Trivy

<details>
<summary>Show Answer</summary>

**Answer: B) Kyverno**

Kyverno uses Kubernetes-native YAML policies, while OPA Gatekeeper uses the Rego policy language.

</details>

---

## Scenario-Based Questions

### Scenario 1

Your security team has identified that some pods in your cluster are running as root. You need to enforce that all pods in the "production" namespace run as non-root users.

**Question**: Which is the most appropriate solution?

A) Add a LimitRange to the namespace  
B) Apply Pod Security Standards with "restricted" level  
C) Create a ResourceQuota  
D) Configure a HorizontalPodAutoscaler

<details>
<summary>Show Answer</summary>

**Answer: B) Apply Pod Security Standards with "restricted" level**

Pod Security Standards at the "restricted" level enforce that containers must run as non-root, among other security requirements.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
```

</details>

### Scenario 2

You need to ensure that pods in the "backend" namespace can only communicate with pods in the "database" namespace on port 5432.

**Question**: What type of resource should you create?

A) Service  
B) Ingress  
C) NetworkPolicy  
D) PodSecurityPolicy

<details>
<summary>Show Answer</summary>

**Answer: C) NetworkPolicy**

NetworkPolicy resources control pod-to-pod communication. You would create an egress policy in the "backend" namespace allowing traffic to the "database" namespace on port 5432.

</details>

### Scenario 3

An audit reveals that your cluster's API server allows anonymous requests. What is the recommended remediation?

A) Enable RBAC authorization mode  
B) Set `--anonymous-auth=false` on the API server  
C) Create a ClusterRole for anonymous users  
D) Enable audit logging

<details>
<summary>Show Answer</summary>

**Answer: B) Set `--anonymous-auth=false` on the API server**

Disabling anonymous authentication prevents unauthenticated requests from accessing the API server.

</details>

---

## Study Tips

1. **Understand the concepts** - Don't just memorize; understand why security controls exist
2. **Practice with real clusters** - Set up a test cluster and implement security controls
3. **Review official documentation** - Kubernetes security docs are comprehensive
4. **Know the tools** - Familiarize yourself with kube-bench, Trivy, Falco, OPA
5. **Understand compliance frameworks** - Know the basics of CIS, NIST, and Pod Security Standards

---

[← Back to KCSA Overview](./README.md)
