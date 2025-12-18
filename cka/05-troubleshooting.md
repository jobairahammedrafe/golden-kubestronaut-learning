# Troubleshooting (30%)

This domain covers troubleshooting Kubernetes clusters, applications, and networking issues. This is the largest domain in the CKA exam.

## Cluster Troubleshooting

### Check Cluster Health

```bash
# Cluster info
kubectl cluster-info
kubectl cluster-info dump

# Component status (deprecated but useful)
kubectl get componentstatuses

# Check nodes
kubectl get nodes
kubectl describe node <node-name>

# Check system pods
kubectl get pods -n kube-system
```

### Control Plane Components

```bash
# Check control plane pods (if using kubeadm)
kubectl get pods -n kube-system

# Check static pod manifests
ls /etc/kubernetes/manifests/
cat /etc/kubernetes/manifests/kube-apiserver.yaml

# Check component logs
kubectl logs -n kube-system kube-apiserver-<node>
kubectl logs -n kube-system kube-controller-manager-<node>
kubectl logs -n kube-system kube-scheduler-<node>
kubectl logs -n kube-system etcd-<node>

# If running as systemd services
sudo journalctl -u kubelet
sudo journalctl -u kube-apiserver
```

### kubelet Troubleshooting

```bash
# Check kubelet status
sudo systemctl status kubelet
sudo systemctl restart kubelet

# Check kubelet logs
sudo journalctl -u kubelet -f
sudo journalctl -u kubelet --since "10 minutes ago"

# Check kubelet config
cat /var/lib/kubelet/config.yaml
cat /etc/kubernetes/kubelet.conf
```

### etcd Troubleshooting

```bash
# Check etcd health
ETCDCTL_API=3 etcdctl endpoint health \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Check etcd members
ETCDCTL_API=3 etcdctl member list \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```

## Node Troubleshooting

### Node Status

```bash
# Get node details
kubectl get nodes -o wide
kubectl describe node <node-name>

# Check node conditions
kubectl get nodes -o jsonpath='{.items[*].status.conditions}'
```

### Node Conditions

| Condition | Description |
|-----------|-------------|
| `Ready` | Node is healthy and ready |
| `MemoryPressure` | Node memory is low |
| `DiskPressure` | Node disk space is low |
| `PIDPressure` | Too many processes |
| `NetworkUnavailable` | Network not configured |

### Node Maintenance

```bash
# Cordon node (prevent scheduling)
kubectl cordon <node-name>

# Drain node (evict pods)
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# Uncordon node
kubectl uncordon <node-name>
```

## Application Troubleshooting

### Pod Debugging

```bash
# Get pod status
kubectl get pods
kubectl get pods -o wide
kubectl get pods --all-namespaces

# Describe pod (events, conditions)
kubectl describe pod <pod-name>

# Get pod YAML
kubectl get pod <pod-name> -o yaml

# Check pod logs
kubectl logs <pod-name>
kubectl logs <pod-name> -c <container-name>
kubectl logs <pod-name> --previous
kubectl logs <pod-name> -f
kubectl logs <pod-name> --tail=100

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/sh
kubectl exec <pod-name> -- cat /etc/config/app.conf
```

### Common Pod Issues

| Status | Cause | Solution |
|--------|-------|----------|
| **Pending** | No node available, resource constraints | Check events, node resources |
| **ImagePullBackOff** | Image not found, auth issues | Check image name, pull secrets |
| **CrashLoopBackOff** | Container crashes repeatedly | Check logs, probe config |
| **CreateContainerConfigError** | ConfigMap/Secret missing | Check references |
| **OOMKilled** | Out of memory | Increase memory limits |
| **Evicted** | Node resource pressure | Check node conditions |

### Debug with Ephemeral Containers

```bash
# Add debug container to running pod
kubectl debug <pod-name> -it --image=busybox --target=<container-name>

# Debug node
kubectl debug node/<node-name> -it --image=ubuntu
```

### Pod Resource Issues

```bash
# Check resource usage
kubectl top pods
kubectl top pods --containers
kubectl top nodes

# Check resource requests/limits
kubectl describe pod <pod-name> | grep -A 5 "Requests\|Limits"
```

## Service Troubleshooting

### Service Debugging

