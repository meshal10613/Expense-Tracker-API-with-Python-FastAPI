# Expense Tracker API with Python & FastAPI

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

A clean FastAPI REST API with versioned routing, standardized API responses, Docker support, and an Nginx reverse proxy that load balances traffic across five FastAPI containers.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Docker And Nginx](#docker-and-nginx)
- [API Documentation](#api-documentation)
- [Load Balancer Verification](#load-balancer-verification)
- [Extended Documentation](#extended-documentation)
- [Roadmap](#roadmap)
- [License](#license)

---

## Features

- **FastAPI application** served by Uvicorn.
- **Versioned API routing** under `/api/v1`.
- **Standard response model** for API routes through `StandardResponse`.
- **Environment-based port config** through `PORT`, defaulting to `5000`.
- **Dockerized runtime** using `python:3.12-slim`.
- **Nginx reverse proxy** exposed on host port `8080`.
- **Five FastAPI instances**: `app1`, `app2`, `app3`, `app4`, and `app5`.
- **Container health checks** for each FastAPI service.
- **Root diagnostic response** with process id and hostname to confirm load balancing.

---

## Architecture

```text
Client
  |
  v
localhost:8080
  |
  v
Nginx container:80
  |
  +--> app1:5000
  +--> app2:5000
  +--> app3:5000
  +--> app4:5000
  +--> app5:5000
```

Nginx and the FastAPI containers communicate over Docker's internal `backend` network. Port `5000` is not published to the host; only Nginx is publicly reachable through `8080`.

---

## Project Structure

```text
.
├── .dockerignore
├── .env
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── nginx/
│   └── default.conf
├── requirements.txt
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── docs/
│   ├── API_DOCUMENTATION.md
│   ├── ARCHITECTURE.md
│   └── SETUP_GUIDE.md
└── app/
    ├── __init__.py
    ├── config.py
    ├── main.py
    ├── api/
    │   ├── router.py
    │   └── v1/
    │       └── router.py
    ├── core/
    ├── models/
    └── shared/
        └── sendResponse.py
```

---

## Quick Start

Create `.env`:

```bash
cp .env.example .env
```

Use:

```env
PORT=5000
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run locally with auto reload:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

Local app URL:

```text
http://127.0.0.1:5000
```

---

## Docker And Nginx

Start the complete Docker setup:

```bash
docker compose up --build
```

Run in the background:

```bash
docker compose up -d --build
```

Stop containers:

```bash
docker compose down
```

View logs:

```bash
docker compose logs -f
```

Public URL through Nginx:

```text
http://localhost:8080
```

Swagger and ReDoc through Nginx:

```text
http://localhost:8080/docs
http://localhost:8080/redoc
```

---

## API Documentation

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Root diagnostic endpoint with container instance metadata |
| `GET` | `/api/v1/items` | Example v1 items endpoint using `StandardResponse` |

Root response example:

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

---

## Load Balancer Verification

Refresh this URL several times:

```text
http://localhost:8080
```

The `instance.hostname` value should change between `app1`, `app2`, `app3`, `app4`, and `app5` containers over repeated requests.

You can also inspect service status:

```bash
docker compose ps
```

And follow logs for all app containers:

```bash
docker compose logs -f app1 app2 app3 app4 app5 nginx
```

Nginx currently uses `least_conn`, so traffic is sent to the upstream container with the fewest active connections.

---

## Extended Documentation

- [API Documentation](docs/API_DOCUMENTATION.md)
- [Architecture Guide](docs/ARCHITECTURE.md)
- [Setup Guide](docs/SETUP_GUIDE.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

---

## Roadmap

- [ ] Implement Expense CRUD operations at `/api/v1/expenses`.
- [ ] Add Category management endpoints at `/api/v1/categories`.
- [ ] Connect SQLAlchemy or SQLModel with SQLite/PostgreSQL.
- [ ] Add JWT authentication and authorization.
- [ ] Add unit and integration tests with `pytest`.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
