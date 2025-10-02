
# Performance Calculations — Backend Architecture Task

---

## Company A — Real-time Chat Platform

### 1. Throughput

* **Clients:** 10,000 concurrent WebSocket connections
* **Message rate:** 1–2 msg/min → 0.025 msg/s per user

[
\text{Throughput} = 10{,}000 \times 0.025 = 250 \text{ messages/sec}
]

* **DB operations per message:** 1.5

[
\text{DB ops/sec} = 250 \times 1.5 = 375
]

---

### 2. Database Connection Pool

* **Average DB latency:** 100 ms (~0.1 s)
* **In-flight DB ops:** 375 × 0.1 ≈ 38
* **Add 20% headroom:** ~50 connections

---

### 3. CPU Usage

* **CPU per message:** ~4 ms
* **Total CPU usage:** 250 × 4 ms = 1 CPU core
* **With headroom:** ~1.2 cores
* **Server cores:** 8 → sufficient

---

### 4. Latency

* Event-loop overhead: <5 ms
* Async DB + Redis pub/sub ensures <50 ms delivery
* DB writes do not block event loop

**Expected latency:** <50 ms

---

### 5. Memory Usage

* Base app: 500 MB
* WebSocket memory: 10,000 × 1 KB = 10 MB
* **Total:** 510 MB → fits server memory

---

### 6. Scalability

* Horizontal scaling via clustered event-loop processes
* Redis fan-out ensures consistency
* Linear scaling with added servers

---

### Summary Table

| Metric             | Value / Estimate           |
| ------------------ | -------------------------- |
| Messages/sec       | 250                        |
| DB ops/sec         | 375                        |
| DB connection pool | ~50 connections            |
| CPU usage          | ~1.2 cores                 |
| Memory usage       | ~510 MB                    |
| Latency            | <50 ms                     |
| Scalability        | Horizontal, linear scaling |

---

## Company B — Image Processing Service

### 1. Throughput

* **Concurrent uploads:** 50
* **Processing time per image:** 2–10 s (avg ~6 s)
* **Throughput estimate:** 50 / 6 ≈ 8.3 images/sec

---

### 2. CPU / GPU Usage

* **CPU-bound fraction:** 90%
* **Memory per image:** ~2 GB
* **Server:** 16 cores + GPU

**Concurrency limit:** based on min(CPU cores, memory, GPU capacity)

* CPU: 16 cores / 2 cores per worker → ~8 concurrent workers
* Memory: 32 GB total / 2 GB per image → 16 images max
* GPU: depends on contexts → assume 8 images concurrently

**Effective concurrency:** ~8 images processed in parallel

* Throughput: 8 images / avg 6 s ≈ 1.33 images/sec (CPU-limited)
* With GPU acceleration, can reduce processing time → throughput increases proportionally

---

### 3. Latency

* Single image processing: 2–10 s
* Queueing may add wait time if more tasks arrive
* Latency per image ≈ 6 s (avg) under normal load
* During spikes, latency increases linearly with queue length

---

### 4. Memory Usage

* Each worker: ~2 GB
* 8 workers → 16 GB
* Fits within typical 32 GB server RAM

---

### 5. Scalability

* Horizontal scaling: adding more servers or GPUs
* Task queue decouples ingestion from processing
* Linear scaling until CPU/GPU or memory limits reached

---

### Summary Table

| Metric             | Value / Estimate                  |
| ------------------ | --------------------------------- |
| Concurrency        | ~8 images at a time               |
| Throughput         | ~1.33 images/sec (CPU-limited)    |
| Processing latency | 2–10 s per image                  |
| Memory usage       | ~16 GB for 8 workers              |
| CPU usage          | ~8 cores                          |
| Scalability        | Horizontal scaling, GPU-dependent |

---

## Company C — E-commerce API Gateway

### 1. Throughput

* **Requests per second:** 1,000 RPS (up to 5x spike → 5,000 RPS)
* **Fan-out per request:** 2–10 microservices (avg ~5)
* **Total microservice calls:** 1,000 × 5 = 5,000 calls/sec (normal), 25,000 calls/sec (peak)

---

### 2. CPU Usage

* **CPU-bound fraction:** 30% (JSON parsing, aggregation)
* For 1,000 RPS: 1,000 × 30% × ~2 ms per request ≈ 0.6 CPU-core
* 4-core server → sufficient under normal load
* Peak 5,000 RPS → 3 CPU cores → still feasible with multiplexing

---

### 3. Latency

* **I/O-bound microservice calls:** 100–500 ms
* Multiplexing + connection pooling reduces socket setup overhead
* Aggregation performed asynchronously → minimal added latency
* **Expected latency:** ~100–500 ms depending on slowest microservice

---

### 4. Memory Usage

* Base application: ~1 GB
* Connection pools per microservice: negligible extra memory (~tens of MB)
* Fits 4-core, 1 GB server comfortably

---

### 5. Scalability

* Multiplexing allows thousands of concurrent fan-out requests without spawning threads
* Horizontal scaling: add servers behind load balancer
* Connection pools + HTTP/2 streams prevent socket exhaustion

---

### Summary Table

| Metric                 | Value / Estimate                       |
| ---------------------- | -------------------------------------- |
| RPS (normal/peak)      | 1,000 / 5,000                          |
| Microservice calls/sec | 5,000 / 25,000                         |
| CPU usage              | ~0.6 cores normal, ~3 cores peak       |
| Memory usage           | ~1 GB                                  |
| Latency                | 100–500 ms                             |
| Scalability            | Horizontal scaling, connection pooling |

---

