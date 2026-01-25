# Service Standard Contract

This document defines the standard structure and conventions for all backend microservices.

---

## 1. Root Structure

```
service_<name>/
├── .dockerignore          # Files to exclude from Docker builds
├── .env                   # Environment variables (not committed to git)
├── Dockerfile             # Container definition
├── README.md              # Service overview and setup instructions
├── pyproject.toml         # Dependencies, tool configs (pytest, mypy, ruff)
├── docs/                  # Service documentation (legal-binding detail level)
├── scripts/               # Local development helper scripts
└── src/                   # Source code
    ├── __init__.py
    ├── main.py            # FastAPI app entry point
    ├── startup.py         # Pre-startup initialization (env loading, etc.)
    ├── api/               # Service boundary - all external communication
    ├── config/            # Configuration & infrastructure connections
    ├── service_layer/     # Business logic
    ├── data_repositories/ # CRUD operations per data store
    ├── data_models/       # Pydantic models & database schemas
    ├── event_broker/      # Kafka integration (if applicable)
    ├── utils/             # Shared utilities
    └── tests/             # Test files
```

---

## 2. `docs/` - Service Documentation

Serves as a centralized, legally-binding documentation source. Content should enable generation of full compliance reports covering design, architecture, capabilities, features, and boundaries.

```
docs/
├── api/              # OpenAPI specs, endpoint contracts, request/response schemas
├── architecture/     # System design, UML diagrams, component boundaries, data flow
├── compliance/       # GDPR, AI-Act, data handling policies, audit requirements
├── security/         # Auth flows, threat models, access control, encryption
├── data/             # Data models, lineage, transformations (traceability)
├── features/         # Service capabilities, feature specs, business logic docs
└── decisions/        # ADRs (Architecture Decision Records) - the "why" behind choices
```

---

## 3. `scripts/` - Local Development Helpers

Scripts for local development workflow only. Not for production use.

Examples:
- `reset_schema.sh` - Reset and seed database for local development
- `run_local.sh` - Start service locally outside Docker

---

## 4. `src/main.py` and `src/startup.py` - Application Entry Points

### 4.1 `main.py` - FastAPI Application

**Purpose:** Define and configure the FastAPI application instance.

**Allowed:**
- FastAPI app instantiation
- Router registration
- Middleware registration
- Lifespan event handlers (startup/shutdown)
- OpenAPI configuration

**Not allowed:**
- Business logic
- Direct database calls
- Environment variable loading (belongs in `startup.py`)

### 4.2 `startup.py` - Pre-Startup Initialization

**Purpose:** Initialize environment and validate configuration before the app starts.

**Allowed:**
- Environment variable loading (dotenv)
- Configuration validation
- Early logging setup
- Pre-flight checks (database connectivity, required services)

**Not allowed:**
- Business logic
- Request handling
- Route definitions

---

## 5. `src/api/` - Service Boundary

The single point of contact for all external communication (inbound and outbound).

```
api/
├── routes/           # Inbound - FastAPI endpoint handlers
├── paths.py          # Route path constants (single source of truth)
├── schemas/          # Request/Response Pydantic models (API contracts)
├── dependencies/     # FastAPI Depends() functions
├── middleware/       # Custom middleware (CORS, logging, auth)
└── clients/          # Outbound - HTTP clients for external services
```

### 5.1 `api/paths.py` - Route Path Constants

**Purpose:** Single source of truth for all route paths. Enables easy debugging and one-place changes.

**Allowed:**
- Route prefix constants
- Route path constants (static segments)
- Path parameter patterns

**Not allowed:**
- Business logic
- Route handler functions
- Pydantic models

**Naming convention:** Classes named `<Feature>Routes` with uppercase constants.

---

### 5.2 `api/routes/` - Endpoint Handlers

**Purpose:** FastAPI endpoint handlers. The entry point for all HTTP requests.

**Allowed:**
- FastAPI `APIRouter` instances
- Endpoint functions decorated with `@router.get`, `@router.post`, etc.
- Dependency injection via `Depends()`
- HTTP-level concerns: status codes, headers, HTTPException

**Not allowed:**
- Business logic (delegate to `service_layer/`)
- Direct database calls (use dependencies to inject services)
- Pydantic model definitions (belong in `schemas/`)
- Hardcoded route paths (use `paths.py`)

