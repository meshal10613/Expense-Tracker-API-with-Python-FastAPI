# Contributing Guidelines

Thank you for your interest in contributing to the **Expense Tracker API** project! We welcome contributions, bug fixes, documentation improvements, and feature proposals.

---

## Code of Conduct

Please treat all community members with respect, empathy, and professional courtesy.

---

## Development Workflow

### 1. Fork & Branch

1. Clone or fork the repository.
2. Create a feature branch off `master`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   For bug fixes:
   ```bash
   git checkout -b fix/issue-description
   ```

### 2. Local Setup

Follow the instructions in [`docs/SETUP_GUIDE.md`](docs/SETUP_GUIDE.md) to set up your virtual environment and install dependencies.

---

## Coding Standards

- **PEP 8**: Follow standard Python formatting rules.
- **Type Annotations**: Always include Python type hints for function signatures and return models.
- **API Response Wrapper**: Ensure all API endpoints return `StandardResponse[T]` defined in [`app/shared/sendResponse.py`](app/shared/sendResponse.py).
- **Docstrings**: Add concise docstrings for new API handlers, helper functions, and Pydantic models.

---

## Commit Guidelines

Use clear, descriptive commit messages adhering to standard conventions:

- `feat: add expense CRUD endpoints`
- `fix: resolve port parsing bug in config.py`
- `docs: update setup guide and API documentation`
- `refactor: improve response model typing`

---

## Pull Request Checklist

Before submitting a Pull Request (PR), please verify:

- [ ] The application starts cleanly without errors (`python app/main.py`).
- [ ] Code follows project conventions and directory modularity.
- [ ] Documentation (`README.md`, `docs/`) is updated if new features or configuration variables were added.
- [ ] Pull Request title clearly describes the change.
