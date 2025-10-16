import pathlib, os
from pathlib import Path

class Config:
    # Путь к проекту для анализа (измени на свой)
    #print('Введи полный путь к проекту. >>> ')
    PROJECT_PATH = Path(input('Введи полный путь к проекту. \n>>> '))
    

    # Модель Ollama
    OLLAMA_MODEL = "codellama:7b"  # или "llama3", "mistral" и т.д.
    OLLAMA_URL = "http://localhost:11434"
    
    # Игнорируемые папки и файлы
    IGNORE_PATTERNS = [
        "__pycache__", "*.pyc", ".git", "node_modules", 
        "venv", ".env", "*.log", "dist", "build"
    ]
    
    # Максимальный размер файла для чтения (в байтах)
    MAX_FILE_SIZE = 100000  # 100KB

    