```bash
# Check service
kubectl get svc
kubectl describe svc <service-name>

# Check endpoints
kubectl get endpoints <service-name>

# Test service from within cluster
kubectl run test --image=busybox:1.36 --rm -it -- wget -qO- http://<service-name>

# Check service DNS
kubectl run test --image=busybox:1.36 --rm -it -- nslookup <service-name>
```

### Common Service Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| No endpoints | Selector mismatch | Check pod labels match service selector |
| Connection refused | Wrong port | Check targetPort matches container port |
| DNS not resolving | CoreDNS issues | Check CoreDNS pods |

## Networking Troubleshooting

### DNS Debugging

```bash
# Check CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns

# Test DNS resolution
kubectl run test --image=busybox:1.36 --rm -it -- nslookup kubernetes
kubectl run test --image=busybox:1.36 --rm -it -- nslookup <service>.<namespace>.svc.cluster.local

# Check resolv.conf in pod
kubectl exec <pod-name> -- cat /etc/resolv.conf
```

### Network Policy Debugging

```bash
# List network policies
kubectl get networkpolicies
kubectl describe networkpolicy <policy-name>

# Test connectivity
kubectl exec <pod-name> -- nc -zv <target-ip> <port>
kubectl exec <pod-name> -- wget -qO- --timeout=2 http://<service>
```

### CNI Troubleshooting

```bash
# Check CNI config
ls /etc/cni/net.d/
cat /etc/cni/net.d/*.conf

# Check CNI binaries
ls /opt/cni/bin/

# Check pod networking
kubectl exec <pod-name> -- ip addr
kubectl exec <pod-name> -- ip route
```

## Certificate Troubleshooting

```bash
# Check certificate expiration
kubeadm certs check-expiration

# View certificate details
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout

# Check certificate dates
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -dates

# Renew certificates
kubeadm certs renew all
```

## Logging

### Container Logs

```bash
# View logs
kubectl logs <pod-name>
kubectl logs <pod-name> -c <container>
kubectl logs <pod-name> --all-containers

# Follow logs
kubectl logs -f <pod-name>

# Previous container logs
kubectl logs <pod-name> --previous

# Logs since time
kubectl logs <pod-name> --since=1h
kubectl logs <pod-name> --since-time=2024-01-01T00:00:00Z

# Logs with timestamps
kubectl logs <pod-name> --timestamps
```

### System Logs

```bash
# kubelet logs
sudo journalctl -u kubelet

# Container runtime logs
sudo journalctl -u containerd
sudo journalctl -u docker

# System messages
sudo tail -f /var/log/syslog
sudo tail -f /var/log/messages
```

## Events

```bash
# Get events
kubectl get events
kubectl get events --sort-by='.lastTimestamp'
kubectl get events -n <namespace>

# Watch events
kubectl get events -w

# Filter events
kubectl get events --field-selector type=Warning
kubectl get events --field-selector involvedObject.name=<pod-name>
```

## Troubleshooting Checklist

### Pod Not Starting

1. Check pod status: `kubectl get pod <pod>`
2. Check events: `kubectl describe pod <pod>`
3. Check logs: `kubectl logs <pod>`
4. Check node resources: `kubectl describe node <node>`
5. Check image: `kubectl get pod <pod> -o yaml | grep image`

### Service Not Working

1. Check service: `kubectl get svc <service>`
2. Check endpoints: `kubectl get endpoints <service>`
3. Check pod labels match selector
4. Test from within cluster
5. Check network policies

### Node Not Ready

1. Check node status: `kubectl describe node <node>`
2. Check kubelet: `systemctl status kubelet`
3. Check kubelet logs: `journalctl -u kubelet`
4. Check container runtime
5. Check disk/memory pressure

## Key Concepts to Remember

1. **kubectl describe** - First step for troubleshooting
2. **kubectl logs** - Check container output
3. **kubectl exec** - Debug inside container
4. **Events** - Show what happened
5. **journalctl** - System service logs

## Practice Questions

1. A pod is in CrashLoopBackOff status. How do you troubleshoot?
2. How do you check why a node is NotReady?
3. A service has no endpoints. What could be wrong?
4. How do you view kubelet logs?
5. How do you test DNS resolution from within a pod?

---

[← Previous: Storage](./04-storage.md) | [Back to CKA Overview](./README.md) | [Next: Sample Practice Questions →](./sample-questions.md)
