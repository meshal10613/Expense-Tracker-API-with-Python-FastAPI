# Architecture & Design Overview

This document describes the current architecture of the Expense Tracker API, including the FastAPI application, Docker Compose runtime, and Nginx load balancer.

---

## Architecture Principles

1. **Modular routing**: API routes are grouped through FastAPI `APIRouter` modules.
2. **Versioned APIs**: Current public API routes live under `/api/v1`.
3. **Standard responses**: API endpoints use a shared response contract where appropriate.
4. **Environment-based configuration**: `PORT` is read from the environment and defaults to `5000`.
5. **Container-first runtime**: Docker Compose runs five FastAPI app containers behind Nginx.
6. **Private app network**: FastAPI containers do not publish port `5000` to the host.

---

## Runtime Architecture

```mermaid
graph TD
    Client["Client Browser / HTTP Client"]
    Nginx["Nginx Reverse Proxy<br/>host 8080 -> container 80"]
    App1["app1:5000"]
    App2["app2:5000"]
    App3["app3:5000"]
    App4["app4:5000"]
    App5["app5:5000"]

    Client --> Nginx
    Nginx --> App1
    Nginx --> App2
    Nginx --> App3
    Nginx --> App4
    Nginx --> App5
```

Nginx communicates with `app1` through `app5` using Docker's internal DNS on the `backend` network.

---

## Docker Networking

The Compose stack defines one bridge network:

```yaml
networks:
  backend:
    driver: bridge
```

Every FastAPI container and the Nginx container joins this network. Nginx can resolve app containers by service name:

```nginx
server app1:5000;
server app2:5000;
server app3:5000;
server app4:5000;
server app5:5000;
```

Only Nginx is exposed to the host:

```yaml
ports:
  - "8080:80"
```

FastAPI services use `expose: "5000"`, which documents the internal port without publishing it to the host.

---

## Nginx Load Balancing

The upstream uses `least_conn`:

```nginx
upstream expense_tracker_api {
    least_conn;
    server app1:5000;
    server app2:5000;
    server app3:5000;
    server app4:5000;
    server app5:5000;
}
```

`least_conn` sends each request to the upstream container with the fewest active connections. For light manual browser refreshes, distribution may not appear perfectly round-robin, but repeated requests should show traffic reaching all five containers.

---

## Request Lifecycle

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant Nginx as Nginx :80
    participant App as FastAPI appN:5000
    participant Router as app/api/router.py
    participant V1 as app/api/v1/router.py
    participant Expenses as app/api/v1/expenses/router.py

    Client->>Nginx: GET /api/v1/expenses on localhost:8080
    Nginx->>App: Proxy request to one healthy upstream
    App->>Router: Match /api
    Router->>V1: Match /v1
    V1->>Expenses: Match /expenses
    Expenses-->>App: Return Success model payload with db/expenses.json
    App-->>Nginx: JSON response
    Nginx-->>Client: HTTP 200
```

For the root diagnostic endpoint:

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant Nginx as Nginx :80
    participant App as FastAPI appN:5000

    Client->>Nginx: GET /
    Nginx->>App: Proxy to one upstream container
    App-->>Nginx: success, message, pid, hostname
    Nginx-->>Client: JSON response
```

---

## Application Routing

```mermaid
graph TD
    Main["app/main.py<br/>FastAPI app"]
    ApiRouter["app/api/router.py<br/>/api"]
    V1Router["app/api/v1/router.py<br/>/v1"]
    ExpensesRouter["app/api/v1/expenses/router.py<br/>/expenses"]
    ExpensesEndpoint["GET /expenses"]
    Root["GET /"]

    Main --> Root
    Main --> ApiRouter
    ApiRouter --> V1Router
    V1Router --> ExpensesRouter
    ExpensesRouter --> ExpensesEndpoint
```

Final endpoint paths:

```text
GET /
GET /api/v1/expenses
```

---

## Health Checks

Each app service runs a Docker health check against:

```text
http://127.0.0.1:5000/
```

Nginx has `depends_on` conditions so it starts after the five FastAPI services become healthy.

---

## Root Diagnostic Response

The root endpoint returns instance metadata:

```json
{
  "success": true,
  "message": "Hello, World!",
  "instance": {
    "pid": 1,
    "hostname": "container-id"
  }
}
```

This response is intentionally not wrapped in `StandardResponse`; it exists to verify which container handled a request.

---

## Extension Plan

Recommended future structure for domain modules:

```text
app/api/v1/
├── auth/
│   ├── routes.py
│   ├── schemas.py
│   └── service.py
├── users/
│   ├── routes.py
│   ├── schemas.py
│   └── service.py
└── router.py
```

Keep HTTP concerns in `routes.py`, validation models in `schemas.py`, and business logic in `service.py`.
