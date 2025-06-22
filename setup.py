"""
Setup script for Chatbot RAG System
This script helps set up the Python environment and install dependencies.
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return the result."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, cwd=cwd)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e}")
        print(f"Error output: {e.stderr}")
        return None

def create_virtual_environment():
    """Create a virtual environment if it doesn't exist."""
    venv_path = Path("PythonBackend/ragsystem_env")
    
    if venv_path.exists():
        print("Virtual environment already exists.")
        return True
    
    print("Creating virtual environment...")
    try:
        venv.create("PythonBackend/ragsystem_env", with_pip=True)
        print("Virtual environment created successfully.")
        return True
    except Exception as e:
        print(f"Error creating virtual environment: {e}")
        return False

def install_requirements():
    """Install Python requirements."""
    print("Installing Python requirements...")
    
    # Determine the pip command based on the OS
    if os.name == 'nt':  # Windows
        pip_cmd = "PythonBackend\\ragsystem_env\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_cmd = "PythonBackend/ragsystem_env/bin/pip"
    
    requirements_file = "PythonBackend/requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"Requirements file not found: {requirements_file}")
        return False
    
    result = run_command(f"{pip_cmd} install -r {requirements_file}")
    if result:
        print("Requirements installed successfully.")
        return True
    else:
        print("Failed to install requirements.")
        return False

def main():
    """Main setup function."""
    print(" Setting up Chatbot RAG System...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("PythonBackend"):
        print("Error: Please run this script from the project root directory.")
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Update PythonBackend/.env with your OpenAI API key")
    print("2. Start the Python backend:")
    print("   cd PythonBackend")
    print("   ragsystem_env\\Scripts\\activate  # Windows")
    print("   source ragsystem_env/bin/activate  # macOS/Linux")
    print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    print("3. Start the .NET API:")
    print("   cd ChatbotAPI")
    print("   dotnet run")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main() 