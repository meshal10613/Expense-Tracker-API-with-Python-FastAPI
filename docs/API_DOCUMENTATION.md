# API Documentation

This document describes the currently available API endpoints and response formats.

---

## Base URLs

Local Python server:

```text
http://127.0.0.1:5000
```

Docker/Nginx server:

```text
http://localhost:8080
```

Interactive documentation:

```text
http://localhost:8080/docs
http://localhost:8080/redoc
```

---

## Response Formats

Most API routes use the standard `Success` or `Error` model from [`app/shared/response.py`](../app/shared/response.py).

The root `/` endpoint is an exception. It returns instance metadata for Docker/Nginx load-balancer verification.

### Success Response

```typescript
interface Success<T> {
  success: boolean;
  message: string;
  data?: T;
  meta?: Meta;
}

interface Meta {
  page?: number;
  limit?: number;
  total?: number;
  total_pages?: number;
}
```

### Error Response

```typescript
interface Error {
  success: boolean;
  message: string;
  details?: string;
}
```

---

## Endpoints

### Root Diagnostic Endpoint

Returns a basic status response plus the process id and container hostname that handled the request.

- **URL**: `/`
- **Method**: `GET`
- **Authentication**: No
- **Used for**: Health checks and load-balancer verification

#### Response

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

#### cURL

Local:

```bash
curl http://127.0.0.1:5000/
```

Through Nginx:

```bash
curl http://localhost:8080/
```

---

### Get Expenses List

Returns stored expense records loaded from `db/expenses.json`. Supports optional search by name, field sorting, and ordering.

- **URL**: `/api/v1/expenses` (or `/api/v1/expenses/`)
- **Method**: `GET`
- **Authentication**: No

#### Query Parameters

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `search` | `string` | No | `null` | Case-insensitive search on expense name |
| `sort_by` | `string` | No | `null` | Field to sort by: `id`, `name`, `amount`, `category`, `date`, `description` |
| `order` | `string` | No | `"asc"` | Sort ordering: `asc` or `desc` |

#### Response

```json
{
  "success": true,
  "message": "Expenses retrieved successfully",
  "data": [
    {
      "id": "E001",
      "name": "Groceries",
      "amount": 150.75,
      "category": "Food",
      "date": "2024-06-01",
      "description": "Weekly grocery shopping at the local supermarket."
    }
  ],
  "meta": null
}
```

#### cURL

All expenses:

```bash
curl http://localhost:8080/api/v1/expenses/
```

Search and sort:

```bash
curl "http://localhost:8080/api/v1/expenses/?search=bill&sort_by=amount&order=desc"
```

#### Python Example

```python
import requests

response = requests.get(
    "http://localhost:8080/api/v1/expenses/",
    params={"search": "bill", "sort_by": "amount", "order": "desc"}
)
payload = response.json()

print(payload["success"])
print(payload["message"])
print(payload["data"])
```
```

---

## HTTP Status Codes

| Code | Status | Description |
| :--- | :--- | :--- |
| `200` | OK | Request processed successfully |
| `400` | Bad Request | Invalid request data |
| `404` | Not Found | Endpoint or resource does not exist |
| `422` | Unprocessable Entity | Validation failed |
| `500` | Internal Server Error | Unexpected server error |
| `502` | Bad Gateway | Nginx could not reach a healthy upstream |
| `503` | Service Unavailable | Upstream service unavailable |

---

## Planned Endpoints

- `POST /api/v1/expenses`
- `GET /api/v1/expenses`
- `GET /api/v1/expenses/{id}`
- `PUT /api/v1/expenses/{id}`
- `DELETE /api/v1/expenses/{id}`
- `GET /api/v1/categories`
