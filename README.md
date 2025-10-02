# Backend Architecture Decision Task

## Overview

This repository contains the solution for the **Backend Architecture Decision Task**, where we analyze and recommend optimal backend architecture patterns for three different companies with varying workloads and constraints. The task includes architecture analysis, implementation sketches, and performance calculations.

**Task Duration:** 1 day (6–8 hours)
**Goal:** Recommend suitable backend architecture patterns (Single-threaded, Multi-threaded, Multiplexing) and justify decisions based on workload characteristics, latency, CPU/memory constraints, and scalability requirements.

---

## Repository Structure

```
StudentName_ArchitectureAnalysis/
│
├── analysis_report.pdf
├── performance_calculations.md
├── README.md
└── implementation_sketches/
    ├── company_a_solution.py
    ├── company_b_solution.py
    └── company_c_solution.py
```

---

## Contents

### 1. Analysis Report (`analysis_report.pdf`)

* Provides a detailed architecture recommendation for each company:

  * **Company A:** Real-time Chat Platform → Single-threaded Event Loop (clustered)
  * **Company B:** Image Processing Service → Multi-process/Worker Pool + GPU
  * **Company C:** E-commerce API Gateway → Multiplexing + Connection Pooling (HTTP/2)
* Includes:

  * Workload analysis and constraints
  * Technical justification
  * Trade-offs and alternative approaches
  * Conclusion and high-level recommendations

### 2. Implementation Sketches (`implementation_sketches/`)

Python pseudocode examples for each company, showing how the recommended architecture can be implemented:

* **Company A (`company_a_solution.py`)**

  * Event-loop handling for WebSocket messages
  * Worker threads for CPU-bound tasks
  * Redis pub/sub integration for message fan-out
* **Company B (`company_b_solution.py`)**

  * Multi-process/worker pool architecture
  * Task queue integration (RabbitMQ/Redis Streams)
  * GPU/CPU image processing tasks
* **Company C (`company_c_solution.py`)**

  * Connection pooling and multiplexing for API gateway
  * Async request handling for microservice fan-out

### 3. Performance Calculations (`performance_calculations.md`)

* Throughput, latency, CPU/memory usage, and scalability estimates for each company
* Calculations based on workload data from the task description
* Includes tables summarizing metrics for clarity

---

## How to Use

1. **Review the Analysis Report:** Understand the architecture recommendations and reasoning.
2. **Check Implementation Sketches:** Use pseudocode as a starting point for real implementation.
3. **Review Performance Calculations:** See estimated throughput, latency, CPU/memory usage, and scalability.
4. **Replicate or Extend:** Modify sketches or calculations for experimentation or deployment.

---

## Notes

* The analysis focuses on realistic trade-offs based on workload characteristics.
* No production code is included; pseudocode is for demonstration of architecture principles.
* Calculations and recommendations are made under normal and peak load assumptions.

---

## References / Real-World Context

* **WhatsApp:** Single-threaded Erlang processes for massive concurrency
* **Netflix:** Reactive programming for millions of concurrent streams
* **Instagram:** Switched from multi-threaded to async architecture for better performance
* **Cloudflare:** Extensive use of multiplexing for edge efficiency

