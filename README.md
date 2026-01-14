# Caching Performance Analysis

Caching is a fundamental systems design technique used to mitigate high-latency disk access and reduce network I/O load in backend services. By storing frequently or recently accessed data in faster storage layers—typically memory—caching significantly reduces I/O load and disk latency on database systems such as PostgreSQL or NoSQL stores.

From a backend engineering perspective, caching is often a prerequisite for building scalable systems. Caching strategies can take many forms, including CDNs, in-process caches, browser-level (HTTP) caching, and distributed caches using systems like Redis or Memcached.

In this mini-blog, I will compare and analyze the latency for read operations under different caching setups.

## Data Model

Our setup uses a simple `User` model with the following fields:
```python
class User(Base):
    __tablename__                   = "users"
    id : Mapped[int]                = Column(Integer, primary_key=True)
    name : Mapped[str]              = Column(String)
    age : Mapped[int]               = Column(Integer)
```

The `User` model contains three columns: `id`, `name`, and `age`. This intentionally small data model allows us to focus on infrastructure overhead rather than data transfer costs.

## Benchmark Results

### Read Performance Comparison (Sync Version)

| Storage Layer                     | Avg Latency (µs) | Throughput (ops/sec) |
|-----------------------------------|------------------|----------------------|
| PostgreSQL (Disk)                 | 1051.61          | 951                  |
| PostgreSQL (Disk) w/o ORM         | 828.84           | 1207                 |
| Redis (Distributed)               | 152.46           | 6559                 |
| In-process Cache                  | 1.99             | 503,180              |

### Read Performance Comparison (Async Version)

| Storage Layer                     | Avg Latency (µs) | Throughput (ops/sec) |
|-----------------------------------|------------------|----------------------|
| PostgreSQL (Disk)                 | 1082.11          | 924                  |
| PostgreSQL (Disk) w/o ORM         | 890.30           | 1123                 |
| Redis (Distributed)               | 169.87           | 5887                 |
| In-process Cache                  | 1.99             | 501,278              |

## Key Insights

### Performance Tiers

The benchmark results reveal distinct performance tiers across different caching strategies:

1. **In-Process Cache** (~2µs latency): Provides sub-microsecond access times with throughput exceeding 500K ops/sec. This represents a ~500x improvement over direct database access.

2. **Distributed Cache (Redis)** (~150-170µs latency): Offers ~6-7x faster reads than PostgreSQL with throughput around 6K ops/sec. The network roundtrip adds overhead but provides horizontal scalability and shared state across backend services.

3. **Database with ORM** (~1050-1080µs latency): Standard PostgreSQL access through an SqlAlchemy ORM layer shows ~900-950 ops/sec throughput. The ORM abstraction adds measurable overhead.

4. **Database without ORM** (~830-890µs latency): Raw SQL queries improve throughput by ~20-30%, demonstrating the cost of object-relational mapping convenience.

### Async vs Sync Considerations

The async implementation shows minimal performance differences compared to the synchronous version for these workloads. The slight increase in latency (2-10%) suggests that async overhead is negligible for I/O-bound operations. However, async patterns become valuable when handling concurrent requests or when orchestrating multiple I/O operations.

### ORM Overhead

Comparing PostgreSQL access with and without an ORM reveals a ~20-27% performance penalty. While ORMs provide developer productivity benefits, high-throughput systems may benefit from selective use of raw SQL for critical paths.

## Practical Considerations

When designing caching strategies for production systems, consider the following:

- **Use in-process caches** for data that doesn't change often and where showing slightly outdated information is acceptable. Good examples: user profiles in small applications, or recent time records in payroll systems which is base on my experience.
- **Deploy distributed caches** (Redis/Memcached) when you need shared state across multiple application instances or when cache invalidation patterns are well-defined
- **Choose the right tool for each use case**: Use raw SQL for performance-critical paths, 
  but consider whether you need the ORM's convenience features like automatic transaction 
  management, relationship handling, and connection pooling. For simple, high-throughput 
  reads, these features may add unnecessary overhead.
- **Profile your access patterns** before implementing caching—premature optimization based on assumptions can introduce complexity without proportional benefits

## Conclusion

In real backend systems, understanding access patterns is critical to selecting appropriate caching strategies. The performance difference between storage layers can vary by orders of magnitude, directly impacting user experience and system scalability. However, the "best" caching strategy depends on your specific consistency requirements, data access patterns, deployment architecture, and operational complexity tolerance.

Effective caching is not about always choosing the fastest option—it's about matching the right caching tier to each use case's requirements while maintaining system reliability and developer productivity.

## AI Assistance

This project was developed with ~50% assistance from Claude AI for code generation and documentation. Part of my exploration into LLM-assisted development workflows. I mainly use Sonnet, can't wait what Claude Opus has to offer.
