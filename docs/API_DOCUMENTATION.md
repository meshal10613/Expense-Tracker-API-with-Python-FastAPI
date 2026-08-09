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

Most API routes should use the shared `StandardResponse` model from [`app/shared/sendResponse.py`](../app/shared/sendResponse.py).

The root `/` endpoint is an exception. It returns instance metadata for Docker/Nginx load-balancer verification.

### StandardResponse

```typescript
interface StandardResponse<T> {
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

### Get Items List

Returns an example list of items from API version 1.

- **URL**: `/api/v1/items`
- **Method**: `GET`
- **Authentication**: No

#### Response

```json
{
  "success": true,
  "message": "Items retrieved successfully",
  "data": [
    "item1",
    "item2",
    "item3"
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 3,
    "total_pages": 1
  }
}
```

#### cURL

Local:

```bash
curl http://127.0.0.1:5000/api/v1/items
```

Through Nginx:

```bash
curl http://localhost:8080/api/v1/items
```

#### Python Example

```python
import requests

response = requests.get("http://localhost:8080/api/v1/items")
payload = response.json()

print(payload["success"])
print(payload["message"])
print(payload["data"])
print(payload["meta"])
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
