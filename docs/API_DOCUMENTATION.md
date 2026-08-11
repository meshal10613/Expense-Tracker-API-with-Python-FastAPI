# API Documentation

This document describes the available API endpoints, Pydantic validation rules, and response formats.

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

---

### Get Expenses List

Returns stored expense records loaded from `db/expenses.json`. Supports optional search by name/category/description, field sorting, and ordering.

- **URL**: `/api/v1/expenses`
- **Method**: `GET`
- **Authentication**: No

#### Query Parameters

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `search` | `string` | No | `null` | Case-insensitive search on expense name, category, or description |
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

---

### Get Expense by ID

Returns a single expense record by ID.

- **URL**: `/api/v1/expenses/{expense_id}`
- **Method**: `GET`
- **Authentication**: No

---

### Create Expense

Creates a new expense record.

- **URL**: `/api/v1/expenses/`
- **Method**: `POST`
- **Validation**: Enforced via Pydantic (`ExpenseCreate`)

#### Payload Rules
- `name`: `string` (Required, 1-100 characters)
- `amount`: `number` (Required, > 0)
- `category`: `string` (Required, 1-50 characters)
- `description`: `string` (Required, max 500 characters)
- `date`: `string` (Optional, ISO date `YYYY-MM-DD`). **Auto-generated** to today's date if omitted or set to `null`.

#### Request Body Example
```json
{
  "name": "Coffee & Snacks",
  "amount": 12.50,
  "category": "Food",
  "description": "Afternoon coffee break"
}
```

#### Response Example (`201 Created`)
```json
{
  "success": true,
  "message": "Expense created successfully with ID E011",
  "data": {
    "id": "E011",
    "name": "Coffee & Snacks",
    "amount": 12.5,
    "category": "Food",
    "date": "2026-08-11",
    "description": "Afternoon coffee break"
  }
}
```

---

### Update Expense

Updates an existing expense record by ID.

- **URL**: `/api/v1/expenses/{expense_id}`
- **Method**: `PUT`
- **Validation**: Enforced via Pydantic (`ExpenseUpdate`)

#### Payload Rules
- All fields (`name`, `amount`, `category`, `date`, `description`) are optional.
- **Minimum 1 field requirement**: The request body must contain at least 1 field to update. Sending an empty JSON `{}` or all `null` fields returns `422 Unprocessable Entity`.

#### Request Body Example
```json
{
  "amount": 15.00
}
```

#### Response Example (`200 OK`)
```json
{
  "success": true,
  "message": "Expense with ID E011 updated successfully",
  "data": {
    "id": "E011",
    "name": "Coffee & Snacks",
    "amount": 15.0,
    "category": "Food",
    "date": "2026-08-11",
    "description": "Afternoon coffee break"
  }
}
```

---

### Delete Expense

Deletes an expense record by ID.

- **URL**: `/api/v1/expenses/{expense_id}`
- **Method**: `DELETE`

---

## HTTP Status Codes

| Code | Status | Description |
| :--- | :--- | :--- |
| `200` | OK | Request processed successfully |
| `201` | Created | Resource created successfully |
| `400` | Bad Request | Invalid request parameters |
| `404` | Not Found | Expense ID or route not found |
| `422` | Unprocessable Entity | Pydantic validation failed |
| `500` | Internal Server Error | Unexpected server error |
| `502` | Bad Gateway | Nginx could not reach a healthy upstream |
| `503` | Service Unavailable | Upstream service unavailable |