**Naming convention:** `routes_<feature>.py`

---

### 5.3 `api/schemas/` - API Contracts

**Purpose:** Pydantic models defining the API contract. These are the PUBLIC interface.

**Allowed:**
- Request models (what clients send)
- Response models (what clients receive)
- Enums used in requests/responses
- Field validators specific to API validation

**Not allowed:**
- Database ORM models (belong in `data_models/`)
- Internal data structures not exposed via API
- Business logic

**Naming convention:** `<feature>_schemas.py`

---

### 5.4 `api/dependencies/` - Dependency Injection

**Purpose:** FastAPI `Depends()` functions that wire up services, connections, and auth.

**Allowed:**
- Functions that return service instances
- Functions that return database sessions
- Authentication/authorization checks
- Request-scoped resource management

**Not allowed:**
- Business logic
- Direct database queries
- Endpoint definitions

**Naming convention:** `<resource>_deps.py` or `deps.py` for small services

---

### 5.5 `api/middleware/` - Request/Response Interceptors

**Purpose:** Middleware applied globally or to route groups.

**Allowed:**
- CORS configuration
- Request logging
- Authentication middleware
- Rate limiting
- Request ID injection
- Error handling wrappers

**Not allowed:**
- Business logic
- Feature-specific logic (use dependencies instead)

**Naming convention:** `<concern>_middleware.py`

---

### 5.6 `api/clients/` - Outbound HTTP Clients

**Purpose:** HTTP/SDK clients for calling external services or suppliers. Handles the transport layer only.

**Allowed:**
- HTTP client wrappers (httpx, aiohttp)
- SDK initializations for third-party services
- Request/response transformation for external APIs
- Retry logic, timeout configuration
- Circuit breaker patterns

**Not allowed:**
- Business logic about what to do with responses (belongs in `service_layer/`)
- Internal service calls within same codebase

**Naming convention:** `<service>_client.py`

**Relationship with other directories:**

| Concern | Location |
|---------|----------|
| Client implementation (HTTP calls) | `api/clients/` |
| Request/response schemas for external APIs | `data_models/external_apis/` |
| Connection configuration (base URLs, timeouts) | `config/connections/` |

---

## 6. `src/data_repositories/` - Data Access Layer

Pure CRUD operations for each data store. No business logic.

```
data_repositories/
├── __init__.py
├── minio_repository.py       # File storage operations
├── postgres_repository.py    # Relational database operations
├── qdrant_repository.py      # Vector database operations
└── neo4j_repository.py       # Graph database operations (if needed)
```

**Purpose:** Isolate all data store interactions. Each repository handles one data store.

**Allowed:**
- CRUD operations (Create, Read, Update, Delete)
- Query building and execution
- Data store-specific error handling
- Connection management via injected connection objects

**Not allowed:**
- Business logic (belongs in `service_layer/`)
- Cross-repository operations (orchestrate in `service_layer/`)
- Direct instantiation of connections (inject via `__init__`)
- API schemas (use internal types or `data_models/`)
- Domain-specific mappings (e.g., logical bucket names to physical names)

**Naming convention:** `<store>_repository.py` (named after the **data store**, not the entity)

**Multiple repositories per file:** Allowed if they share the same data store (e.g., `CorrectionRepository` and `JobListingRepository` in `postgres_repository.py`).

---

## 7. `src/data_models/` - Data Structures & Schemas

Defines all data structures using Pydantic models for validation and SQLAlchemy ORM for table definitions. This is where you declare **what** data looks like - not how to store or retrieve it.

**Core principle:** Every data boundary has a Pydantic model. Data enters validated, exits validated. No exceptions.

```
data_models/
├── __init__.py
├── databases/                   # Relational databases (ORM + Pydantic)
│   └── postgres/
│       ├── corrections.py       # CorrectionORM + CorrectionItem
│       ├── job_listings.py      # JobListingORM + JobListingItem
│       └── *.sql                # SQL scripts for table setup/seeding
├── vector_stores/               # Vector databases (Pydantic only)
│   └── qdrant/
│       └── embeddings.py        # Embedding payload schemas
├── object_storage/              # File/blob storage (Pydantic only)
│   └── minio/
│       └── files.py             # File metadata validation
├── cache/                       # In-memory stores (Pydantic only)
│   └── redis/
│       └── sessions.py          # Cache entry schemas
├── external_apis/               # Third-party services (Pydantic only)
│   └── <provider>/
│       └── <provider>.py        # API payload validation
└── events/                      # Message broker schemas (Pydantic only)
    └── kafka/
        └── <event>_event.py     # Event contract definitions
```

