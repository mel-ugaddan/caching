# Caching
Caching is a fundamental systems design technique used to mitigate high-latency disk access and reduce network I/O in backend services. 
By storing frequently accessed or computationally expensive data in faster storage layers—typically memory—caching significantly 
reduces I/O load and disk latency on database systems such as PostgreSQL or NoSQL stores.

From a backend engineering perspective, caching is often a prerequisite for building scalable systems. Caching strategies 
can take many forms, including CDNs, in-process caches, browser-level (HTTP) caching, and distributed caches using systems like 
Redis or Memcached.

In this mini-blog, I will benchmark and analyze server response latency for read operations under different caching setups.


## Read Performance Comparison

| Storage Layer        | Avg Latency (ms) | Throughput (ops/sec) |
|----------------------|------------------|----------------------|
| PostgreSQL (Disk)    | 5 – 15           | 1k – 5k              |
| Redis (Distributed)  | 0.3 – 1.2        | 50k – 200k           |
| In-process Cache     | 0.01 – 0.05      | 1M+                  |

---

Conclusion : In real backend systems, it is really important to know how the access patterns are defined. This way, we can employ 
strategies that we are going to use in order to improve the user experience and overall health of the systems.
