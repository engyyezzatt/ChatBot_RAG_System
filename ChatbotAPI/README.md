# Chatbot API (.NET Web API)

This is the .NET Web API component of the intelligent chatbot system that integrates with a Python RAG backend to provide intelligent responses based on document retrieval.

## Features

- **HTTP POST endpoint** for processing user questions
- **SQLite database integration** for storing user queries and chatbot responses (no manual setup required)
- **Python backend integration** via HTTP communication
- **Health monitoring** for both .NET API and Python backend
- **Swagger documentation** for API testing
- **CORS support** for frontend integration

## Prerequisites

- .NET 9.0 SDK
- Python backend running on `http://localhost:8000` (default, configurable)
- Python 3.11+ (for backend)

## Setup Instructions

### 1. Database Setup

**No manual setup required!**
- The API uses **SQLite** and will automatically create the database file at `Database/ChatbotDB.db` on first run.
- You do **not** need SQL Server or to run any SQL scripts.

### 2. Configuration

Update the connection string in `appsettings.json` if needed (default is SQLite):

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Data Source=../Database/ChatbotDB.db"
  },
  "PythonBackend": {
    "BaseUrl": "http://localhost:8000" // Change if your Python backend runs elsewhere
  }
}
```

### 3. Build and Run

```bash
# Navigate to the ChatbotAPI directory
cd ChatbotAPI

dotnet restore
dotnet build
dotnet run
```

The API will be available at:
- **API Base URL**: `http://localhost:5001` (or `https://localhost:7001`)
- **Swagger UI**: `http://localhost:5001/swagger`

## API Endpoints

### POST /api/chat
Process a user question and return an AI response.

**Request Body:**
```json
{
  "question": "What is the company leave policy?",
  "sessionId": "123e4567-e89b-12d3-a456-426614174000"
}
```
- `sessionId` should be a valid UUID (Guid). If not provided, the backend will generate a new one for the session.

**Response Example:**
```json
{
  "queryId": 1,
  "question": "What is the company leave policy?",
  "response": "Based on the HR policy document, employees are entitled to 20 days of annual leave per year.",
  "questionTimestamp": "2024-01-15T10:30:00Z",
  "responseTimestamp": "2024-01-15T10:30:02Z",
  "processingTimeSeconds": 15,
  "sources": ["HR_Policy_Dataset1.txt"],
  "status": "Success"
}
```
> **Note:** JSON fields use camelCase by default (e.g., `processingTimeSeconds`).


### GET /api/health
Check the health status of both .NET API and Python backend.

**Response Example:**
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "dotnet_api": {
    "status": "healthy",
    "version": "1.0.0"
  },
  "python_backend": {
    "status": "healthy",
    "vector_store_status": "ready"
  }
}
```

## Database Schema

### UserQueries Table
- `QueryId` (Primary Key)
- `Question` (User's question)
- `Timestamp` (When the question was asked)
- `SessionId` (Session tracking, Guid/UUID)
- `Status` (Pending, Processing, Completed, Failed)

### ChatbotResponses Table
- `ResponseId` (Primary Key)
- `QueryId` (Foreign Key to UserQueries)
- `Response` (AI-generated response)
- `Timestamp` (When the response was generated)
- `ProcessingTimeSeconds` (Time taken to process, double)
- `Sources` (JSON array of source documents)
- `Status` (Success, Error)
- `ErrorMessage` (Error details if failed)

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input data
- **503 Service Unavailable**: Python backend communication issues
- **500 Internal Server Error**: Unexpected errors

All errors are logged and include appropriate error messages.

## Logging

The application uses structured logging with different levels:
- **Information**: Normal operations
- **Warning**: Non-critical issues
- **Error**: Errors that need attention
- **Debug**: Detailed information (development only)

## CORS Configuration

CORS is configured to allow requests from common frontend development ports:
- `http://localhost:3000` (React default)
- `http://localhost:4200` (Angular default)
- HTTPS variants of the above

## Testing

### Using Swagger UI
1. Navigate to `http://localhost:5001/swagger` (or `https://localhost:7001/swagger`)
2. Test the endpoints directly from the browser

### Using curl
```bash
# Send a chat request
curl -X POST "http://localhost:5001/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the company leave policy?", "sessionId": "123e4567-e89b-12d3-a456-426614174000"}'


# Check health
curl "http://localhost:5001/api/health"
```

### Automated Test Script
You can run the full system test from the project root:
```bash
python Tests/test_api.py
```
This will test health, chat, and database endpoints end-to-end.

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure the API can write to `Database/ChatbotDB.db`
   - Check connection string in `appsettings.json`
   - The database file is created automatically on first run

2. **Python Backend Connection Error**
   - Ensure Python backend is running on `http://localhost:8000`
   - Check Python backend health endpoint
   - Update `PythonBackend:BaseUrl` in `appsettings.json` if needed

3. **CORS Issues**
   - Update `appsettings.json` with your frontend URL
   - Ensure frontend is making requests from allowed origins

### Logs
Check the console output for detailed error messages and logs.

## Architecture

The application follows a clean architecture pattern:

- **Controllers**: Handle HTTP requests and responses
- **Services**: Business logic and external service integration
- **Models**: Entity Framework entities
- **DTOs**: Data transfer objects for API communication
- **Data**: Database context and configuration

## Dependencies

- **Microsoft.EntityFrameworkCore.Sqlite**: Database access (SQLite)
- **Microsoft.AspNetCore.OpenApi**: API documentation
- **Swashbuckle.AspNetCore**: Swagger UI
- **System.Text.Json**: JSON serialization 