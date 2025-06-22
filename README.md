# Chatbot RAG System

A Retrieval-Augmented Generation (RAG) chatbot system built with a .NET API and a Python backend. This project uses local policy documents to provide context-aware answers to user questions.

## 🚀 Core Features

-   **.NET 8 Web API**: Handles user interactions, session management, and database storage.
-   **Python & FastAPI Backend**: Powers the core RAG logic using LangChain and an LLM.
-   **SQLite Database**: Stores conversation history for easy retrieval and review.
-   **Vector Storage**: Uses ChromaDB to store document embeddings for efficient retrieval.
-   **Automated Setup**: Includes scripts to simplify environment setup.
-   **Comprehensive Testing**: Contains scripts to test the API, backend, and view the database.

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
└── README.md
```

## 🛠️ Prerequisites

-   .NET 8 SDK (or later)
-   Python 3.11 (or later)
-   Git

## 📦 Installation & Setup

This project includes a setup script to automate the Python environment creation.

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/engyyezzatt/ChatBot_RAG_System.git
    cd Chatbot_RAG_System
    ```

2.  **Run the Python Setup Script**
    This script will create a virtual environment, install dependencies, and generate a `.env` file for you.

    ```bash
    python setup.py
    ```

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

4.  **Build the .NET API**
    This step prepares the C# project.

    ```bash
    cd ChatbotAPI
    dotnet build
    cd ..
    ```

## 🚀 Running the Application

Both the Python backend and the .NET API must be running for the system to work.

1.  **Start the Python Backend**
    This service handles the AI-powered chat logic.

    ```bash
    cd PythonBackend
    # Activate virtual environment
    # On Windows:
    ragsystem_env\Scripts\activate
    # On macOS/Linux:
    source ragsystem_env/bin/activate

    # Start the FastAPI server
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    The backend will automatically process the documents in `PythonBackend/docs` and create a vector store.

2.  **Start the .NET API**
    In a **new terminal**, navigate to the API directory and run the application.

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