**Purpose:** Single source of truth for all data structures. Separates "what data looks like" from "how to access it" (repositories) and "what to do with it" (service layer).

**Allowed:**
- Pydantic `BaseModel` classes for data validation (mandatory for all boundaries)
- SQLAlchemy ORM model classes (only in `databases/`)
- Python `Enum` classes for constrained values
- SQL scripts for table creation and seeding (only in `databases/`)
- Type aliases and custom types

**Not allowed:**
- CRUD operations (belongs in `data_repositories/`)
- Business logic (belongs in `service_layer/`)
- API request/response schemas (belongs in `api/schemas/`)
- Connection handling (belongs in `config/`)

**Naming convention:** `<entity>.py` (e.g., `corrections.py`, `embeddings.py`, `files.py`)

### 7.1 Directory Categories

| Directory | Contains ORM? | Purpose |
|-----------|---------------|---------|
| `databases/` | Yes | Relational DB table definitions + Pydantic validation |
| `vector_stores/` | No | Vector payload schemas for similarity search |
| `object_storage/` | No | File metadata validation before storage operations |
| `cache/` | No | Cache entry schemas for serialization |
| `external_apis/` | No | Request/response validation for third-party APIs |
| `events/` | No | Message contracts for event-driven communication |

### 7.2 Database Models (ORM + Pydantic)

Only `databases/` contains SQLAlchemy ORM because only relational databases have tables. Combine ORM and Pydantic in the same file per entity.

**File structure:** Each file contains:
1. Enum classes for constrained values
2. SQLAlchemy ORM class (table definition)
3. Pydantic model class (data validation)

### 7.3 Non-Database Models (Pydantic Only)

All other categories (`object_storage/`, `vector_stores/`, `cache/`, `external_apis/`, `events/`) contain only Pydantic models for validation—no ORM.

---

## 8. `src/service_layer/` - Business Logic

Contains domain-aware business logic that orchestrates repositories and applies business rules. This is where you implement **what** the service does.

```
service_layer/
├── file_service.py           # File upload orchestration
├── correction_service.py     # Corrections business logic
├── joblisting_service.py     # Job listings business logic
├── embedding_service.py      # Text extraction + vector embedding
└── <feature>_service.py      # One service per domain feature
```

**Purpose:** Orchestrate data operations, apply business rules, transform between layers. The "brain" of the service.

**Allowed:**
- Orchestration across multiple repositories
- Business rule validation and decisions
- Data transformation (ORM → Pydantic, aggregations)
- Domain-specific mappings (e.g., logical bucket names to physical bucket names)
- Domain-specific utilities (e.g., text extraction for embedding)
- Calls to `api/clients/` for external services

**Not allowed:**
- Direct database/store connections (inject repositories)
- HTTP handling (belongs in `api/routes/`)
- Generic utilities with no domain knowledge (belongs in `utils/`)

**Naming convention:** `<feature>_service.py`

### 8.1 Service Layer vs Utils Boundary

| Aspect | `service_layer/` | `utils/` |
|--------|------------------|----------|
| **Domain knowledge** | Yes - knows business context | No - domain-agnostic |
| **Dependencies** | Uses repositories, clients | No service dependencies |
| **State** | Stateful (holds repo refs) | Stateless (pure functions) |
| **Reusability** | Specific to THIS service | Copy-paste to ANY project |

**Rule of thumb:** If it knows about "cover letters", "job listings", or other domain concepts → `service_layer/`. If it's generic (date formatting, string utils) → `utils/`.

---

## 9. `src/config/` - Service Configuration

Defines how the service is configured: environment settings, infrastructure connections, and operational parameters.

