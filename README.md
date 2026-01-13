# Caching
Caching is a fundamental systems design technique used to mitigate high-latency disk access and reduce network I/O in backend services. 
By storing frequently accessed or computationally expensive data in faster storage layers—typically memory—caching significantly 
reduces I/O load and disk latency on database systems such as PostgreSQL or NoSQL stores.

From a backend engineering perspective, caching is often a prerequisite for building scalable systems. Caching strategies 
can take many forms, including CDNs, in-process caches, browser-level (HTTP) caching, and distributed caches using systems like 
Redis or Memcached.

In this mini-blog, I will compare and analyze the latency for read operations under different caching setups. Our setup is 
that 

### Read Performance Comparison (Sync Version)

| Storage Layer        | Avg Latency (µs) | Throughput (ops/sec) |
|----------------------|------------------|----------------------|
| PostgreSQL (Disk)    |1051.61           | 951                  |
| PostgreSQL (Disk) w/o ORM | 828.84      | 1207                 |
| Redis (Distributed)  |152.46            | 6559                 |
| In-process Cache     |1.99              | 503180               |

Lorem, ipsum

### Read Performance Comparison (Async Version)

| Storage Layer        | Avg Latency (ms) | Throughput (ops/sec) |
|----------------------|------------------|----------------------|
| PostgreSQL (Disk)    | 1082.11          | 924                  |
| PostgreSQL (Disk) w/o ORM | 890.30      | 1123                 |
| Redis (Distributed)  | 169.87           | 5887                 |
| In-process Cache     | 1.99             | 501278               |

---

Conclusion : In real backend systems, it is really important to know how the access patterns are defined. This way, we can employ 
strategies that we are going to use in order to improve the user experience and overall health of the systems.
