# Cluster Troubleshooting Scenarios

Real-world troubleshooting scenarios for CKA/CKS exam preparation.

---

## Scenario 1: Node NotReady

### Problem

```
$ kubectl get nodes
NAME      STATUS     ROLES           AGE   VERSION
master    Ready      control-plane   10d   v1.28.0
worker1   NotReady   <none>          10d   v1.28.0
```

### Diagnosis Steps

```bash
# 1. Check node conditions
kubectl describe node worker1 | grep -A5 Conditions

# 2. SSH to node and check kubelet
ssh worker1
sudo systemctl status kubelet
sudo journalctl -u kubelet -f

# 3. Check container runtime
sudo systemctl status containerd
sudo crictl ps
```

### Common Causes & Solutions

<details>
<summary>Kubelet not running</summary>

```bash
sudo systemctl start kubelet
sudo systemctl enable kubelet
```

</details>

<details>
<summary>Container runtime issue</summary>

```bash
sudo systemctl restart containerd
sudo systemctl status containerd
```

</details>

<details>
<summary>Network plugin issue</summary>

```bash
# Check CNI pods
kubectl get pods -n kube-system | grep -E "calico|flannel|weave"

# Reinstall CNI if needed
kubectl apply -f <cni-manifest.yaml>
```

</details>

<details>
<summary>Disk pressure</summary>

```bash
# Check disk usage
df -h

# Clean up unused images
sudo crictl rmi --prune
```

</details>

---

## Scenario 2: Pod Stuck in Pending

### Problem

```
$ kubectl get pods
NAME    READY   STATUS    RESTARTS   AGE
nginx   0/1     Pending   0          5m
```

### Diagnosis Steps

```bash
# 1. Check pod events
kubectl describe pod nginx

# 2. Check node resources
kubectl describe nodes | grep -A5 "Allocated resources"

# 3. Check scheduler
kubectl get pods -n kube-system | grep scheduler
```

### Common Causes & Solutions

<details>
<summary>Insufficient resources</summary>

```bash
# Check resource requests vs available
kubectl describe nodes | grep -A10 "Allocated resources"

# Solution: Scale down other pods or add nodes
kubectl scale deployment other-app --replicas=1
```

</details>

<details>
<summary>No matching node (nodeSelector/affinity)</summary>

```bash
# Check pod spec
kubectl get pod nginx -o yaml | grep -A5 nodeSelector

# Add label to node
kubectl label node worker1 disktype=ssd
```

</details>

<details>
<summary>Taints preventing scheduling</summary>

```bash
# Check node taints
kubectl describe node worker1 | grep Taints

# Add toleration to pod or remove taint
kubectl taint nodes worker1 key:NoSchedule-
```

</details>

<details>
<summary>PVC not bound</summary>

```bash
# Check PVC status
kubectl get pvc

# Check PV availability
kubectl get pv
```

</details>

---

## Scenario 3: Pod CrashLoopBackOff

### Problem

```
$ kubectl get pods
NAME    READY   STATUS             RESTARTS   AGE
app     0/1     CrashLoopBackOff   5          10m
```

### Diagnosis Steps

```bash
# 1. Check pod logs
kubectl logs app
kubectl logs app --previous

# 2. Check pod events
kubectl describe pod app

# 3. Check container exit code
kubectl get pod app -o jsonpath='{.status.containerStatuses[0].lastState.terminated.exitCode}'
```

### Common Causes & Solutions

<details>
<summary>Application error</summary>

```bash
# Check logs for errors
kubectl logs app --previous

# Fix application code or configuration
```

</details>

<details>
<summary>Missing ConfigMap/Secret</summary>

```bash
# Check if referenced ConfigMap exists
kubectl get configmap myconfig

# Create missing ConfigMap
kubectl create configmap myconfig --from-literal=key=value
```

</details>

<details>
<summary>Liveness probe failing</summary>

```bash
# Check probe configuration
kubectl get pod app -o yaml | grep -A10 livenessProbe

# Adjust probe settings or fix application health endpoint
```

</details>

<details>
<summary>Resource limits too low</summary>

```bash
# Check OOMKilled
kubectl describe pod app | grep OOMKilled

# Increase memory limits
kubectl set resources deployment app --limits=memory=512Mi
```

