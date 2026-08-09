# Changelog

All notable changes to the Expense Tracker API project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- Optional `search` (by name, case-insensitive), `sort_by` (field selection), and `order` (`asc`/`desc`) query parameters to `GET /api/v1/expenses`.
- Expenses endpoint `/api/v1/expenses` returning stored expense data from `db/expenses.json`.
- `db/` directory copying to `Dockerfile` to ensure JSON data file availability within Docker containers.
- Dockerfile for containerized FastAPI/Uvicorn runtime.
- Docker Compose stack with five FastAPI services: `app1`, `app2`, `app3`, `app4`, and `app5`.
- Nginx reverse proxy and load balancer on host port `8080`.
- Docker bridge network for internal service discovery.
- Health checks for FastAPI containers.
- Root diagnostic response with `pid` and `hostname` for load-balancer verification.
- Docker setup and verification documentation.

### Fixed

- Fixed `TabError` (inconsistent use of tabs and spaces in indentation) in [`app/api/v1/expenses/router.py`](app/api/v1/expenses/router.py).
- Fixed relative file loading path in `load_data()` by using [`DB_EXPENSES_FILE`](app/config.py) from `app.config`.
- Fixed missing `db/` directory in `Dockerfile`.

### Changed

- Local development command now uses `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000`.
- Uvicorn startup now uses `app.main:app` and binds to `0.0.0.0`.
- Docker runtime explicitly uses `PORT=5000` to avoid `.env` conflicts.
- Updated documentation (`README.md`, `API_DOCUMENTATION.md`, `ARCHITECTURE.md`, `SETUP_GUIDE.md`) to reflect `GET /api/v1/expenses`, standardized response models (`Success`, `Error`, `Meta`), and accurate project layout.

### Planned

- Full Expense CRUD operations (Create, Update, Delete) under `/api/v1/expenses`.
- Category management endpoints under `/api/v1/categories`.
- Database integration with SQLAlchemy or SQLModel.
- JWT authentication and authorization.
- Test suite with `pytest`.

---

## [1.0.0] - 2026-08-08

### Added

- Initial FastAPI application.
- Uvicorn server runner.
- Environment configuration with `python-dotenv`.
- Modular package structure under `app/`.
- Versioned routing with `/api/v1`.
- Shared `StandardResponse` and `Meta` models.
- Initial documentation suite.
