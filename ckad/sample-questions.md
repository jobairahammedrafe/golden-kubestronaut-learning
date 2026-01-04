# CKAD Sample Practice Questions

<div class="pdf-download">
  <a href="/pdf/sample-questions.pdf" class="md-button md-button--primary" download>
    <span class="twemoji">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M5 20h14v-2H5v2zM19 9h-4V3H9v6H5l7 7 7-7z"></path></svg>
    </span>
    Download PDF Version
  </a>
</div>



> **Disclaimer**: These are sample practice questions created for study purposes only. They are NOT actual exam questions and are designed to help you test your understanding of CKAD concepts. Real exam questions may differ in format and content.

## Practice Resources

Before attempting these questions, we highly recommend practicing on:

- **[Killercoda CKAD Scenarios](https://killercoda.com/ckad)** ⭐ Free hands-on practice environments
- **[killer.sh CKAD Simulator](https://killer.sh/ckad)** - Included with exam registration

## Instructions

- The CKAD exam is **performance-based** (hands-on), not multiple choice
- Practice these scenarios in a real Kubernetes cluster
- Time yourself - aim for efficiency
- Use imperative commands when possible to save time

---

## Section 1: Application Design and Build (20%)

### Question 1.1 - Create a Job

Create a Job named `pi-calculator` that:
- Uses the image `perl:5.34`
- Runs the command `perl -Mbignum=bpi -wle 'print bpi(2000)'`
- Completes 3 times successfully
- Runs 2 pods in parallel
- Has a backoff limit of 4

<details>
<summary>Show Solution</summary>

```bash
# Generate base YAML
kubectl create job pi-calculator --image=perl:5.34 --dry-run=client -o yaml -- perl -Mbignum=bpi -wle 'print bpi(2000)' > job.yaml

# Edit to add completions, parallelism, backoffLimit
```

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi-calculator
spec:
  completions: 3
  parallelism: 2
  backoffLimit: 4
  template:
    spec:
      containers:
      - name: pi-calculator
        image: perl:5.34
        command: ["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
```

```bash
kubectl apply -f job.yaml
```

</details>

### Question 1.2 - Create a CronJob

Create a CronJob named `backup-job` that:
- Runs every day at 2:30 AM
- Uses image `busybox:1.36`
- Runs command `echo "Backup completed at $(date)"`
- Keeps 3 successful job history
- Keeps 1 failed job history

<details>
<summary>Show Solution</summary>

```bash
kubectl create cronjob backup-job --image=busybox:1.36 --schedule="30 2 * * *" -- /bin/sh -c 'echo "Backup completed at $(date)"'

# Or with YAML for history limits:
```

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-job
spec:
  schedule: "30 2 * * *"
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: busybox:1.36
            command: ["/bin/sh", "-c", "echo \"Backup completed at $(date)\""]
          restartPolicy: OnFailure
```

</details>

### Question 1.3 - Multi-Container Pod

Create a Pod named `app-with-sidecar` with:
- Main container: `nginx:1.21` named `main-app`
- Sidecar container: `busybox:1.36` named `log-agent` that runs `tail -f /var/log/nginx/access.log`
- Both containers share a volume mounted at `/var/log/nginx`

<details>
<summary>Show Solution</summary>

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-with-sidecar
spec:
  containers:
  - name: main-app
    image: nginx:1.21
    volumeMounts:
    - name: logs
      mountPath: /var/log/nginx
  - name: log-agent
    image: busybox:1.36
    command: ["tail", "-f", "/var/log/nginx/access.log"]
    volumeMounts:
    - name: logs
      mountPath: /var/log/nginx
  volumes:
  - name: logs
    emptyDir: {}
```

</details>

---

## Section 2: Application Deployment (20%)

### Question 2.1 - Create and Scale Deployment

1. Create a Deployment named `web-app` with image `nginx:1.21` and 3 replicas
2. Update the image to `nginx:1.22`
3. Check the rollout status
4. Rollback to the previous version

<details>
<summary>Show Solution</summary>

```bash
# Create deployment
kubectl create deployment web-app --image=nginx:1.21 --replicas=3

# Update image
kubectl set image deployment/web-app nginx=nginx:1.22

# Check rollout status
kubectl rollout status deployment/web-app

# View history
kubectl rollout history deployment/web-app

# Rollback
kubectl rollout undo deployment/web-app
```

</details>

### Question 2.2 - Deployment Strategy

Create a Deployment named `rolling-app` with:
- Image: `nginx:1.21`
- 4 replicas
- Rolling update strategy with maxSurge=1 and maxUnavailable=1

<details>
<summary>Show Solution</summary>

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rolling-app
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  selector:
    matchLabels:
      app: rolling-app
  template:
    metadata:
      labels:
        app: rolling-app
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
```

</details>

### Question 2.3 - Helm Operations

1. Add the bitnami repository
2. Search for nginx chart
3. Install nginx chart with release name `my-nginx`
4. List all releases
5. Uninstall the release

<details>
<summary>Show Solution</summary>

```bash
# Add repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Search
helm search repo nginx

# Install
helm install my-nginx bitnami/nginx

# List releases
helm list

# Uninstall
helm uninstall my-nginx
```

</details>

---

## Section 3: Application Observability and Maintenance (15%)

### Question 3.1 - Configure Probes

Create a Pod named `health-check-pod` with:
- Image: `nginx:1.21`
- Liveness probe: HTTP GET on path `/` port 80, initial delay 10s, period 5s
- Readiness probe: HTTP GET on path `/` port 80, initial delay 5s, period 3s

<details>
<summary>Show Solution</summary>

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: health-check-pod
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
    livenessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 10
      periodSeconds: 5
    readinessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 3
```

</details>

### Question 3.2 - Debugging

A Pod named `broken-pod` is not running correctly. Debug and fix it.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: broken-pod
spec:
  containers:
  - name: app
    image: nginx:latest
    command: ["nginx", "-g", "daemon off;"]
    resources:
      limits:
        memory: "10Mi"
```

<details>
<summary>Show Solution</summary>

```bash
# Check pod status
kubectl get pod broken-pod

# Check events and details
kubectl describe pod broken-pod

# Check logs
kubectl logs broken-pod

# The issue is likely OOMKilled due to low memory limit
# Fix by increasing memory limit:
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: broken-pod
spec:
  containers:
  - name: app
    image: nginx:latest
    resources:
      limits:
        memory: "128Mi"
```

</details>

### Question 3.3 - View Logs

1. View logs of pod `nginx` in namespace `web`
2. View logs of the previous container instance
3. Follow logs in real-time
4. View last 50 lines

<details>
<summary>Show Solution</summary>

```bash
# View logs
kubectl logs nginx -n web

# Previous container
kubectl logs nginx -n web --previous

# Follow logs
kubectl logs -f nginx -n web

# Last 50 lines
kubectl logs nginx -n web --tail=50
```

</details>

---

## Section 4: Application Environment, Configuration and Security (25%)

### Question 4.1 - ConfigMap and Secret

1. Create a ConfigMap named `app-config` with:
   - `APP_ENV=production`
   - `LOG_LEVEL=info`

2. Create a Secret named `db-secret` with:
   - `DB_USER=admin`
   - `DB_PASS=secret123`

3. Create a Pod that uses both as environment variables

<details>
<summary>Show Solution</summary>

```bash
# Create ConfigMap
kubectl create configmap app-config --from-literal=APP_ENV=production --from-literal=LOG_LEVEL=info

# Create Secret
kubectl create secret generic db-secret --from-literal=DB_USER=admin --from-literal=DB_PASS=secret123
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  containers:
  - name: app
    image: nginx:1.21
    envFrom:
    - configMapRef:
        name: app-config
    - secretRef:
        name: db-secret
```

</details>

### Question 4.2 - Security Context

Create a Pod named `secure-pod` that:
- Runs as user ID 1000
- Runs as group ID 3000
- Has a read-only root filesystem
- Cannot escalate privileges

<details>
<summary>Show Solution</summary>

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
  containers:
  - name: app
    image: nginx:1.21
    securityContext:
      readOnlyRootFilesystem: true
      allowPrivilegeEscalation: false
```

</details>

### Question 4.3 - Resource Limits

Create a Pod named `resource-pod` with:
- Image: `nginx:1.21`
- CPU request: 100m, limit: 200m
- Memory request: 64Mi, limit: 128Mi

<details>
<summary>Show Solution</summary>

```bash
kubectl run resource-pod --image=nginx:1.21 --dry-run=client -o yaml > pod.yaml
# Edit to add resources
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-pod
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    resources:
      requests:
        cpu: "100m"
        memory: "64Mi"
      limits:
        cpu: "200m"
        memory: "128Mi"
```

</details>

---

## Section 5: Services and Networking (20%)

### Question 5.1 - Create Services

1. Create a Deployment named `web` with image `nginx:1.21` and 3 replicas
2. Expose it as a ClusterIP Service on port 80
3. Expose it as a NodePort Service on port 30080

<details>
<summary>Show Solution</summary>

```bash
# Create deployment
kubectl create deployment web --image=nginx:1.21 --replicas=3

# ClusterIP service
kubectl expose deployment web --port=80 --target-port=80 --name=web-clusterip

# NodePort service
kubectl expose deployment web --port=80 --target-port=80 --type=NodePort --name=web-nodeport

# Or specify nodePort:
kubectl create service nodeport web-nodeport --tcp=80:80 --node-port=30080
```

</details>

### Question 5.2 - Network Policy

Create a NetworkPolicy named `api-policy` in namespace `default` that:
- Applies to pods with label `app=api`
- Allows ingress only from pods with label `app=frontend`
- Allows ingress only on port 8080

<details>
<summary>Show Solution</summary>

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

</details>

### Question 5.3 - Ingress

Create an Ingress named `web-ingress` that:
- Routes `app.example.com/api` to service `api-service` port 80
- Routes `app.example.com/web` to service `web-service` port 80
- Uses ingress class `nginx`

<details>
<summary>Show Solution</summary>

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
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
            name: api-service
            port:
              number: 80
      - path: /web
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

</details>

---

## Exam Tips

1. **Use aliases**: `alias k=kubectl`
2. **Enable auto-completion**: `source <(kubectl completion bash)`
3. **Use `--dry-run=client -o yaml`** to generate YAML templates
4. **Bookmark important docs** before the exam
5. **Practice on [Killercoda](https://killercoda.com/ckad)** for free hands-on scenarios
6. **Time management**: Don't spend too long on any single question
7. **Use imperative commands** when possible to save time

## Additional Practice

- [Killercoda CKAD Scenarios](https://killercoda.com/ckad) - Free interactive scenarios
- [killer.sh](https://killer.sh/ckad) - Exam simulator (included with registration)
- [Kubernetes Documentation](https://kubernetes.io/docs/) - Allowed during exam

---

[← Back to CKAD Overview](./README.md)
