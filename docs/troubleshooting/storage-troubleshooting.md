# Storage Troubleshooting Scenarios

Real-world storage troubleshooting scenarios for CKA exam preparation.

---

## Scenario 1: PVC Stuck in Pending

### Problem

```bash
$ kubectl get pvc
NAME      STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
my-pvc    Pending                                      standard       5m
```

### Diagnosis Steps

```bash
# 1. Describe PVC for events
kubectl describe pvc my-pvc

# 2. Check StorageClass
kubectl get storageclass

# 3. Check available PVs
kubectl get pv

# 4. Check provisioner pods
kubectl get pods -n kube-system | grep provisioner
```

### Solutions

<details>
<summary>No matching PV available</summary>

```yaml
# Create matching PV
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
  - ReadWriteOnce
  hostPath:
    path: /data/my-pv
  storageClassName: standard
```

</details>

<details>
<summary>StorageClass not found</summary>

```bash
# List available StorageClasses
kubectl get storageclass

# Create StorageClass or update PVC to use existing one
kubectl patch pvc my-pvc -p '{"spec":{"storageClassName":"existing-class"}}'
```

</details>

<details>
<summary>Provisioner not working</summary>

```bash
# Check provisioner logs
kubectl logs -n kube-system <provisioner-pod>

# Restart provisioner
kubectl rollout restart deployment <provisioner> -n kube-system
```

</details>

---

## Scenario 2: Pod Cannot Mount Volume

### Problem

```bash
$ kubectl get pods
NAME    READY   STATUS              RESTARTS   AGE
my-pod  0/1     ContainerCreating   0          5m

$ kubectl describe pod my-pod
Events:
  Warning  FailedMount  Unable to attach or mount volumes
```

### Diagnosis Steps

```bash
# 1. Check PVC is bound
kubectl get pvc

# 2. Check PV status
kubectl get pv

# 3. Check node where pod is scheduled
kubectl get pod my-pod -o wide

# 4. Check volume attachment
kubectl get volumeattachment
```

### Solutions

<details>
<summary>PVC not bound</summary>

```bash
# Check PVC status
kubectl get pvc my-pvc

# If pending, check PV availability
kubectl get pv
```

</details>

<details>
<summary>Volume already attached to another node</summary>

```bash
# For RWO volumes, check which node has it
kubectl get pv my-pv -o yaml | grep -A5 nodeAffinity

# Either move pod to that node or use RWX volume
```

</details>

<details>
<summary>Node storage driver issue</summary>

```bash
# Check CSI driver pods
kubectl get pods -n kube-system | grep csi

# Check kubelet logs on node
ssh node1 "sudo journalctl -u kubelet | grep -i volume"
```

</details>

---

## Scenario 3: Volume Data Not Persisting

### Problem

Data written to volume is lost after pod restart

### Diagnosis Steps

```bash
# 1. Check volume mount in pod
kubectl get pod my-pod -o yaml | grep -A10 volumeMounts

# 2. Check PVC reclaim policy
kubectl get pv my-pv -o yaml | grep persistentVolumeReclaimPolicy

# 3. Verify data path
kubectl exec my-pod -- ls -la /data
```

### Solutions

<details>
<summary>Using emptyDir instead of PVC</summary>

```yaml
# emptyDir is ephemeral - use PVC instead
volumes:
- name: data
  persistentVolumeClaim:
    claimName: my-pvc
```

</details>

<details>
<summary>Wrong mount path</summary>

```bash
# Check where app writes data
kubectl exec my-pod -- cat /app/config | grep data_path

# Update volumeMount path to match
```

</details>

<details>
<summary>Reclaim policy is Delete</summary>

```bash
# Change to Retain for important data
kubectl patch pv my-pv -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
```

</details>

---

## Scenario 4: Disk Pressure on Node

### Problem

```bash
$ kubectl describe node worker1
Conditions:
  Type             Status
  DiskPressure     True
```

### Diagnosis Steps

```bash
# 1. Check disk usage on node
ssh worker1 "df -h"

# 2. Check container images
ssh worker1 "sudo crictl images"

# 3. Check container logs size
ssh worker1 "sudo du -sh /var/log/containers/*"
```

### Solutions

<details>
<summary>Clean unused images</summary>

```bash
ssh worker1 "sudo crictl rmi --prune"
```

</details>

<details>
<summary>Clean old container logs</summary>

```bash
# Truncate large log files
ssh worker1 "sudo truncate -s 0 /var/log/containers/*.log"
```

</details>

<details>
<summary>Remove unused volumes</summary>

```bash
# List unused volumes
kubectl get pv | grep Released

# Delete released PVs
kubectl delete pv <released-pv-name>
```

</details>

---

## Storage Debugging Commands

```bash
# Check PV/PVC status
kubectl get pv,pvc -A

# Describe for events
kubectl describe pvc my-pvc
kubectl describe pv my-pv

# Check StorageClass
kubectl get storageclass -o yaml

# Check CSI drivers
kubectl get csidrivers

# Check volume attachments
kubectl get volumeattachment

# Debug from inside pod
kubectl exec my-pod -- df -h
kubectl exec my-pod -- mount | grep /data
```

---

[← Back to Home](../README.md)
