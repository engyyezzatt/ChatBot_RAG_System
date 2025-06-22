@echo off
REM Change to the directory where this script is located
cd /d "%~dp0"

REM --- PYTHON BACKEND SETUP ---
cd PythonBackend

REM Create venv if it doesn't exist
if not exist "ragsystem_env" (
    echo Creating Python virtual environment...
    python -m venv ragsystem_env
)

REM Activate venv and install requirements
call ragsystem_env\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

REM Deactivate venv (optional, just to clean up main window)
call ragsystem_env\Scripts\deactivate.bat

cd ..

REM --- START PYTHON BACKEND IN NEW WINDOW ---
start cmd /k "cd /d %cd%\PythonBackend && call ragsystem_env\Scripts\activate && uvicorn app.main:app --reload"

REM --- START .NET BACKEND IN NEW WINDOW ---
start cmd /k "cd /d %cd%\ChatbotAPI && dotnet run"

REM --- OPEN SWAGGER UI ---
timeout /t 8 >nul
start http://localhost:5001/swagger

echo All services started! You can now test the endpoints in Swagger.
pause