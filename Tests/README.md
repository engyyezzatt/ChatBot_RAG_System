# 🧪 Test Files

This directory contains test scripts for validating the Chatbot System components.

##  Test Files Overview

### `test_api.py`
**Purpose**: Tests the .NET Web API endpoints
- **What it tests**: Health checks, database connection, chat functionality, conversation history
- **When to use**: After starting the .NET API to verify all endpoints work correctly
- **Usage**: `python test_api.py`

### `test_python_backend.py`
**Purpose**: Tests the Python RAG backend directly
- **What it tests**: Python backend health and chat endpoints (bypasses .NET API)
- **When to use**: To isolate whether issues are with the .NET API or Python backend
- **Usage**: `python test_python_backend.py`

### `view_database.py`
**Purpose**: Interactive SQLite database viewer
- **What it shows**: Database contents, conversation history, user queries, chatbot responses
- **When to use**: To inspect what data is being stored in the database
- **Usage**: `python view_database.py`

##  Quick Test Workflow

1. **Start the Python Backend**:
   ```bash
   cd ../PythonBackend
   python -m uvicorn app.main:app --reload
   ```

2. **Test Python Backend** (optional):
   ```bash
   python test_python_backend.py
   ```

3. **Start the .NET API**:
   ```bash
   cd ../ChatbotAPI
   dotnet run
   ```

4. **Test the Full System**:
   ```bash
   python test_api.py
   ```

5. **View Database Contents** (optional):
   ```bash
   python view_database.py
   ```

##  Troubleshooting

### If `test_python_backend.py` fails:
- Check if Python backend is running on `http://localhost:8000`
- Verify the virtual environment is activated
- Check Python backend console for errors

### If `test_api.py` fails:
- Check if .NET API is running (usually on `http://localhost:5001`)
- Verify Python backend is running on `http://localhost:8000`
- Check .NET API console for errors

### If `view_database.py` shows no data:
- Make sure the .NET API has been run at least once
- The database file should be created at `../ChatbotAPI/ChatbotDB.db`
- Run some chat requests first to populate the database

## 📊 Expected Test Results

### Successful `test_api.py` run:
```
✅ Health check passed
✅ Database connection successful
✅ Chat request successful
✅ Database verification successful
✅ History request successful
   All tests passed!
```

### Successful `test_python_backend.py` run:
```
✅ Health check passed
✅ Chat request successful
✅ Python backend is working correctly!
```

### Database viewer should show:
- UserQueries table with recent questions
- ChatbotResponses table with AI responses
- Conversation history with both queries and responses 