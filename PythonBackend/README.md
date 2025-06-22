# Python RAG Backend

A FastAPI-based backend for Retrieval-Augmented Generation (RAG) using Ollama and LangChain.

## Features

- **Ollama Integration**: Uses Ollama for local LLM inference
- **Document Processing**: Loads and processes text documents
- **Vector Store**: Uses ChromaDB for document embeddings and retrieval
- **RAG Pipeline**: Retrieves relevant context and generates responses
- **Health Checks**: Monitors service status and dependencies

## Prerequisites

1. **Ollama**: Install and run Ollama locally
   ```bash
   # Install Ollama from https://ollama.ai/
   # Then pull a model (e.g., llama3)
   ollama pull llama3
   ```
   > **Note:** The default model is `llama3` (see .env example below).

2. **Python Dependencies**: Install required packages
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The backend uses the following default settings (can be overridden via a `.env` file):

- **OLLAMA_URL**: `http://localhost:11434`
- **OLLAMA_MODEL**: `llama3` 
- **VECTOR_STORE_PATH**: `./vector_store/`
- **API_PORT**: `8000`

### Example `.env` file
```
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3
DOCS_PATH=docs/
VECTOR_STORE_PATH=./vector_store/
API_PORT=8000
```

## Setup

1. **Add Documents**: Place your `.txt` files in the `docs/` directory
2. **Test Setup**: Run the test script to verify everything works
   ```bash
   python ../Tests/test_python_backend.py
   ```
   > **Note:** Test scripts are located in the root-level `Tests/` directory, not in `PythonBackend/`.
3. **Start Server**: Run the FastAPI server
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

- **Health Check**: `GET /health`
- **Chat**: `POST /chat` (requires `question` and `session_id` fields)
- **Documentation**: `GET /docs` (Swagger UI)

### Chat Request Example

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
           "question": "What is the main topic of your documents?",
           "session_id": "123e4567-e89b-12d3-a456-426614174000"
         }'
```
> **Note:** `session_id` must be a valid UUID4 string. You can generate one in Python with:
> ```python
> import uuid; print(uuid.uuid4())
> ```

## Project Structure

```
Chatbot_RAG_System/PythonBackend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config/
│   │   └── settings.py      # Configuration settings
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   └── services/
│       ├── rag_service.py   # RAG pipeline logic
│       └── document_processor.py  # Document processing
├── docs/                    # Document files (.txt)
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Troubleshooting

1. **Ollama Connection Issues**: Make sure Ollama is running on port 11434
2. **Model Not Found**: Pull the required model with `ollama pull <model_name>`
3. **Document Issues**: Ensure `.txt` files exist in the `docs/` directory
4. **Port Conflicts**: Change the port in settings, `.env`, or use `--port` flag with uvicorn

## Development

- **Auto-reload**: Use `--reload` flag for development
- **Logging**: Check console output for detailed logs
- **Testing**: Use the test script in `../Tests/` to verify setup before running 