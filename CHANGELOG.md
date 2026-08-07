# Changelog

All notable changes to the **Expense Tracker API** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Expense CRUD endpoints (`POST`, `GET`, `PUT`, `DELETE` `/api/v1/expenses`).
- Category management endpoints (`/api/v1/categories`).
- Database integration via SQLAlchemy / SQLModel (PostgreSQL / SQLite).
- JWT User Authentication & Authorization.

---

## [1.0.0] - 2026-08-08

### Added
- **FastAPI Core**: Initial project setup with FastAPI framework and Uvicorn server runner.
- **Environment Management**: Dynamic environment configuration via `python-dotenv` in `app/config.py`.
- **Modular Package Structure**: Clean directory hierarchy with `__init__.py` markers across `app/`, `api/`, `core/`, `models/`, and `shared/`.
- **Versioned API Architecture**: Master `APIRouter` mounted at `/api` and aggregated v1 sub-router mounted at `/v1`.
- **Standardized Response Model**: Generic `StandardResponse` and `Meta` generic Pydantic models in `app/shared/sendResponse.py`.
- **Documentation Suite**: Added `README.md`, `docs/API_DOCUMENTATION.md`, `docs/ARCHITECTURE.md`, `docs/SETUP_GUIDE.md`, `CONTRIBUTING.md`, and `CHANGELOG.md`.
