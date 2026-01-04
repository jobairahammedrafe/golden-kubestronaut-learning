# CKA Sample Practice Questions

<div class="pdf-download">
  <a href="/pdf/sample-questions.pdf" class="md-button md-button--primary" download>
    <span class="twemoji">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M5 20h14v-2H5v2zM19 9h-4V3H9v6H5l7 7 7-7z"></path></svg>
    </span>
    Download PDF Version
  </a>
</div>



> **Disclaimer**: These are sample practice questions created for study purposes only. They are NOT actual exam questions and are designed to help you test your understanding of CKA concepts. Real exam questions may differ in format and content.

## Practice Resources

Before attempting these questions, we highly recommend practicing on:

- **[Killercoda CKA Scenarios](https://killercoda.com/cka)** ⭐ Free hands-on practice environments
- **[killer.sh CKA Simulator](https://killer.sh/cka)** - Included with exam registration

## Instructions

- The CKA exam is **performance-based** (hands-on), not multiple choice
- Practice these scenarios in a real Kubernetes cluster
- Time yourself - aim for efficiency
- Use imperative commands when possible to save time

---

## Section 1: Cluster Architecture, Installation & Configuration (25%)

### Question 1.1 - Cluster Upgrade

Upgrade the control plane node from Kubernetes 1.29.0 to 1.30.0.

<details>
<summary>Show Solution</summary>

```bash
# Upgrade kubeadm
sudo apt-mark unhold kubeadm
sudo apt-get update && sudo apt-get install -y kubeadm=1.30.0-1.1
sudo apt-mark hold kubeadm

# Plan and apply upgrade
sudo kubeadm upgrade plan
sudo kubeadm upgrade apply v1.30.0

# Upgrade kubelet and kubectl
sudo apt-mark unhold kubelet kubectl
sudo apt-get update && sudo apt-get install -y kubelet=1.30.0-1.1 kubectl=1.30.0-1.1
sudo apt-mark hold kubelet kubectl

# Restart kubelet
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

</details>

### Question 1.2 - etcd Backup

Create a backup of etcd to `/backup/etcd-snapshot.db`.

<details>
<summary>Show Solution</summary>

```bash
ETCDCTL_API=3 etcdctl snapshot save /backup/etcd-snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Verify backup
ETCDCTL_API=3 etcdctl snapshot status /backup/etcd-snapshot.db --write-out=table
```

</details>

### Question 1.3 - RBAC

Create a Role named `pod-reader` in the `development` namespace that allows `get`, `list`, and `watch` on pods. Then create a RoleBinding to bind this role to user `jane`.

<details>
<summary>Show Solution</summary>

```bash
# Create namespace if not exists
kubectl create namespace development

# Create role
kubectl create role pod-reader \
  --verb=get,list,watch \
  --resource=pods \
  -n development

# Create rolebinding
kubectl create rolebinding read-pods \
  --role=pod-reader \
  --user=jane \
  -n development

# Verify
kubectl auth can-i list pods -n development --as jane
```

</details>

### Question 1.4 - Join Worker Node

A new worker node needs to join the cluster. Generate the join command.

<details>
<summary>Show Solution</summary>

```bash
# On control plane
kubeadm token create --print-join-command

# Output will be something like:
# kubeadm join <control-plane-ip>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>

# Run the output command on the worker node with sudo
```

</details>

---

## Section 2: Workloads & Scheduling (15%)

### Question 2.1 - Node Affinity

Create a deployment named `web-app` with 3 replicas using image `nginx:1.21`. The pods should only be scheduled on nodes with label `disk=ssd`.

<details>
<summary>Show Solution</summary>

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: disk
                operator: In
                values:
                - ssd
      containers:
      - name: nginx
        image: nginx:1.21
```

```bash
# Or label a node first
kubectl label nodes <node-name> disk=ssd
```

</details>

### Question 2.2 - Taints and Tolerations

Taint node `node01` with `key=value:NoSchedule`. Then create a pod named `tolerant-pod` that can be scheduled on this node.

<details>
<summary>Show Solution</summary>

```bash
# Taint the node
kubectl taint nodes node01 key=value:NoSchedule
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: tolerant-pod
spec:
  tolerations:
  - key: "key"
    operator: "Equal"
    value: "value"
    effect: "NoSchedule"
  containers:
  - name: nginx
    image: nginx
```

</details>

### Question 2.3 - DaemonSet

Create a DaemonSet named `log-collector` using image `fluentd:v1.14` that runs on all nodes including control plane nodes.

<details>
<summary>Show Solution</summary>

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: log-collector
spec:
  selector:
    matchLabels:
      name: log-collector
  template:
    metadata:
      labels:
        name: log-collector
    spec:
      tolerations:
      - key: node-role.kubernetes.io/control-plane
        operator: Exists
        effect: NoSchedule
      - key: node-role.kubernetes.io/master
        operator: Exists
        effect: NoSchedule
      containers:
      - name: fluentd
        image: fluentd:v1.14
```

</details>

### Question 2.4 - Static Pod

Create a static pod named `static-nginx` using image `nginx` on node `node01`.

<details>
<summary>Show Solution</summary>

```bash
# SSH to node01
ssh node01

# Find static pod path
cat /var/lib/kubelet/config.yaml | grep staticPodPath
# Usually: /etc/kubernetes/manifests

# Create static pod manifest
cat <<EOF > /etc/kubernetes/manifests/static-nginx.yaml
apiVersion: v1
kind: Pod
metadata:
  name: static-nginx
spec:
  containers:
  - name: nginx
    image: nginx
EOF
```

</details>

---

## Section 3: Services & Networking (20%)

### Question 3.1 - Create Service

Create a deployment named `web` with image `nginx:1.21` and 3 replicas. Expose it using a NodePort service on port 30080.

<details>
<summary>Show Solution</summary>

```bash
# Create deployment
kubectl create deployment web --image=nginx:1.21 --replicas=3

# Expose as NodePort
kubectl expose deployment web --port=80 --type=NodePort --name=web-service

# Or with specific nodePort:
kubectl create service nodeport web-service --tcp=80:80 --node-port=30080
# Then patch selector if needed
```

</details>

### Question 3.2 - Network Policy

Create a NetworkPolicy named `deny-all` in namespace `secure` that denies all ingress traffic to pods in that namespace.

<details>
<summary>Show Solution</summary>

```bash
kubectl create namespace secure
```

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: secure
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```

</details>

### Question 3.3 - Ingress

Create an Ingress named `app-ingress` that routes:
- `app.example.com/api` to service `api-svc` port 80
- `app.example.com/web` to service `web-svc` port 80

<details>
<summary>Show Solution</summary>

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-svc
            port:
              number: 80
      - path: /web
        pathType: Prefix
        backend:
          service:
            name: web-svc
            port:
              number: 80
```

</details>

### Question 3.4 - CoreDNS

A pod cannot resolve service DNS names. Troubleshoot and fix the issue.

<details>
<summary>Show Solution</summary>

```bash
# Check CoreDNS pods
kubectl get pods -n kube-system -l k8s-app=kube-dns

# Check CoreDNS logs
kubectl logs -n kube-system -l k8s-app=kube-dns

# Check CoreDNS service
kubectl get svc -n kube-system kube-dns

# Check CoreDNS ConfigMap
kubectl get configmap coredns -n kube-system -o yaml

# Test DNS from a pod
kubectl run test --image=busybox:1.36 --rm -it -- nslookup kubernetes

# If CoreDNS pods are not running, check events
kubectl describe pods -n kube-system -l k8s-app=kube-dns

# Restart CoreDNS if needed
kubectl rollout restart deployment coredns -n kube-system
```

</details>

---

## Section 4: Storage (10%)

### Question 4.1 - PersistentVolume and PVC

Create a PersistentVolume named `pv-data` with 1Gi storage using hostPath `/data`. Then create a PVC named `pvc-data` that requests 500Mi.

<details>
<summary>Show Solution</summary>

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-data
spec:
  capacity:
    storage: 1Gi
  accessModes:
  - ReadWriteOnce
  hostPath:
    path: /data
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-data
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
```

</details>

### Question 4.2 - Pod with PVC

Create a pod named `data-pod` using image `nginx` that mounts the PVC `pvc-data` at `/usr/share/nginx/html`.

<details>
<summary>Show Solution</summary>

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: data-pod
spec:
  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: data
      mountPath: /usr/share/nginx/html
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: pvc-data
```

</details>

---

## Section 5: Troubleshooting (30%)

### Question 5.1 - Pod Troubleshooting

A pod named `broken-pod` in namespace `default` is not running. Identify and fix the issue.

<details>
<summary>Show Solution</summary>

```bash
# Check pod status
kubectl get pod broken-pod

# Check events and details
kubectl describe pod broken-pod

# Common issues to look for:
# - ImagePullBackOff: Check image name, pull secrets
# - CrashLoopBackOff: Check logs
# - Pending: Check node resources, taints, affinity

# Check logs
kubectl logs broken-pod
kubectl logs broken-pod --previous

# If image issue, fix the image
kubectl set image pod/broken-pod <container>=<correct-image>

# Or edit the pod
kubectl edit pod broken-pod
```

</details>

### Question 5.2 - Node Troubleshooting

Node `node01` is in NotReady state. Troubleshoot and fix.

<details>
<summary>Show Solution</summary>

```bash
# Check node status
kubectl describe node node01

# SSH to the node
ssh node01

# Check kubelet status
sudo systemctl status kubelet

# Check kubelet logs
sudo journalctl -u kubelet -f

# Common fixes:
# Start kubelet if stopped
sudo systemctl start kubelet
sudo systemctl enable kubelet

# Check container runtime
sudo systemctl status containerd
sudo systemctl start containerd

# Check disk space
df -h

# Check memory
free -m
```

</details>

### Question 5.3 - Service Troubleshooting

A service named `web-svc` is not routing traffic to pods. Troubleshoot.

<details>
<summary>Show Solution</summary>

```bash
# Check service
kubectl get svc web-svc
kubectl describe svc web-svc

# Check endpoints
kubectl get endpoints web-svc

# If no endpoints, check:
# 1. Pod labels match service selector
kubectl get pods --show-labels
kubectl get svc web-svc -o yaml | grep selector -A 5

# 2. Pods are running
kubectl get pods -l <selector>

# 3. Pod ports match targetPort
kubectl get pods -o yaml | grep containerPort

# Fix selector if needed
kubectl patch svc web-svc -p '{"spec":{"selector":{"app":"correct-label"}}}'
```

</details>

### Question 5.4 - Control Plane Troubleshooting

The API server is not responding. Troubleshoot.

<details>
<summary>Show Solution</summary>

```bash
# Check if API server pod is running
sudo crictl ps | grep kube-apiserver

# Check static pod manifest
sudo cat /etc/kubernetes/manifests/kube-apiserver.yaml

# Check API server logs
sudo crictl logs <container-id>

# Or check kubelet logs for static pod issues
sudo journalctl -u kubelet | grep apiserver

# Common issues:
# - Certificate expired: kubeadm certs renew all
# - Wrong configuration in manifest
# - etcd not accessible

# Check etcd
sudo crictl ps | grep etcd
ETCDCTL_API=3 etcdctl endpoint health \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```

</details>

### Question 5.5 - Application Logs

View the logs of pod `app-pod` container `sidecar` from the last hour.

<details>
<summary>Show Solution</summary>

```bash
kubectl logs app-pod -c sidecar --since=1h
```

</details>

---

## Exam Tips

1. **Use aliases**: `alias k=kubectl`
2. **Enable auto-completion**: `source <(kubectl completion bash)`
3. **Use `--dry-run=client -o yaml`** to generate YAML templates
4. **Bookmark important docs** before the exam
5. **Practice on [Killercoda](https://killercoda.com/cka)** for free hands-on scenarios
6. **Focus on troubleshooting** - it's 30% of the exam
7. **Know etcd backup/restore** commands
8. **Practice cluster upgrades** with kubeadm

## Additional Practice

- [Killercoda CKA Scenarios](https://killercoda.com/cka) - Free interactive scenarios
- [killer.sh](https://killer.sh/cka) - Exam simulator (included with registration)
- [Kubernetes Documentation](https://kubernetes.io/docs/) - Allowed during exam

---

[← Back to CKA Overview](./README.md)
