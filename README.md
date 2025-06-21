# Chatbot RAG System

A comprehensive Retrieval-Augmented Generation (RAG) chatbot system built with .NET Core API and Python backend, featuring document processing, vector storage, and intelligent query responses.

## 🚀 Features

- **Dual Backend Architecture**: .NET Core API for web interface + Python backend for RAG processing
- **Document Processing**: Automatic ingestion and processing of HR policy documents
- **Vector Storage**: ChromaDB-based vector database for efficient document retrieval
- **Intelligent Responses**: Context-aware responses using LangChain and OpenAI
- **RESTful API**: Clean API endpoints for chat interactions
- **Database Integration**: SQL Server database for conversation history
- **Comprehensive Testing**: Unit tests for both API and Python backend

## 📁 Project Structure

```
Chatbot_RAG_System/
├── ChatbotAPI/                 # .NET Core Web API
│   ├── Controllers/            # API endpoints
│   ├── Services/              # Business logic services
│   ├── Models/                # Data models
│   ├── DTOs/                  # Data transfer objects
│   └── Data/                  # Database context
├── PythonBackend/             # Python RAG backend
│   ├── app/                   # Main application
│   │   ├── services/          # RAG and document processing
│   │   ├── models/            # Pydantic schemas
│   │   └── config/            # Configuration settings
│   ├── docs/                  # Sample HR policy documents
│   └── requirements.txt       # Python dependencies
├── Database/                  # SQL database scripts
├── Tests/                     # Test files
└── README.md                  # This file
```

## 🛠️ Prerequisites

- **.NET 9.0 SDK**
- **Python 3.11+**
- **SQL Server** (or SQL Server Express)
- **Git**

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Chatbot_RAG_System.git
cd Chatbot_RAG_System
```

### 2. Setup .NET API

```bash
cd ChatbotAPI
dotnet restore
dotnet build
```

### 3. Setup Python Backend

```bash
cd PythonBackend

# Create virtual environment
python -m venv ragsystem_env

# Activate virtual environment
# On Windows:
ragsystem_env\Scripts\activate
# On macOS/Linux:
source ragsystem_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Database Setup

1. Create a SQL Server database
2. Update connection string in `ChatbotAPI/appsettings.json`
3. Run the database migration:
   ```bash
   cd ChatbotAPI
   dotnet ef database update
   ```

### 5. Environment Configuration

Create environment files for sensitive data:

**Python Backend** (`.env` file in `PythonBackend/`):
```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=your_database_connection_string
```

**C# API** (update `appsettings.json`):
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "your_database_connection_string"
  },
  "PythonBackendUrl": "http://localhost:8000"
}
```

## 🚀 Running the Application

### 1. Start Python Backend

```bash
cd PythonBackend
# Activate virtual environment first
ragsystem_env\Scripts\activate  # Windows
# source ragsystem_env/bin/activate  # macOS/Linux

# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start .NET API

```bash
cd ChatbotAPI
dotnet run
```

The API will be available at `https://localhost:7001` (or the configured port).

## 📚 API Usage

### Chat Endpoint

**POST** `/api/chat`

Request body:
```json
{
  "message": "What is the company's vacation policy?",
  "userId": "user123"
}
```

Response:
```json
{
  "response": "Based on our HR policies, employees are entitled to...",
  "timestamp": "2024-01-15T10:30:00Z",
  "userId": "user123"
}
```

### Health Check

**GET** `/api/health`

Returns the health status of both the API and Python backend.

## 🧪 Testing

### Run .NET Tests
```bash
cd ChatbotAPI
dotnet test
```

### Run Python Tests
```bash
cd PythonBackend
# Activate virtual environment first
python -m pytest
```

## 🔧 Configuration

### Python Backend Settings

Edit `PythonBackend/app/config/settings.py` to configure:
- Model parameters
- Vector store settings
- API endpoints

### .NET API Settings

Edit `ChatbotAPI/appsettings.json` to configure:
- Database connection
- Python backend URL
- Logging settings

## 📝 Adding Documents

1. Place your documents in the `PythonBackend/docs/` directory
2. Supported formats: `.txt`, `.pdf`, `.docx`
3. The system will automatically process and index new documents

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/yourusername/Chatbot_RAG_System/issues) page
2. Create a new issue with detailed information
3. Include error logs and system information

## 🔄 Updates

- **v1.0.0**: Initial release with basic RAG functionality
- **v1.1.0**: Added comprehensive testing suite
- **v1.2.0**: Enhanced document processing and vector storage

---

**Note**: Make sure to never commit sensitive information like API keys or database credentials. Use environment variables and `.env` files for configuration.

## 🌐 API Endpoints

### .NET API (http://localhost:5001)
- `GET /` - API information
- `GET /swagger` - API documentation
- `GET /api/health` - Health check
- `POST /api/chat` - Process chat request
- `GET /api/chat/history` - Get conversation history
- `GET /api/chat/db-stats` - Database statistics

### Python Backend (http://localhost:8000)
- `GET /` - Backend information
- `GET /docs` - API documentation
- `GET /health` - Health check
- `POST /chat` - Process RAG request

## 🔍 Troubleshooting

### Common Issues

#### 1. Python Backend Not Starting
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <PID> /F
```

#### 2. .NET API Not Starting
```bash
# Check if port 5001 is in use
netstat -ano | findstr :5001

# Clean and rebuild
dotnet clean
dotnet restore
dotnet build
```

#### 3. Database Connection Issues
- Ensure SQLite is working (included with .NET)
- Check file permissions for `ChatbotDB.db`
- Verify connection string in `appsettings.json`

#### 4. Timeout Issues
- Increase timeout in `appsettings.json`
- Check Python backend performance
- Monitor vector store initialization

### Debug Steps

1. **Test Python Backend Directly**:
   ```bash
   cd Chatbot_RAG_System/Tests
   python test_python_backend.py
   ```

2. **Check .NET API Logs**:
   - Look for detailed error messages in console
   - Check database creation messages

3. **Verify Database**:
   ```bash
   cd Chatbot_RAG_System/Tests
   python view_database.py
   ```

4. **Test Individual Components**:
   - Health check: `curl http://localhost:5001/api/health`
   - Python health: `curl http://localhost:8000/health`

## 📈 Performance Monitoring

### Response Times
- **Typical**: 2-5 seconds for first request
- **Subsequent**: 1-3 seconds (vector store cached)
- **Timeout**: 60 seconds (configurable)

### Database Performance
- **SQLite**: Fast for development
- **Indexes**: On Timestamp and SessionId columns
- **Storage**: Local file (`ChatbotDB.db`) 