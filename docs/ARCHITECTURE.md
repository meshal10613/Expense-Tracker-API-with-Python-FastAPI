# Architecture & Design Overview

This document describes the architectural principles, directory layout, design patterns, and request lifecycle of the **Expense Tracker API**.

---

## Architecture Principles

1. **Modular & Layered Structure**: Separation of concerns across API routing, shared generic utilities, configuration, and data models.
2. **Versioned API Design**: Decoupled routing enabling seamless backward-compatible versioning (`/api/v1`, `/api/v2`).
3. **Standardized Communication Contract**: Uniform JSON response schema enforced across all endpoints via generic Pydantic generic types.
4. **Environment Isolation**: Strict configuration isolation loading settings (`PORT`, environment secrets) dynamically from `.env`.

---

## Application Directory Topology

```text
.
├── .env                  # Local environment configuration
├── .env.example          # Environment blueprint
├── README.md             # Project primary document
├── requirements.txt      # Python dependencies manifest
├── docs/                 # Extended project documentation suite
│   ├── API_DOCUMENTATION.md
│   ├── ARCHITECTURE.md
│   └── SETUP_GUIDE.md
└── app/                  # Main Python package
    ├── __init__.py       # Top-level package marker
    ├── config.py         # Dynamic environment variable loader (.env)
    ├── main.py           # Application initializer & Uvicorn runner
    ├── api/              # API routing layer
    │   ├── __init__.py   # Package marker
    │   ├── router.py     # Master APIRouter (mounted at /api)
    │   └── v1/           # API version 1 module
    │       ├── __init__.py # Package marker
    │       └── router.py # v1 router aggregator (mounted at /v1)
    ├── core/             # Core application logic & settings
    │   └── __init__.py   # Package marker
    ├── models/           # Domain schemas & database models
    │   └── __init__.py   # Package marker
    └── shared/           # Cross-cutting concerns & shared helpers
        ├── __init__.py   # Package marker
        └── sendResponse.py # Generic Pydantic response models
```

---

## Key Design Patterns

### 1. Master & Versioned Router Aggregation

The routing hierarchy uses hierarchical `APIRouter` composition:

```mermaid
graph TD
    App["FastAPI App (app/main.py)"]
    MasterRouter["Master APIRouter (app/api/router.py) [/api]"]
    V1Router["v1 APIRouter (app/api/v1/router.py) [/v1]"]
    ItemsEndpoint["GET /items"]

    App -->|includes| MasterRouter
    MasterRouter -->|includes| V1Router
    V1Router -->|registers| ItemsEndpoint
```

- **Root App** includes `api_router` mounted under `/api`.
- **`app/api/router.py`** aggregates versioned routers like `v1_router` under `/v1`.
- **Resulting Endpoint Path**: `/api/v1/items`.

---

### 2. Standardized Response Model Pattern

All endpoints construct and return responses using `StandardResponse[T]` defined in [`app/shared/sendResponse.py`](../app/shared/sendResponse.py).

```mermaid
classDiagram
    class StandardResponse~T~ {
        +bool success
        +str message
        +Optional~T~ data
        +Optional~Meta~ meta
    }
    class Meta {
        +Optional~int~ page
        +Optional~int~ limit
        +Optional~int~ total
        +Optional~int~ total_pages
    }
    StandardResponse o-- Meta : contains
```

#### Rationale:
- Enforces consistency across front-end integration.
- Supports generic typed payloads (`T`).
- Easily includes standardized pagination metadata (`Meta`) without altering API signatures.

---

## Request & Execution Lifecycle

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant Main as app/main.py
    participant Router as app/api/router.py
    participant V1 as app/api/v1/router.py
    participant Helper as app/shared/sendResponse.py

    Client->>Main: HTTP GET /api/v1/items
    Main->>Router: Forward to /api
    Router->>V1: Forward to /v1/items
    V1->>Helper: Instantiates StandardResponse(success=True, data=[...], meta=Meta(...))
    Helper-->>V1: Returns validated Pydantic model
    V1-->>Main: Serializes model to JSON
    Main-->>Client: HTTP 200 OK (Standard JSON payload)
```

---

## Extensibility & Scalability Roadmap

1. **Adding API v2**:
   Simply create `app/api/v2/router.py` and include it in `app/api/router.py` with `prefix="/v2"`.
2. **Database Integration**:
   Integrate ORM database engines (e.g. SQLAlchemy or SQLModel) inside `app/models/` and manage DB connections inside `app/core/`.
3. **Authentication Layer**:
   Add JWT authentication middleware or FastAPI dependencies inside `app/core/security.py`.
