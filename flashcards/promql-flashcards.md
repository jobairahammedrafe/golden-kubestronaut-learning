# PromQL Flashcards

Quick reference flashcards for Prometheus Query Language (PCA exam).

---

## Basic Queries

### Q: What is an instant vector?

<details>
<summary>Answer</summary>

A set of time series with a single sample value at a given timestamp.

```promql
up
http_requests_total{job="api"}
```

</details>

### Q: What is a range vector?

<details>
<summary>Answer</summary>

A set of time series with a range of samples over time.

```promql
http_requests_total[5m]
http_requests_total{job="api"}[1h]
```

</details>

### Q: How to filter by label?

<details>
<summary>Answer</summary>

```promql
# Exact match
up{job="prometheus"}

# Regex match
up{job=~"prom.*"}

# Not equal
up{job!="prometheus"}

# Regex not match
up{job!~"test.*"}
```

</details>

---

## Functions

### Q: What is rate()?

<details>
<summary>Answer</summary>

Per-second average rate of increase over time range.

```promql
rate(http_requests_total[5m])
```

Best for: Alerting, slow-moving counters

</details>

### Q: What is irate()?

<details>
<summary>Answer</summary>

Instant rate using last two data points.

```promql
irate(http_requests_total[5m])
```

Best for: Volatile, fast-moving counters, graphs

</details>

### Q: What is increase()?

<details>
<summary>Answer</summary>

Total increase over time range.

```promql
increase(http_requests_total[1h])
```

Returns: Absolute increase, not per-second

</details>

### Q: What is histogram_quantile()?

<details>
<summary>Answer</summary>

Calculates quantile from histogram buckets.

```promql
# 99th percentile
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# 50th percentile (median)
histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))
```

</details>

---

## Aggregation

### Q: How to sum by label?

<details>
<summary>Answer</summary>

```promql
sum by (job) (rate(http_requests_total[5m]))

# or
sum(rate(http_requests_total[5m])) by (job)
```

</details>

### Q: How to sum without label?

<details>
<summary>Answer</summary>

```promql
sum without (instance) (rate(http_requests_total[5m]))
```

Aggregates across all instances

</details>

### Q: What aggregation operators exist?

<details>
<summary>Answer</summary>

- `sum` - Sum values
- `avg` - Average
- `min` / `max` - Minimum/Maximum
- `count` - Count elements
- `stddev` / `stdvar` - Standard deviation/variance
- `topk` / `bottomk` - Top/Bottom K elements
- `quantile` - Calculate quantile

</details>

---

## Operators

### Q: How to calculate percentage?

<details>
<summary>Answer</summary>

```promql
# Error rate percentage
100 * (
  sum(rate(http_requests_total{status=~"5.."}[5m]))
  /
  sum(rate(http_requests_total[5m]))
)
```

</details>

### Q: How to compare to past?

<details>
<summary>Answer</summary>

Use `offset`:

```promql
# Current vs 1 hour ago
rate(http_requests_total[5m]) - rate(http_requests_total[5m] offset 1h)

# Current vs 1 day ago
rate(http_requests_total[5m]) / rate(http_requests_total[5m] offset 1d)
```

</details>

### Q: What comparison operators exist?

<details>
<summary>Answer</summary>

- `==` - Equal
- `!=` - Not equal
- `>` / `<` - Greater/Less than
- `>=` / `<=` - Greater/Less than or equal

```promql
# Filter where value > 100
http_requests_total > 100

# Return 1 or 0 (bool modifier)
http_requests_total > bool 100
```

</details>

---

## Common Patterns

### Q: CPU utilization query?

<details>
<summary>Answer</summary>

```promql
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

</details>

### Q: Memory utilization query?

<details>
<summary>Answer</summary>

```promql
100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))
```

</details>

### Q: Disk usage query?

<details>
<summary>Answer</summary>

```promql
100 - (node_filesystem_avail_bytes / node_filesystem_size_bytes * 100)
```

</details>

### Q: Request latency P99?

<details>
<summary>Answer</summary>

```promql
histogram_quantile(0.99, 
  sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
)
```

</details>

---

## Recording Rules

### Q: What is a recording rule?

<details>
<summary>Answer</summary>

Pre-computed query stored as new time series:
- Improves query performance
- Simplifies complex queries
- Naming convention: `level:metric:operations`

```yaml
groups:
- name: example
  rules:
  - record: job:http_requests:rate5m
    expr: sum by (job) (rate(http_requests_total[5m]))
```

</details>

---

## Alerting Rules

### Q: What is an alerting rule?

<details>
<summary>Answer</summary>

```yaml
groups:
- name: alerts
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status="500"}[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High error rate detected"
```

</details>

### Q: What does 'for' do in alerting?

<details>
<summary>Answer</summary>

Duration the condition must be true before firing:
- Prevents flapping alerts
- Alert goes from PENDING to FIRING after duration

</details>

---

[← Back to Home](../README.md)