</details>

---

## Scenario 4: Service Not Accessible

### Problem

```
$ kubectl exec test-pod -- curl http://my-service:80
curl: (7) Failed to connect
```

### Diagnosis Steps

```bash
# 1. Check service exists
kubectl get svc my-service

# 2. Check endpoints
kubectl get endpoints my-service

# 3. Check pod labels match service selector
kubectl get pods --show-labels
kubectl get svc my-service -o yaml | grep -A5 selector
```

### Common Causes & Solutions

<details>
<summary>No endpoints (selector mismatch)</summary>

```bash
# Check service selector
kubectl get svc my-service -o jsonpath='{.spec.selector}'

# Check pod labels
kubectl get pods --show-labels

# Fix labels
kubectl label pod my-pod app=myapp
```

</details>

<details>
<summary>Pod not ready</summary>

```bash
# Check pod readiness
kubectl get pods

# Check readiness probe
kubectl describe pod my-pod | grep -A5 Readiness
```

</details>

<details>
<summary>NetworkPolicy blocking traffic</summary>

```bash
# Check network policies
kubectl get networkpolicy

# Check if policy allows traffic
kubectl describe networkpolicy
```

</details>

<details>
<summary>Wrong port configuration</summary>

```bash
# Check service port vs target port
kubectl get svc my-service -o yaml

# Check container port
kubectl get pod my-pod -o yaml | grep containerPort
```

</details>

---

## Scenario 5: API Server Not Responding

### Problem

```
$ kubectl get nodes
The connection to the server was refused
```

### Diagnosis Steps

```bash
# 1. Check API server pod (on control plane)
sudo crictl ps | grep kube-apiserver

# 2. Check API server logs
sudo crictl logs <apiserver-container-id>

# 3. Check manifest
sudo cat /etc/kubernetes/manifests/kube-apiserver.yaml
```

### Common Causes & Solutions

<details>
<summary>API server not running</summary>

```bash
# Check static pod manifest
sudo ls /etc/kubernetes/manifests/

# Check for syntax errors
sudo cat /etc/kubernetes/manifests/kube-apiserver.yaml | head -50

# Check kubelet logs
sudo journalctl -u kubelet | grep apiserver
```

</details>

<details>
<summary>Certificate issues</summary>

```bash
# Check certificate expiry
sudo openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -dates

# Renew certificates
sudo kubeadm certs renew all
```

</details>

<details>
<summary>etcd not accessible</summary>

```bash
# Check etcd pod
sudo crictl ps | grep etcd

# Check etcd health
ETCDCTL_API=3 etcdctl endpoint health \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```

</details>

---

## Scenario 6: etcd Issues

### Problem

etcd cluster unhealthy or data corruption

### Diagnosis Steps

```bash
# 1. Check etcd pod
kubectl get pods -n kube-system | grep etcd

# 2. Check etcd health
ETCDCTL_API=3 etcdctl endpoint health \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# 3. Check etcd logs
sudo crictl logs <etcd-container-id>
```

### Solutions

<details>
<summary>Restore from backup</summary>

```bash
# Stop API server
sudo mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/

# Restore etcd
ETCDCTL_API=3 etcdctl snapshot restore /backup/etcd-snapshot.db \
  --data-dir=/var/lib/etcd-restored

# Update etcd manifest to use new data-dir
sudo sed -i 's|/var/lib/etcd|/var/lib/etcd-restored|g' \
  /etc/kubernetes/manifests/etcd.yaml

# Restore API server
sudo mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/
```

</details>

---

## Quick Troubleshooting Commands

```bash
# Overall cluster health
kubectl get componentstatuses
kubectl get nodes
kubectl get pods -A

# Events sorted by time
kubectl get events --sort-by='.lastTimestamp' -A

# Resource usage
kubectl top nodes
kubectl top pods -A

# Logs
kubectl logs <pod> -f
kubectl logs <pod> --previous
kubectl logs <pod> -c <container>

# Debug pod
kubectl run debug --image=busybox --rm -it --restart=Never -- sh

# Check DNS
kubectl run dns-test --image=busybox --rm -it --restart=Never -- nslookup kubernetes
```

---

[← Back to Home](../README.md)
