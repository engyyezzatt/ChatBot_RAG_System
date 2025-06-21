# Chatbot API (.NET Web API)

This is the .NET Web API component of the intelligent chatbot system that integrates with a Python RAG backend to provide intelligent responses based on document retrieval.

## Features

- **HTTP POST endpoint** for processing user questions
- **Database integration** for storing user queries and chatbot responses
- **Python backend integration** via HTTP communication
- **Conversation history** retrieval
- **Health monitoring** for both .NET API and Python backend
- **Swagger documentation** for API testing
- **CORS support** for frontend integration

## Prerequisites

- .NET 8.0 SDK
- SQL Server (LocalDB, Express, or full version)
- Python backend running on `http://localhost:8000`

## Setup Instructions

### 1. Database Setup

1. Open SQL Server Management Studio or use the command line
2. Run the SQL script located at `../Database/ChatbotDatabase.sql`
3. This will create the `ChatbotDB` database with the required tables

### 2. Configuration

Update the connection string in `appsettings.json` if needed:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=ChatbotDB;Trusted_Connection=true;TrustServerCertificate=true;MultipleActiveResultSets=true"
  }
}
```

### 3. Build and Run

```bash
# Navigate to the ChatbotAPI directory
cd src/ChatbotAPI

# Restore packages
dotnet restore

# Build the project
dotnet build

# Run the application
dotnet run
```

The API will be available at:
- **API Base URL**: `https://localhost:7001` (or `http://localhost:5001`)
- **Swagger UI**: `https://localhost:7001/swagger`

## API Endpoints

### POST /api/chat
Process a user question and return an AI response.

**Request Body:**
```json
{
  "question": "What is the company leave policy?",
  "sessionId": "session-123",
  "userId": "user-456"
}
```

**Response:**
```json
{
  "queryId": 1,
  "question": "What is the company leave policy?",
  "response": "Based on the HR policy document, employees are entitled to 20 days of annual leave per year.",
  "questionTimestamp": "2024-01-15T10:30:00Z",
  "responseTimestamp": "2024-01-15T10:30:02Z",
  "processingTimeMs": 1500,
  "sources": ["HR_Policy_Dataset1.txt"],
  "status": "Success"
}
```

### GET /api/chat/history
Retrieve conversation history.

**Query Parameters:**
- `sessionId` (optional): Filter by session ID
- `limit` (optional): Maximum number of records (default: 50, max: 100)

**Response:**
```json
[
  {
    "queryId": 1,
    "question": "What is the company leave policy?",
    "response": "Based on the HR policy document...",
    "questionTimestamp": "2024-01-15T10:30:00Z",
    "responseTimestamp": "2024-01-15T10:30:02Z",
    "processingTimeMs": 1500,
    "sources": ["HR_Policy_Dataset1.txt"],
    "status": "Success"
  }
]
```

### GET /api/health
Check the health status of both .NET API and Python backend.

**Response:**
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
- `SessionId` (Optional session tracking)
- `UserId` (Optional user identification)
- `Status` (Pending, Processing, Completed, Failed)

### ChatbotResponses Table
- `ResponseId` (Primary Key)
- `QueryId` (Foreign Key to UserQueries)
- `Response` (AI-generated response)
- `Timestamp` (When the response was generated)
- `ProcessingTimeMs` (Time taken to process)
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
1. Navigate to `https://localhost:7001/swagger`
2. Test the endpoints directly from the browser

### Using curl
```bash
# Send a chat request
curl -X POST "https://localhost:7001/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the company leave policy?", "sessionId": "test-session"}'

# Get conversation history
curl "https://localhost:7001/api/chat/history?limit=10"

# Check health
curl "https://localhost:7001/api/health"
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure SQL Server is running
   - Check connection string in `appsettings.json`
   - Verify database exists

2. **Python Backend Connection Error**
   - Ensure Python backend is running on `http://localhost:8000`
   - Check Python backend health endpoint

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

- **Microsoft.EntityFrameworkCore.SqlServer**: Database access
- **Microsoft.AspNetCore.OpenApi**: API documentation
- **Swashbuckle.AspNetCore**: Swagger UI
- **System.Text.Json**: JSON serialization 