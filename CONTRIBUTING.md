# Contributing Guidelines

Thank you for contributing to the Expense Tracker API.

---

## Development Workflow

Create a branch:

```bash
git checkout -b feature/your-feature-name
```

For fixes:

```bash
git checkout -b fix/issue-description
```

---

## Local Setup

Follow [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md).

Common local command:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

Docker command:

```bash
docker compose up --build
```

Docker URL:

```text
http://localhost:8080
```

---

## Coding Standards

- Follow PEP 8.
- Use type hints for new functions where practical.
- Keep route modules small and grouped by domain.
- Use `StandardResponse[T]` for normal API endpoints.
- Keep the root `/` diagnostic endpoint returning instance metadata unless the load-balancer check is replaced with another endpoint.
- Keep FastAPI containers listening on `0.0.0.0:5000` in Docker.
- Do not publish app container port `5000` directly to the host; expose public traffic through Nginx.

---

## Docker And Nginx Changes

When changing Docker or Nginx config, verify:

```bash
docker compose config
```

Then run:

```bash
docker compose up --build
```

Confirm:

```bash
docker compose ps
```

Refresh `http://localhost:8080` several times and check that different `instance.hostname` values appear.

---

## Commit Guidelines

Use clear commit messages:

- `feat: add expense CRUD endpoints`
- `fix: resolve port parsing bug`
- `docs: update docker setup guide`
- `refactor: split auth routes`

---

## Pull Request Checklist

- [ ] Local server starts with `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000`.
- [ ] Docker stack starts with `docker compose up --build`.
- [ ] Nginx endpoint works at `http://localhost:8080`.
- [ ] `docker compose ps` shows healthy app containers.
- [ ] New API routes use the project routing conventions.
- [ ] Documentation is updated when behavior, commands, routes, or configuration changes.
