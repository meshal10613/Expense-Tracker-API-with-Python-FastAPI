# Changelog

All notable changes to the Expense Tracker API project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- Pydantic V2 schema validation (`ExpenseCreate`, `ExpenseUpdate`, `ExpenseResponse`) in [`app/schemas/expense.py`](app/schemas/expense.py).
- Automated date generation (`YYYY-MM-DD`) when creating expenses without a date parameter.
- Custom model validator in `ExpenseUpdate` ensuring at least 1 field is supplied for update requests.
- Service layer [`app/services/expense_service.py`](app/services/expense_service.py) separating domain logic and JSON file persistence from API controllers.
- Full CRUD API endpoints (`GET`, `POST`, `PUT`, `DELETE`) under `/api/v1/expenses`.
- Optional `search` (by name, category, description), `sort_by` (field selection), and `order` (`asc`/`desc`) query parameters to `GET /api/v1/expenses`.
- Docker Compose stack with five FastAPI services: `app1`, `app2`, `app3`, `app4`, and `app5`.
- Nginx reverse proxy and load balancer on host port `8080`.

### Changed

- Refactored [`app/api/v1/expenses/router.py`](app/api/v1/expenses/router.py) to delegate business logic to `expense_service` and validate HTTP bodies via Pydantic schemas.
- Updated documentation (`README.md`, `API_DOCUMENTATION.md`, `ARCHITECTURE.md`, `SETUP_GUIDE.md`) to reflect full CRUD endpoints, Pydantic validation rules, and the layered architecture.

### Fixed

- Fixed relative file loading path in `load_data()` by using [`DB_EXPENSES_FILE`](app/config.py) from `app.config`.
- Fixed sequential ID generation logic when expenses are deleted.

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