```
config/
├── __init__.py
├── settings.py                  # Pydantic BaseSettings - loads environment variables
├── logging_config.py            # Log levels, formatters, handlers (optional)
└── connections/                 # Infrastructure connection classes
    ├── __init__.py
    ├── postgres_connection.py   # PostgreSQL client setup
    ├── minio_connection.py      # MinIO/S3 client setup
    ├── qdrant_connection.py     # Vector DB client setup
    ├── kafka_connection.py      # Message broker setup
    └── redis_connection.py      # Cache client setup
```

### 9.1 `settings.py` - Environment Configuration

**Purpose:** Single source of truth for all environment variables. Uses Pydantic `BaseSettings` to load and validate configuration from `.env` files.

**Allowed:**
- Environment variable definitions with types and defaults
- Computed properties (e.g., constructing URLs from host/port)
- Environment-specific settings (dev/prod/test)
- Validation rules for configuration values

**Not allowed:**
- Connection instantiation (belongs in `connections/`)
- Business logic
- Hardcoded secrets (must come from environment)

**Naming convention:** `settings.py` or `<service>_settings.py`

### 9.2 `connections/` - Infrastructure Connections

**Purpose:** Initialize and manage connections to external infrastructure (databases, storage, message brokers). Each connection class encapsulates client setup, validation, and lifecycle management.

**Allowed:**
- Client initialization using settings from `settings.py`
- Connection validation (health checks on startup)
- Singleton patterns for connection reuse
- Lazy initialization for performance
- Connection pooling configuration

**Not allowed:**
- CRUD operations (belongs in `data_repositories/`)
- Business logic
- Direct environment variable access (use `settings.py`)

**Naming convention:** `<infrastructure>_connection.py` with class named `<Infrastructure>Connection` (e.g., `MinioConnection`, `PostgresConnection`)

### 9.3 Connection Categories

| Category | Description | Examples | `data_models/` location |
|----------|-------------|----------|------------------------|
| **Databases** | Relational and NoSQL databases | PostgreSQL, MongoDB, Neo4j | `databases/` |
| **Vector stores** | Embedding/similarity search | Qdrant, Pinecone, Weaviate | `vector_stores/` |
| **Object storage** | File/blob storage | MinIO, AWS S3, Azure Blob | `object_storage/` |
| **Cache** | In-memory data stores | Redis, Memcached | `cache/` |
| **External APIs** | Third-party service clients | OpenAI, SendGrid, Stripe | `external_apis/` |
| **Message brokers** | Event streaming and queues | Kafka, RabbitMQ | `events/` |

### 9.4 Optional Configuration Files

Additional configuration files may be added as needed:

| File | Purpose |
|------|---------|
| `logging_config.py` | Log levels, formatters, handlers |
| `feature_flags.py` | Enable/disable features per environment |
| `security_config.py` | CORS, rate limits, auth settings |
| `monitoring_config.py` | Prometheus, tracing, alerting |

---

## 10. `src/event_broker/` - Event-Driven Messaging

Handles asynchronous communication via message brokers (Kafka, RabbitMQ, etc.). Contains producers that send events and consumers that react to events.

```
event_broker/
├── __init__.py
├── producers/                   # Outbound - publish events
│   └── <event>_producer.py
└── consumers/                   # Inbound - listen and react to events
    └── <event>_consumer.py
```

### 10.1 `producers/` - Event Publishers

**Purpose:** Send events to message broker topics when something happens in this service.

**Allowed:**
- Kafka/RabbitMQ producer classes
- Event serialization (Pydantic model → JSON)
- Retry and error handling for publishing
- Topic configuration

**Not allowed:**
- Event schema definitions (belongs in `data_models/events/`)
- Business logic (belongs in `service_layer/`)
- Broker connection setup (belongs in `config/connections/`)

**Naming convention:** `<event>_producer.py`

### 10.2 `consumers/` - Event Listeners

**Purpose:** Listen for events from message broker topics and trigger appropriate actions.

**Allowed:**
- Kafka/RabbitMQ consumer classes
- Event deserialization (JSON → Pydantic model)
- Delegation to `service_layer/` for processing
- Consumer group configuration
- Offset management and acknowledgment

**Not allowed:**
- Event schema definitions (belongs in `data_models/events/`)
- Heavy business logic (delegate to `service_layer/`)
- Direct database operations (delegate to `service_layer/`)

**Naming convention:** `<event>_consumer.py`

