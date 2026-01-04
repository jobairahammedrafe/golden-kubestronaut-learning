# Cilium Architecture

<div class="pdf-download">
  <a href="/pdf/01-cilium-architecture.pdf" class="md-button md-button--primary" download>
    <span class="twemoji">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M5 20h14v-2H5v2zM19 9h-4V3H9v6H5l7 7 7-7z"></path></svg>
    </span>
    Download PDF Version
  </a>
</div>



Comprehensive guide to Cilium networking for CCA certification.

---

## Overview

Cilium is a CNI plugin that provides:

- **Networking** - Pod-to-pod connectivity using eBPF
- **Security** - Network policies with L3-L7 filtering
- **Observability** - Deep visibility with Hubble
- **Load Balancing** - Kubernetes service implementation

---

## Architecture Components

### Cilium Agent

- Runs on every node as DaemonSet
- Manages eBPF programs
- Implements network policies
- Handles service load balancing

### Cilium Operator

- Cluster-wide operations
- IP address management (IPAM)
- Garbage collection

### Hubble

- Observability platform
- Network flow visibility
- Service dependency maps

---

## eBPF Technology

eBPF (extended Berkeley Packet Filter) enables:

- High-performance packet processing
- Programmable network datapath
- No kernel modifications needed
- Real-time observability

```
┌─────────────────────────────────────────────────────────┐
│                    User Space                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Cilium CLI  │  │   Hubble    │  │  Operator   │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    Kernel Space                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │                  eBPF Programs                    │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐         │   │
│  │  │  XDP    │  │   TC    │  │ Socket  │         │   │
│  │  └─────────┘  └─────────┘  └─────────┘         │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## Installation

### Using Cilium CLI

```bash
# Install Cilium CLI
curl -L --remote-name-all https://github.com/cilium/cilium-cli/releases/latest/download/cilium-linux-amd64.tar.gz
tar xzvf cilium-linux-amd64.tar.gz
sudo mv cilium /usr/local/bin

# Install Cilium
cilium install

# Check status
cilium status

# Enable Hubble
cilium hubble enable --ui
```

### Using Helm

```bash
helm repo add cilium https://helm.cilium.io/
helm install cilium cilium/cilium --namespace kube-system
```

---

## Network Policies

### CiliumNetworkPolicy

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-frontend
  namespace: default
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
    toPorts:
    - ports:
      - port: "80"
        protocol: TCP
```

### L7 Policy (HTTP)

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: l7-policy
spec:
  endpointSelector:
    matchLabels:
      app: api
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
    toPorts:
    - ports:
      - port: "80"
        protocol: TCP
      rules:
        http:
        - method: GET
          path: "/api/v1/.*"
```

### Cluster-wide Policy

```yaml
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: default-deny
spec:
  endpointSelector: {}
  ingress:
  - fromEntities:
    - cluster
```

---

## Hubble Observability

### Enable Hubble

```bash
cilium hubble enable
cilium hubble enable --ui
```

### Hubble CLI

```bash
# Install Hubble CLI
export HUBBLE_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/hubble/master/stable.txt)
curl -L --remote-name-all https://github.com/cilium/hubble/releases/download/$HUBBLE_VERSION/hubble-linux-amd64.tar.gz
tar xzvf hubble-linux-amd64.tar.gz
sudo mv hubble /usr/local/bin

# Port forward
cilium hubble port-forward &

# Observe flows
hubble observe
hubble observe --namespace default
hubble observe --pod frontend
hubble observe --verdict DROPPED
```

### Hubble UI

```bash
cilium hubble ui
```

---

## Service Load Balancing

Cilium replaces kube-proxy with eBPF-based load balancing:

```bash
# Install without kube-proxy
cilium install --set kubeProxyReplacement=strict

# Verify
cilium status | grep KubeProxyReplacement
```

---

## Useful Commands

```bash
# Status
cilium status
cilium status --verbose

# Connectivity test
cilium connectivity test

# Endpoint list
cilium endpoint list

# Service list
cilium service list

# BPF maps
cilium bpf lb list
cilium bpf ct list global
cilium bpf policy get

# Debug
cilium debuginfo
```

---

[← Back to CCA Overview](./README.md)
