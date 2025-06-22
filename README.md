# Chatbot RAG System

A Retrieval-Augmented Generation (RAG) chatbot system built with a .NET API and a Python backend. This project uses local policy documents to provide context-aware answers to user questions.

## 🚀 Core Features

-   **.NET 8 Web API**: Handles user interactions, session management, and database storage.
-   **Python & FastAPI Backend**: Powers the core RAG logic using LangChain and an LLM.
-   **SQLite Database**: Stores conversation history for easy retrieval and review.
-   **Vector Storage**: Uses ChromaDB to store document embeddings for efficient retrieval.
-   **Automated Setup**: Includes scripts to simplify environment setup.
-   **Comprehensive Testing**: Contains scripts to test the API, backend, and view the database.

## ⚡ Quick Start: Automated vs. Manual Setup

You can set up and run the project in two ways:

### 1. **Automated (Windows Only): `run_api.bat`**
- **One-click solution for Windows users**
- Creates the Python virtual environment (if needed)
- Installs Python dependencies
- Starts the Python backend in a new window
- Starts the .NET API in a new window
- Opens the Swagger UI in your browser
- **Recommended for most Windows users**

### 2. **Manual/Cross-platform: `setup.py` & Step-by-Step**
- **Works on Windows, macOS, and Linux**
- `setup.py` creates the Python virtual environment and installs dependencies
- You manually start the Python backend and .NET API in separate terminals
- Useful for advanced users or non-Windows systems

| Feature                  | run_api.bat (Windows) | setup.py (Cross-platform) |
|--------------------------|:---------------------:|:-------------------------:|
| Creates venv             |          ✅           |            ✅             |
| Installs requirements    |          ✅           |            ✅             |
| Starts Python backend    |          ✅           |            ❌             |
| Starts .NET API          |          ✅           |            ❌             |
| Opens Swagger UI         |          ✅           |            ❌             |
| One-click experience     |          ✅           |            ❌             |
| Works on Linux/macOS     |          ❌           |            ✅             |

---

## 📁 Project Structure

```
Chatbot_RAG_System/
├── ChatbotAPI/         # .NET Web API
│   ├── Controllers/
│   ├── Data/           # DbContext for SQLite
│   ├── Models/         # C# data models
│   ├── Services/
│   └── Program.cs      # App startup and configuration
├── Database/           # Contains the SQLite database file
│   └── ChatbotDB.db    # (created automatically on first run)
├── PythonBackend/      # Python RAG backend
│   ├── app/            # FastAPI application
│   ├── docs/           # Source documents for the RAG system
│   └── vector_store/   # ChromaDB vector storage
├── Tests/                # Python test and utility scripts
│   ├── test_api.py
│   ├── test_python_backend.py
│   └── view_database.py
├── setup.py            # Python environment setup script
├── run_api.bat         # Windows batch file for full automation
└── README.md
```

## 🛠️ Prerequisites

-   .NET 8 SDK (or later)
-   Python 3.11 (or later)
-   Git

## 📦 Installation & Setup

### **Option 1: Automated Setup (Windows Only)**

1. **Clone the Repository**
    ```bash
    git clone https://github.com/engyyezzatt/ChatBot_RAG_System.git
    cd Chatbot_RAG_System
    ```
2. **Run the Batch File**
    ```bash
    run_api.bat
    ```
    This will:
    - Create the Python virtual environment (if needed)
    - Install dependencies
    - Start both backends in new windows
    - Open Swagger UI for testing

### **Option 2: Manual/Cross-platform Setup**

1. **Clone the Repository**
    ```bash
    git clone https://github.com/engyyezzatt/ChatBot_RAG_System.git
    cd Chatbot_RAG_System
    ```
2. **Run the Python Setup Script**
    ```bash
    python setup.py
    ```
    Or, do it step-by-step:
    ```bash
    cd PythonBackend
    python -m venv ragsystem_env
    # Activate virtual environment
    # On Windows:
    ragsystem_env\Scripts\activate
    # On macOS/Linux:
    source ragsystem_env/bin/activate
    pip install -r requirements.txt
    ```
3. **Build the .NET API**
    ```bash
    cd ChatbotAPI
    dotnet build
    cd ..
    ```

## 🚀 Running the Application

Both the Python backend and the .NET API must be running for the system to work.

### **If you used `run_api.bat` (Windows):**
- Both services and Swagger UI will start automatically in new windows.

### **If you used manual setup:**
1. **Start the Python Backend**
    ```bash
    cd PythonBackend
    # Activate virtual environment
    # On Windows:
    ragsystem_env\Scripts\activate
    # On macOS/Linux:
    source ragsystem_env/bin/activate
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
2. **Start the .NET API**
    In a **new terminal**, navigate to the API directory and run:
    ```bash
    cd ChatbotAPI
    dotnet run
    ```
    The API will be available at `http://localhost:5001`. The SQLite database file (`ChatbotDB.db`) will be created automatically in the `Database` directory the first time the API starts.

## 🧪 Testing & Verification

The `Tests` directory contains scripts to verify that the system is working correctly.

-   **Test the Full System**:
    Run `Tests/test_api.py` to perform an end-to-end test that sends a message to the .NET API, which then calls the Python backend.
    ```bash
    python Tests/test_api.py
    ```

-   **View Database Contents**:
    Run `Tests/view_database.py` to inspect the queries and responses stored in the SQLite database.
    ```bash
    python Tests/view_database.py
    ```

## 🌐 API Endpoints

-   **.NET API**: `http://localhost:5001`
    -   `GET /swagger`: View interactive API documentation.
    -   `GET /api/health`: Health check for the API and its connection to the Python backend.
    -   `POST /api/chat`: Send a chat message.
-   **Python Backend**: `http://localhost:8000`
    -   `GET /docs`: View interactive backend API documentation.
    -   `POST /chat`: The internal endpoint used by the .NET API for RAG processing. 