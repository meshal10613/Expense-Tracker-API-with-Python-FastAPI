# API Documentation

Welcome to the **Expense Tracker API** specification. This document outlines the available HTTP endpoints, standard response models, error structures, and example requests.

---

## Interactive Documentation

When the application is running, interactive OpenAPI documentation can be accessed via:

- **Swagger UI**: [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs)
- **ReDoc**: [http://127.0.0.1:5000/redoc](http://127.0.0.1:5000/redoc)

*(Note: Replace `5000` with your custom `PORT` if configured differently in `.env`)*

---

## Standard Response Format

All API responses strictly follow a generic response wrapper (`StandardResponse`) defined in [`app/shared/sendResponse.py`](../app/shared/sendResponse.py).

### Schema Definition

```typescript
interface StandardResponse<T> {
  success: boolean;       // Indicates if the operation succeeded
  message: string;        // Human-readable response summary
  data?: T;               // Primary response payload (Generic object/array)
  meta?: Meta;            // Metadata object for pagination/summary stats
}

interface Meta {
  page?: number;          // Current page index (1-based)
  limit?: number;         // Items requested per page
  total?: number;         // Total items available in backend storage
  total_pages?: number;   // Total calculated pages
}
```

---

## Endpoints Specification

### 1. Root / Health Check Endpoint

Retrieves basic server status and confirmation that the API is running.

- **URL**: `/`
- **Method**: `GET`
- **Authentication Required**: No

#### Response

- **Status Code**: `200 OK`
- **Content-Type**: `application/json`

```json
{
  "success": true,
  "message": "Hello, World!"
}
```

#### cURL Example

```bash
curl -X GET "http://127.0.0.1:5000/" -H "accept: application/json"
```

---

### 2. Get Items List (API v1)

Retrieves a paginated list of items registered under API Version 1.

- **URL**: `/api/v1/items`
- **Method**: `GET`
- **Authentication Required**: No

#### Response

- **Status Code**: `200 OK`
- **Content-Type**: `application/json`

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

#### cURL Example

```bash
curl -X GET "http://127.0.0.1:5000/api/v1/items" -H "accept: application/json"
```

#### Python `requests` Example

```python
import requests

url = "http://127.0.0.1:5000/api/v1/items"
response = requests.get(url)

if response.status_code == 200:
    payload = response.json()
    print("Success:", payload["success"])
    print("Message:", payload["message"])
    print("Data:", payload["data"])
    print("Meta:", payload["meta"])
```

---

## HTTP Status Codes

The API utilizes standard HTTP status codes:

| Code | Status | Description |
| :--- | :--- | :--- |
| `200` | OK | Request processed successfully. |
| `400` | Bad Request | Invalid parameter or payload sent by client. |
| `404` | Not Found | Requested endpoint or resource does not exist. |
| `422` | Unprocessable Entity | Pydantic data validation failed. |
| `500` | Internal Server Error | Unexpected server error occurred. |

---

## Future Endpoints (Planned)

The following endpoints are scheduled for upcoming releases:

- `POST /api/v1/expenses` — Create a new expense entry
- `GET /api/v1/expenses` — List and filter expenses
- `GET /api/v1/expenses/{id}` — Get detailed information on a single expense
- `PUT /api/v1/expenses/{id}` — Update existing expense details
- `DELETE /api/v1/expenses/{id}` — Remove an expense entry
- `GET /api/v1/categories` — List expense categories
