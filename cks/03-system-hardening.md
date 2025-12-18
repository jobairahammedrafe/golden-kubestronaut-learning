# System Hardening (15%)

This domain covers hardening the underlying host systems and using kernel security features.

## AppArmor

### AppArmor Basics

```bash
# Check AppArmor status
aa-status
systemctl status apparmor

# List loaded profiles
cat /sys/kernel/security/apparmor/profiles

# Load a profile
apparmor_parser -q /etc/apparmor.d/my-profile

# Reload a profile
apparmor_parser -r /etc/apparmor.d/my-profile
```

### AppArmor Profile Example

```text
# /etc/apparmor.d/k8s-deny-write
#include <tunables/global>

profile k8s-deny-write flags=(attach_disconnected) {
  #include <abstractions/base>

  file,

  # Deny all file writes
  deny /** w,
}
```

### Use AppArmor in Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: apparmor-pod
  annotations:
    container.apparmor.security.beta.kubernetes.io/nginx: localhost/k8s-deny-write
spec:
  containers:
  - name: nginx
    image: nginx
```

### AppArmor Profile Modes

| Mode | Description |
|------|-------------|
| `enforce` | Enforces the policy |
| `complain` | Logs violations but allows |
| `unconfined` | No restrictions |

## seccomp (Secure Computing Mode)

### seccomp Profile Location

```bash
# Default kubelet seccomp profile path
/var/lib/kubelet/seccomp/

# Create profile directory
mkdir -p /var/lib/kubelet/seccomp/profiles
```

### seccomp Profile Example

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": [
    "SCMP_ARCH_X86_64"
  ],
  "syscalls": [
    {
      "names": [
        "accept4",
        "bind",
        "clone",
        "close",
        "connect",
        "epoll_create1",
        "epoll_ctl",
        "epoll_pwait",
        "execve",
        "exit_group",
        "fcntl",
        "fstat",
        "futex",
        "getdents64",
        "getpid",
        "getrandom",
        "getsockname",
        "getsockopt",
        "listen",
        "mmap",
        "mprotect",
        "nanosleep",
        "newfstatat",
        "openat",
        "read",
        "recvfrom",
        "rt_sigaction",
        "rt_sigprocmask",
        "sendto",
        "set_tid_address",
        "setsockopt",
        "socket",
        "write"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

### Use seccomp in Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: seccomp-pod
spec:
  securityContext:
    seccompProfile:
      type: Localhost
      localhostProfile: profiles/audit.json
  containers:
  - name: nginx
    image: nginx
```

### seccomp Profile Types

| Type | Description |
|------|-------------|
| `RuntimeDefault` | Container runtime default profile |
| `Unconfined` | No seccomp filtering |
| `Localhost` | Custom profile from node |

### RuntimeDefault seccomp

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: runtime-default-pod
spec:
  securityContext:
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: nginx
    image: nginx
```

## Minimize Host OS Footprint

### Reduce Attack Surface

```bash
# Remove unnecessary packages
apt-get remove --purge <package>

# Disable unnecessary services
systemctl disable <service>
systemctl stop <service>

# Check listening ports
netstat -tlnp
ss -tlnp

# Check running processes
ps aux
```

### Secure SSH

```bash
# /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
PermitEmptyPasswords no
X11Forwarding no
MaxAuthTries 3
```

### File System Security

```bash
# Set proper permissions
chmod 600 /etc/kubernetes/admin.conf
chmod 600 /etc/kubernetes/pki/*.key

# Check file permissions
ls -la /etc/kubernetes/
ls -la /etc/kubernetes/pki/
```

## Limit Node Access

### Restrict SSH Access

```bash
# Allow only specific users
# /etc/ssh/sshd_config
AllowUsers admin

# Use SSH keys only
PasswordAuthentication no
```

### Use Network Policies for Node Access

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: restrict-node-access
  namespace: kube-system
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  ingress:
  - from:
    - ipBlock:
        cidr: 10.0.0.0/8
```

## Linux Capabilities

### Drop All Capabilities

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: drop-caps-pod
spec:
  containers:
  - name: nginx
    image: nginx
    securityContext:
      capabilities:
        drop:
        - ALL
```

### Add Specific Capabilities

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: net-admin-pod
spec:
  containers:
  - name: nginx
    image: nginx
    securityContext:
      capabilities:
        drop:
        - ALL
        add:
        - NET_BIND_SERVICE
```

### Common Capabilities

| Capability | Description |
|------------|-------------|
| `NET_BIND_SERVICE` | Bind to ports < 1024 |
| `NET_ADMIN` | Network administration |
| `SYS_ADMIN` | System administration (dangerous) |
| `SYS_PTRACE` | Trace processes |
| `CHOWN` | Change file ownership |

## Kernel Hardening

### sysctl Settings

```bash
# /etc/sysctl.d/99-kubernetes-cis.conf

# Disable IP forwarding (if not needed)
net.ipv4.ip_forward = 0

# Disable source routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0

# Enable SYN cookies
net.ipv4.tcp_syncookies = 1

# Disable ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0

# Apply settings
sysctl --system
```

## IAM Roles (Cloud)

### AWS IAM for Nodes

```yaml
# Restrict node IAM role permissions
# Only allow necessary EC2 and ECR actions
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ecr:GetAuthorizationToken",
        "ecr:BatchGetImage"
      ],
      "Resource": "*"
    }
  ]
}
```

### Pod Identity (IRSA)

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-sa
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789:role/my-role
```

## Key Concepts to Remember

1. **AppArmor** - Linux security module for access control
2. **seccomp** - System call filtering
3. **Capabilities** - Drop ALL, add only needed
4. **Minimize footprint** - Remove unnecessary packages/services
5. **Kernel hardening** - sysctl security settings

## Practice Questions

1. How do you apply an AppArmor profile to a container?
2. What is the difference between seccomp RuntimeDefault and Localhost?
3. How do you drop all capabilities from a container?
4. Where are seccomp profiles stored on the node?
5. How do you check AppArmor status on a node?

---

[← Previous: Cluster Hardening](./02-cluster-hardening.md) | [Back to CKS Overview](./README.md) | [Next: Minimize Microservice Vulnerabilities →](./04-minimize-microservice-vulnerabilities.md)
