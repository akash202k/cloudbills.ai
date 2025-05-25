# AWS Cost Analysis Backend

A FastAPI-based backend service for analyzing AWS costs with plans to support Azure and GCP in the future.

## Features

- AWS Cost Explorer integration for detailed cost analysis
- RESTful API endpoints for cost data retrieval
- API key authentication
- Response caching for improved performance
- Comprehensive error handling and logging
- OpenAPI documentation

## Project Structure

```
aws/
├── api/
│   └── v1/
│       └── endpoints/
│           └── costs.py         # Cost analysis endpoints
├── models/
│   └── cost.py                 # Pydantic models for cost data
├── services/
│   └── cost_explorer.py        # AWS Cost Explorer service
├── config.py                   # Application configuration
├── main.py                     # FastAPI application setup
└── README.md                   # This file
```

## API Endpoints

### Cost Summary
- **Endpoint**: `POST /api/v1/costs/cost-summary`
- **Authentication**: Required (X-API-Key header)
- **Request Body**:
  ```json
  {
    "start_date": "2024-01-01T00:00:00Z",
    "end_date": "2024-01-31T23:59:59Z",
    "granularity": "MONTHLY",
    "group_by": ["SERVICE", "REGION"]
  }
  ```
- **Response**: Cost summary with detailed breakdown

### Health Check
- **Endpoint**: `GET /health`
- **Authentication**: None
- **Response**: Service health status

## Configuration

The application uses environment variables for configuration. Create a `.env` file with the following variables:

```env
API_KEY=your_api_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_preferred_region
```

## Development Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   uvicorn aws.main:app --reload
   ```

4. Access the API documentation:
   - Swagger UI: http://localhost:8000/api/v1/docs
   - ReDoc: http://localhost:8000/api/v1/redoc

## Code Standards

- Type hints for all functions
- Async/await for endpoint handlers
- PEP 8 style guide compliance
- Comprehensive docstrings
- Proper error handling with HTTP status codes
- Input validation using Pydantic models

## Security

- API key authentication
- Environment variables for sensitive data
- Input validation and sanitization
- Rate limiting implementation
- No exposure of AWS credentials in responses

## Performance

- Response caching for frequently accessed data
- Connection pooling for AWS clients
- Request/response timing monitoring
- Pagination for large result sets

## Future Plans

- Azure cost analysis integration
- GCP cost analysis integration
- Enhanced caching strategies
- Additional cost analysis metrics
- Cost optimization recommendations

## Contributing

1. Follow the existing code structure and standards
2. Add type hints and docstrings to all new code
3. Include proper error handling
4. Write tests for new functionality
5. Update documentation as needed 