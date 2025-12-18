# Application Observability and Maintenance (15%)

This domain covers monitoring, debugging, and maintaining applications in Kubernetes.

## Probes

### Liveness Probe

Determines if a container is running. If it fails, the container is restarted.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-with-liveness
spec:
  containers:
  - name: app
    image: myapp:v1
    livenessProbe:
      httpGet:
        path: /healthz
        port: 8080
      initialDelaySeconds: 15
      periodSeconds: 10
      timeoutSeconds: 5
      failureThreshold: 3
      successThreshold: 1
```

### Readiness Probe

Determines if a container is ready to receive traffic.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-with-readiness
spec:
  containers:
  - name: app
    image: myapp:v1
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 5
      failureThreshold: 3
```

### Startup Probe

Used for slow-starting containers. Disables liveness/readiness until it succeeds.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-with-startup
spec:
  containers:
  - name: app
    image: myapp:v1
    startupProbe:
      httpGet:
        path: /healthz
        port: 8080
      failureThreshold: 30
      periodSeconds: 10
    livenessProbe:
      httpGet:
        path: /healthz
        port: 8080
      periodSeconds: 10
```

### Probe Types

| Type | Description |
|------|-------------|
| `httpGet` | HTTP GET request to specified path and port |
| `tcpSocket` | TCP connection to specified port |
| `exec` | Execute command in container |
| `grpc` | gRPC health check |

```yaml
# TCP Socket probe
livenessProbe:
  tcpSocket:
    port: 3306
  initialDelaySeconds: 15
  periodSeconds: 10

# Exec probe
livenessProbe:
  exec:
    command:
    - cat
    - /tmp/healthy
  initialDelaySeconds: 5
  periodSeconds: 5

# gRPC probe
livenessProbe:
  grpc:
    port: 50051
  initialDelaySeconds: 10
```

### Probe Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `initialDelaySeconds` | Delay before first probe | 0 |
| `periodSeconds` | How often to probe | 10 |
| `timeoutSeconds` | Probe timeout | 1 |
| `failureThreshold` | Failures before action | 3 |
| `successThreshold` | Successes to be considered healthy | 1 |

## Logging

### Viewing Logs

```bash
# View pod logs
kubectl logs nginx

# View specific container logs
kubectl logs nginx -c sidecar

# Follow logs
kubectl logs -f nginx

# View previous container logs (after restart)
kubectl logs nginx --previous

# View last N lines
kubectl logs nginx --tail=100

# View logs since time
kubectl logs nginx --since=1h
kubectl logs nginx --since-time=2024-01-01T00:00:00Z

# View logs from all pods with label
kubectl logs -l app=nginx

# View logs from all containers in pod
kubectl logs nginx --all-containers
```

### Logging Architecture

```text
┌─────────────────────────────────────────────────────┐
│                     Node                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │    Pod 1    │  │    Pod 2    │  │    Pod 3    │  │
│  │  stdout/err │  │  stdout/err │  │  stdout/err │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  │
│         │                │                │          │
│         └────────────────┼────────────────┘          │
│                          │                           │
│                    ┌─────▼─────┐                     │
│                    │ Container │                     │
│                    │  Runtime  │                     │
│                    └─────┬─────┘                     │
│                          │                           │
│                    ┌─────▼─────┐                     │
│                    │ Log Files │                     │
│                    │/var/log/  │                     │
│                    └───────────┘                     │
└─────────────────────────────────────────────────────┘
```

## Debugging

### Debug Commands

```bash
# Describe pod (events, status)
kubectl describe pod nginx

# Get pod details
kubectl get pod nginx -o yaml
kubectl get pod nginx -o wide

# Check events
kubectl get events --sort-by='.lastTimestamp'
kubectl get events --field-selector involvedObject.name=nginx

# Execute command in container
kubectl exec nginx -- ls /app
kubectl exec -it nginx -- /bin/sh

# Copy files to/from container
kubectl cp nginx:/var/log/app.log ./app.log
kubectl cp ./config.yaml nginx:/app/config.yaml

# Port forward
kubectl port-forward pod/nginx 8080:80
kubectl port-forward svc/nginx 8080:80

# Debug with ephemeral container
kubectl debug nginx -it --image=busybox --target=nginx
```

### Common Issues

| Issue | Debug Steps |
|-------|-------------|
| **ImagePullBackOff** | Check image name, registry access, pull secrets |
| **CrashLoopBackOff** | Check logs, probe configuration, resource limits |
| **Pending** | Check events, node resources, taints/tolerations |
| **OOMKilled** | Increase memory limits |
| **CreateContainerConfigError** | Check ConfigMaps, Secrets references |

### Pod Status Phases

| Phase | Description |
|-------|-------------|
| `Pending` | Pod accepted but not running |
| `Running` | Pod bound to node, containers running |
| `Succeeded` | All containers terminated successfully |
| `Failed` | All containers terminated, at least one failed |
| `Unknown` | Pod state cannot be determined |

## Monitoring

### Resource Metrics

```bash
# View node resource usage
kubectl top nodes

# View pod resource usage
kubectl top pods
kubectl top pods -A
kubectl top pods --containers

# Sort by CPU/memory
kubectl top pods --sort-by=cpu
kubectl top pods --sort-by=memory
```

### Metrics Server

Required for `kubectl top` commands:

```bash
# Check if metrics server is running
kubectl get pods -n kube-system | grep metrics-server

# Install metrics server (if needed)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

## Application Maintenance

### Updating Applications

```bash
# Update image
kubectl set image deployment/nginx nginx=nginx:1.22

# Update environment variable
kubectl set env deployment/nginx ENV=production

# Update resources
kubectl set resources deployment/nginx --limits=cpu=200m,memory=512Mi

# Patch resource
kubectl patch deployment nginx -p '{"spec":{"replicas":5}}'
```

### Scaling

```bash
# Manual scaling
kubectl scale deployment nginx --replicas=5

# Autoscaling
kubectl autoscale deployment nginx --min=2 --max=10 --cpu-percent=80
```

### HorizontalPodAutoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Key Concepts to Remember

1. **Liveness** - Is the container running? Restart if not
2. **Readiness** - Is the container ready for traffic?
3. **Startup** - For slow-starting containers
4. **kubectl logs** - View container output
5. **kubectl describe** - Detailed resource info with events
6. **kubectl top** - Resource usage (requires metrics-server)

## Practice Questions

1. What happens when a liveness probe fails?
2. How do you view logs from a previous container instance?
3. What is the difference between readiness and liveness probes?
4. How do you execute a command in a running container?
5. What probe type would you use for a database container?

---

[← Previous: Application Deployment](./02-application-deployment.md) | [Back to CKAD Overview](./README.md) | [Next: Application Environment, Configuration and Security →](./04-application-environment-config-security.md)
