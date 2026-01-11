# 🔌 API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, no authentication is required. In production, consider implementing:
- API keys
- OAuth 2.0
- JWT tokens

## Endpoints

### 1. Predict House Price

Predict the price of a house based on its features.

**Endpoint**: `POST /predict`

**Request Body**:

```json
{
  "area": 2500,
  "bedrooms": 3,
  "bathrooms": 2.5,
  "location": "Downtown",
  "year_built": 2010
}
```

**Request Schema**:

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| area | float | Yes | > 0, < 50000 | Living area in square feet |
| bedrooms | integer | Yes | 0-20 | Number of bedrooms |
| bathrooms | float | Yes | 0-20 | Number of bathrooms |
| location | string | Yes | min_length=1 | Location/neighborhood |
| year_built | integer | Yes | 1800-2030 | Year the house was built |

**Success Response** (200 OK):

```json
{
  "predicted_price": 450000.50,
  "model_used": "Ridge Regression",
  "confidence_interval": {
    "lower": 427500.48,
    "upper": 472500.53
  },
  "input_features": {
    "area": 2500,
    "bedrooms": 3,
    "bathrooms": 2.5,
    "location": "Downtown",
    "year_built": 2010
  }
}
```

**Error Responses**:

*400 Bad Request* - Invalid input:
```json
{
  "error": "ValidationError",
  "message": "Invalid input data",
  "detail": "Area must be greater than 0"
}
```

*500 Internal Server Error* - Server error:
```json
{
  "error": "PredictionError",
  "message": "Failed to make prediction",
  "detail": "Model not loaded"
}
```

**Example cURL**:

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "area": 2500,
    "bedrooms": 3,
    "bathrooms": 2.5,
    "location": "Downtown",
    "year_built": 2010
  }'
```

**Example Python**:

```python
import requests

url = "http://localhost:8000/api/v1/predict"
data = {
    "area": 2500,
    "bedrooms": 3,
    "bathrooms": 2.5,
    "location": "Downtown",
    "year_built": 2010
}

response = requests.post(url, json=data)
result = response.json()
print(f"Predicted Price: ${result['predicted_price']:,.2f}")
```

**Example JavaScript**:

```javascript
const response = await fetch('http://localhost:8000/api/v1/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    area: 2500,
    bedrooms: 3,
    bathrooms: 2.5,
    location: 'Downtown',
    year_built: 2010
  })
});

const result = await response.json();
console.log(`Predicted Price: $${result.predicted_price.toLocaleString()}`);
```

---

### 2. Health Check

Check the health status of the API service.

**Endpoint**: `GET /health`

**Request**: No parameters required

**Success Response** (200 OK):

```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_name": "Ridge Regression",
  "timestamp": "2026-01-10T22:37:22Z"
}
```

**Example cURL**:

```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

---

### 3. Get Model Information

Get detailed information about the loaded ML model.

**Endpoint**: `GET /model-info`

**Request**: No parameters required

**Success Response** (200 OK):

```json
{
  "model_loaded": true,
  "model_name": "Ridge Regression",
  "model_type": "Ridge",
  "features": ["area", "bedrooms", "bathrooms", "location", "year_built"],
  "training_date": "2026-01-10T17:30:00",
  "cv_folds": 5,
  "cv_results": {
    "Linear Regression": {
      "mean_rmse": 45230.12,
      "std_rmse": 3421.45,
      "mean_r2": 0.8234,
      "std_r2": 0.0234
    },
    "Ridge Regression": {
      "mean_rmse": 42150.34,
      "std_rmse": 2987.23,
      "mean_r2": 0.8567,
      "std_r2": 0.0198
    },
    "Lasso Regression": {
      "mean_rmse": 43890.78,
      "std_rmse": 3156.89,
      "mean_r2": 0.8423,
      "std_r2": 0.0212
    }
  }
}
```

**Example cURL**:

```bash
curl -X GET "http://localhost:8000/api/v1/model-info"
```

---

## Interactive Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- View all endpoints
- See request/response schemas
- Test API calls directly in the browser
- Download OpenAPI specification

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider:

- Per-IP rate limits
- API key-based quotas
- Burst protection

## CORS

The API allows requests from:
- `http://localhost:3000` (React dev server)
- `http://localhost:5173` (Vite dev server)

To add more origins, update `backend/app/core/config.py`:

```python
cors_origins: List[str] = [
    "http://localhost:3000",
    "https://your-production-domain.com"
]
```

## Error Handling

All errors follow a consistent format:

```json
{
  "error": "ErrorType",
  "message": "Human-readable message",
  "detail": "Additional details (optional)"
}
```

**Common Error Types**:
- `ValidationError`: Invalid input data
- `PredictionError`: Error during prediction
- `InternalServerError`: Unexpected server error

## Best Practices

1. **Always validate input** on the client side before sending
2. **Handle errors gracefully** with user-friendly messages
3. **Implement retry logic** for transient failures
4. **Log all API calls** for debugging and monitoring
5. **Use HTTPS** in production
6. **Implement timeouts** to prevent hanging requests

## Versioning

The API uses URL versioning (`/api/v1/`). Future versions will be:
- `/api/v2/` - Breaking changes
- `/api/v1.1/` - Non-breaking additions

## Support

For issues or questions:
- Check the logs in `backend/logs/app.log`
- Review the Swagger documentation at `/docs`
- Ensure the model is trained and loaded

---

**API Version**: 1.0.0  
**Last Updated**: 2026-01-10
