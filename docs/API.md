# 🌐 API Documentation - HRGSMS

Comprehensive API documentation for the Hotel Reservation and Guest Services Management System backend.

## 📋 Overview

The HRGSMS API is built with FastAPI and provides RESTful endpoints for managing all aspects of hotel operations. The API follows OpenAPI 3.0 specifications and includes automatic documentation generation.

## 🔗 Base Information

- **Base URL**: `http://localhost:8000`
- **API Version**: v1
- **Documentation**:
  - Swagger UI: `http://localhost:8000/docs`
  - ReDoc: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Authentication Flow

1. POST `/auth/login` with credentials
2. Receive JWT token in response
3. Include token in `Authorization` header: `Bearer <token>`
4. Token expires after 24 hours

### Login Endpoint

```http
POST /auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "password"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

## 📚 API Endpoints

### 🔐 Authentication Routes

- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user info
- `POST /auth/refresh` - Refresh JWT token

### 🏨 Room Management

- `GET /rooms/` - Get all rooms
- `GET /rooms/{room_id}` - Get specific room
- `POST /rooms/` - Create new room
- `PUT /rooms/{room_id}` - Update room
- `DELETE /rooms/{room_id}` - Delete room
- `GET /rooms/available` - Get available rooms
- `GET /rooms/types` - Get room types

### 📅 Reservations

- `GET /reservations/` - Get all reservations
- `GET /reservations/{reservation_id}` - Get specific reservation
- `POST /reservations/` - Create new reservation
- `PUT /reservations/{reservation_id}` - Update reservation
- `DELETE /reservations/{reservation_id}` - Cancel reservation
- `POST /reservations/{reservation_id}/checkin` - Check-in guest
- `POST /reservations/{reservation_id}/checkout` - Check-out guest

### 👥 Guest Management

- `GET /guests/` - Get all guests
- `GET /guests/{guest_id}` - Get specific guest
- `POST /guests/` - Create new guest
- `PUT /guests/{guest_id}` - Update guest
- `DELETE /guests/{guest_id}` - Delete guest
- `GET /guests/{guest_id}/history` - Get guest stay history

### 🛎️ Services

- `GET /services/` - Get all services
- `GET /services/{service_id}` - Get specific service
- `POST /services/` - Create new service
- `PUT /services/{service_id}` - Update service
- `DELETE /services/{service_id}` - Delete service
- `POST /services/requests` - Create service request
- `GET /services/requests` - Get service requests

### 💰 Billing

- `GET /billing/` - Get all bills
- `GET /billing/{bill_id}` - Get specific bill
- `POST /billing/` - Create new bill
- `PUT /billing/{bill_id}` - Update bill
- `POST /billing/{bill_id}/payment` - Process payment
- `GET /billing/{bill_id}/invoice` - Generate invoice

### 📊 Reports

- `GET /reports/occupancy` - Occupancy reports
- `GET /reports/revenue` - Revenue reports
- `GET /reports/guests` - Guest reports
- `GET /reports/services` - Service reports

## 🏗️ Data Models

### Room

```json
{
  "id": 1,
  "room_number": "101",
  "branch_id": 1,
  "type_id": 1,
  "status": "Available",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Guest

```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@email.com",
  "phone": "+94771234567",
  "nic": "123456789V",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Reservation

```json
{
  "id": 1,
  "guest_id": 1,
  "room_id": 1,
  "check_in_date": "2024-01-15",
  "check_out_date": "2024-01-20",
  "total_amount": 500.0,
  "status": "Confirmed",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Service Request

```json
{
  "id": 1,
  "guest_id": 1,
  "service_id": 1,
  "quantity": 2,
  "total_cost": 50.0,
  "status": "Pending",
  "requested_at": "2024-01-01T10:00:00Z"
}
```

## 📝 Request/Response Examples

### Create Reservation

```http
POST /reservations/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "guest_id": 1,
  "room_id": 101,
  "check_in_date": "2024-01-15",
  "check_out_date": "2024-01-20",
  "special_requests": "Late checkout requested"
}
```

**Response:**

```json
{
  "id": 1,
  "guest_id": 1,
  "room_id": 101,
  "check_in_date": "2024-01-15",
  "check_out_date": "2024-01-20",
  "total_amount": 500.0,
  "status": "Confirmed",
  "special_requests": "Late checkout requested",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Get Available Rooms

```http
GET /rooms/available?check_in=2024-01-15&check_out=2024-01-20&branch_id=1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**

```json
{
  "available_rooms": [
    {
      "id": 101,
      "room_number": "101",
      "type": "Single",
      "rate": 100.0,
      "amenities": ["WiFi", "AC", "TV"]
    },
    {
      "id": 102,
      "room_number": "102",
      "type": "Double",
      "rate": 150.0,
      "amenities": ["WiFi", "AC", "TV", "Balcony"]
    }
  ],
  "total_count": 2
}
```

## 🔍 Query Parameters

### Common Parameters

- `limit`: Number of results to return (default: 50, max: 100)
- `offset`: Number of results to skip (default: 0)
- `sort_by`: Field to sort by
- `sort_order`: `asc` or `desc` (default: `asc`)

### Filtering

- Date fields: Use ISO format `YYYY-MM-DD`
- Search: Use `search` parameter for text search
- Status: Filter by entity status
- Branch: Filter by branch ID

### Example with Filters

```http
GET /reservations/?branch_id=1&status=Confirmed&check_in_date_from=2024-01-01&limit=25&sort_by=created_at&sort_order=desc
```

## ⚠️ Error Handling

### HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

### Error Response Format

```json
{
  "detail": "Error message",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Common Error Codes

- `AUTH_REQUIRED` - Authentication required
- `AUTH_INVALID` - Invalid credentials
- `VALIDATION_ERROR` - Request validation failed
- `RESOURCE_NOT_FOUND` - Requested resource not found
- `ROOM_UNAVAILABLE` - Room not available for booking
- `INSUFFICIENT_PERMISSIONS` - User lacks required permissions

## 🔧 Rate Limiting

- **Rate Limit**: 1000 requests per hour per IP
- **Burst Limit**: 100 requests per minute
- **Headers**:
  - `X-RateLimit-Limit`: Request limit
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset time

## 📊 Pagination

Large datasets are paginated using offset-based pagination:

```json
{
  "items": [...],
  "total": 150,
  "limit": 50,
  "offset": 0,
  "has_next": true,
  "has_prev": false
}
```

## 🔐 CORS Configuration

- **Allowed Origins**: `http://localhost:5173` (development)
- **Allowed Methods**: `GET, POST, PUT, DELETE, OPTIONS`
- **Allowed Headers**: `Authorization, Content-Type`
- **Max Age**: 3600 seconds

## 🧪 Testing

### Using cURL

```bash
# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Get rooms with token
curl -X GET http://localhost:8000/rooms/ \
  -H "Authorization: Bearer <your-token>"
```

### Using Python Requests

```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/auth/login",
    json={"username": "admin", "password": "password"}
)
token = response.json()["access_token"]

# Make authenticated request
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://localhost:8000/rooms/", headers=headers)
```

## 📈 Performance

### Response Times

- **Authentication**: < 100ms
- **Simple queries**: < 200ms
- **Complex queries**: < 500ms
- **Reports**: < 2s

### Database Optimization

- Indexed primary keys
- Foreign key constraints
- Query optimization
- Connection pooling

## 🛠️ Development

### Running API Server

```bash
cd backend
pip install -r requirements.txt
python run.py
```

### Environment Variables

```bash
DATABASE_URL=mysql://user:pass@localhost/hrgsms_db
SECRET_KEY=your-secret-key
DEBUG=True
CORS_ORIGINS=http://localhost:5173
```

### Database Migrations

```bash
# Run migrations
python -m alembic upgrade head

# Create new migration
python -m alembic revision --autogenerate -m "Description"
```

## 📝 API Versioning

- **Current Version**: v1
- **Version Header**: `API-Version: v1`
- **URL Versioning**: `/api/v1/`
- **Backward Compatibility**: 2 versions

## 🔄 Webhooks

### Available Events

- `reservation.created`
- `reservation.updated`
- `guest.checked_in`
- `guest.checked_out`
- `payment.completed`

### Webhook Format

```json
{
  "event": "reservation.created",
  "data": {...},
  "timestamp": "2024-01-01T00:00:00Z",
  "signature": "sha256=..."
}
```

---

**Comprehensive API for modern hotel management** 🚀