### 10.3 Relationship with Other Directories

| Concern | Location |
|---------|----------|
| Event schemas (Pydantic models) | `data_models/events/` |
| Kafka/broker connection setup | `config/connections/kafka_connection.py` |
| Business logic triggered by events | `service_layer/` |
| Producers and consumers | `event_broker/` |

---

## 11. `src/utils/` - Generic Utilities

Generic helper functions usable by any layer (routes, service_layer, repositories) with no domain knowledge. If you can copy-paste it to a completely different project and it still works, it belongs here.

```
utils/
├── __init__.py
├── date_utils.py          # Date/time formatting and manipulation
├── decorators.py          # Reusable function decorators
├── exceptions.py          # Custom exception classes
├── validation.py          # Generic validation helpers
└── process_mining.py      # Process tracking utilities (if needed)
```

**Purpose:** Provide reusable, domain-agnostic helper functions that reduce code duplication across the service.

**Allowed:**
- Pure functions with no side effects
- Generic decorators (retry, timing, caching)
- Custom exception classes
- Date/time utilities
- String manipulation helpers

**Not allowed:**
- Domain-specific logic (belongs in `service_layer/`)
- Database or API calls
- Business rules
- Dependencies on other `src/` modules (except `config/` for settings)

**Naming convention:** `<category>_utils.py` or `<category>.py`

---

## 12. `src/tests/` - Test Suite

Tests for all functionality between each element of code. Validates that components work correctly in isolation and together.

```
tests/
├── __init__.py
├── unit/                    # Isolated component tests
│   ├── test_services/
│   ├── test_repositories/
│   └── test_utils/
├── integration/             # Cross-component tests
│   ├── test_api/
│   └── test_event_broker/
└── conftest.py              # Shared pytest fixtures
```

**Purpose:** Ensure correctness, prevent regressions, and document expected behavior through executable specifications.

### 12.1 Test Categories

| Category | Purpose | Scope |
|----------|---------|-------|
| **Unit tests** | Test single functions/classes in isolation | Mock all dependencies |
| **Integration tests** | Test component interactions | Real or test databases |
| **API tests** | Test HTTP endpoints | Full request/response cycle |
| **Event tests** | Test producer/consumer flows | Mock or real broker |

### 12.2 Naming Convention

- Test files: `test_<module>.py`
- Test functions: `test_<behavior>_<condition>_<expected>`
- Example: `test_upload_file_invalid_type_raises_error()`

### 12.3 Structure Mirrors Source

Tests should mirror the `src/` structure for easy navigation:

| Source | Test |
|--------|------|
| `service_layer/file_service.py` | `tests/unit/test_services/test_file_service.py` |
| `data_repositories/minio_repository.py` | `tests/unit/test_repositories/test_minio_repository.py` |
| `api/routes/routes_files.py` | `tests/integration/test_api/test_routes_files.py` |

---

## Changelog

| Date | Decision |
|------|----------|
| 2026-01-20 | Initial structure defined: root layout, docs/, scripts/ |
| 2026-01-20 | Defined src/ overview and api/ structure (paths, routes, schemas, dependencies, middleware, clients) |
| 2026-01-20 | Defined data_repositories/ - flat structure, one file per data store |
| 2026-01-22 | Defined data_models/ - nested structure by store type, contains Pydantic + ORM models |
| 2026-01-22 | Defined service_layer/ - domain-aware business logic, boundary with utils |
| 2026-01-22 | Defined config/ - settings + nested connections structure |
| 2026-01-22 | Defined event_broker/ - producers and consumers, schemas in data_models |
| 2026-01-22 | Defined utils/ - generic domain-agnostic helpers |
| 2026-01-22 | Defined tests/ - unit and integration tests mirroring src structure |
| 2026-01-23 | Restructured data_models/ - flat infrastructure-based categories (databases, vector_stores, object_storage, cache, external_apis, events) with mandatory Pydantic validation at all boundaries |
| 2026-01-23 | Aligned Section 9.3 connection categories with data_models/ structure |
| 2026-01-23 | **REVISION:** Fixed path inconsistencies (kafka_models→events/, external_services→external_apis), removed code examples, added Section 4 for main.py/startup.py, added api/clients relationship table, clarified repository naming convention |
