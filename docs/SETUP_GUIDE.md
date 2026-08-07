# Installation & Setup Guide

This comprehensive guide will walk you through setting up, configuring, and running the **Expense Tracker API** on Windows, macOS, or Linux.

---

## System Requirements

Before starting, ensure you have the following installed:

- **Python**: Version 3.10 or higher (`python --version`)
- **pip**: Python package manager (`pip --version`)
- **Git**: Source control (`git --version`)

---

## 1. Environment Configuration

The application reads configuration values (such as server `PORT`) dynamically from a `.env` file at project root using `python-dotenv`.

1. Copy `.env.example` to create your local `.env` file:

```bash
cp .env.example .env
```

2. Open `.env` in your code editor and adjust variables as needed:

```env
PORT=5000
```

---

## 2. Virtual Environment Setup

Isolate your project dependencies by creating a Python virtual environment.

### Windows (PowerShell)

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1
```

> **Note for PowerShell execution policy error**:
> If you encounter an execution policy restriction, run:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`

### Windows (Command Prompt / CMD)

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### macOS / Linux (Bash / Zsh)

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

---

## 3. Install Dependencies

With the virtual environment active, install all required packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

To confirm installation, you can inspect installed packages:

```bash
pip list
```

---

## 4. Running the Server

You can launch the FastAPI server using two alternative methods:

### Method A: Programmatic Execution (Recommended)

Run `app/main.py` directly using Python. The script programmatically reads `PORT` from `.env` and triggers Uvicorn:

```bash
python app/main.py
```

### Method B: Direct Uvicorn CLI

Alternatively, run Uvicorn directly from the command line:

```bash
python -m uvicorn app.main:app --reload --port 5000
```

---

## 5. Verifying Installation

Once started, test the application by visiting:

- **Root Health Check**: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- **Swagger Documentation**: [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs)
- **ReDoc Documentation**: [http://127.0.0.1:5000/redoc](http://127.0.0.1:5000/redoc)

---

## Troubleshooting & FAQ

### Issue 1: `Port 5000 is already in use`
- **Solution**: Edit `.env` and change `PORT=5000` to an open port (e.g. `PORT=8000`), then restart the server.

### Issue 2: `ModuleNotFoundError: No module named 'app'`
- **Solution**: Ensure you are running commands from the project root folder (`Expense Tracker API with Python & FastAPI/`), not from inside `app/`.

### Issue 3: Virtual environment not activating on VS Code
- **Solution**: Open command palette (`Ctrl+Shift+P`), select **Python: Select Interpreter**, and choose `.venv/Scripts/python.exe`.
