# Installation & Setup Guide

This guide explains how to run the Expense Tracker API locally and with Docker Compose behind Nginx.

---

## System Requirements

For local development:

- Python 3.10 or higher
- pip
- Git

For Docker development:

- Docker Desktop or Docker Engine
- Docker Compose v2

On Windows, Docker Desktop must be running with the Linux engine enabled before using `docker compose`.

---

## Environment Configuration

Create a local `.env` file:

```bash
cp .env.example .env
```

Use:

```env
PORT=5000
```

The application reads `PORT` from the environment and falls back to `5000` when it is missing or invalid.

In Docker Compose, `PORT` is explicitly set to `"5000"` for every FastAPI container so `.env` cannot accidentally make the app listen on a different internal port.

---

## Local Python Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Activate it on Windows CMD:

```cmd
.venv\Scripts\activate.bat
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the local development server with auto reload:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

Local URLs:

```text
http://127.0.0.1:5000
http://127.0.0.1:5000/docs
http://127.0.0.1:5000/redoc
```

---

## Docker Compose Setup

Start the full stack:

```bash
docker compose up --build
```

Run in detached mode:

```bash
docker compose up -d --build
```

Stop the stack:

```bash
docker compose down
```

View logs:

```bash
docker compose logs -f
```

Public Nginx URL:

```text
http://localhost:8080
```

Interactive docs through Nginx:

```text
http://localhost:8080/docs
http://localhost:8080/redoc
```

---

## Docker Service Layout

```text
nginx:80
  -> app1:5000
  -> app2:5000
  -> app3:5000
  -> app4:5000
  -> app5:5000
```

Only Nginx publishes a host port:

```yaml
ports:
  - "8080:80"
```

FastAPI containers use `expose: "5000"` only. This keeps port `5000` private inside Docker's `backend` network.

---

## Health Checks

Each FastAPI container has a health check that calls:

```text
http://127.0.0.1:5000/
```

Nginx starts after all five FastAPI services are healthy.

Check status:

```bash
docker compose ps
```

---

## Verify Load Balancing

Open or refresh:

```text
http://localhost:8080
```

Expected response:

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

The `hostname` value should vary across repeated requests, showing that different FastAPI containers are receiving traffic.

Follow logs:

```bash
docker compose logs -f app1 app2 app3 app4 app5 nginx
```

---

## Troubleshooting

### `uvicorn: command not found`

Use Python module execution:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

Also confirm dependencies are installed:

```bash
pip install -r requirements.txt
```

### Docker cannot connect to `dockerDesktopLinuxEngine`

Start Docker Desktop and wait until it reports that Docker is running. Then retry:

```bash
docker compose up --build
```

On Windows, this can also help:

```bash
wsl --shutdown
```

Then reopen Docker Desktop.

### Port `8080` is already in use

Change the host port in `docker-compose.yml`:

```yaml
ports:
  - "8081:80"
```

Then access:

```text
http://localhost:8081
```

### `ModuleNotFoundError: No module named 'app'`

Run commands from the project root, not from inside the `app/` directory.
