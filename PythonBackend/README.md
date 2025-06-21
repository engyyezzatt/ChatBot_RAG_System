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
   # Then pull a model (e.g., llama2 or llama3)
   ollama pull llama2
   # or
   ollama pull llama3
   ```

2. **Python Dependencies**: Install required packages
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The backend uses the following default settings (can be overridden via `.env` file):

- **Ollama URL**: `http://localhost:11434`
- **Model**: `llama2` (change to `llama3` if you have it)
- **Documents**: `docs/` directory
- **Vector Store**: `./vector_store/`
- **API Port**: `8000`

## Setup

1. **Add Documents**: Place your `.txt` files in the `docs/` directory
2. **Test Setup**: Run the test script to verify everything works
   ```bash
   python test_setup.py
   ```
3. **Start Server**: Run the FastAPI server
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

- **Health Check**: `GET /health`
- **Chat**: `POST /chat`
- **Documentation**: `GET /docs` (Swagger UI)

### Chat Request Example

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is the main topic of your documents?"}'
```

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
├── tests/                   # Test scripts
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Troubleshooting

1. **Ollama Connection Issues**: Make sure Ollama is running on port 11434
2. **Model Not Found**: Pull the required model with `ollama pull <model_name>`
3. **Document Issues**: Ensure `.txt` files exist in the `docs/` directory
4. **Port Conflicts**: Change the port in settings or use `--port` flag with uvicorn

## Development

- **Auto-reload**: Use `--reload` flag for development
- **Logging**: Check console output for detailed logs
- **Testing**: Use the test script to verify setup before running 