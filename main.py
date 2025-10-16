from project_manager import ProjectManager
from ollama_client import OllamaClient
from config import Config
import os

def main():
    print("🚀 Запуск AI ассистента для программирования...")
    
    # Инициализация
    project_manager = ProjectManager()
    ollama_client = OllamaClient()
    
    # Проверяем доступные модели
    print("Проверяем доступные модели Ollama...")
    models = ollama_client.list_models()
    print(f"Доступные модели: {models}")
    
    # Сканируем проект
    project_tree = project_manager.scan_project()
    
    # Показываем структуру проекта
    print("\n📂 Структура проекта:")
    print(project_manager.format_file_tree())
    
    # Получаем ключевые файлы
    key_files = project_manager.get_key_files()
    print(f"\n🔑 Ключевые файлы для анализа: {len(key_files)}")
    
    # Основной цикл вопрос-ответ
    while True:
        print("\n" + "="*50)
        user_input = input("\n💬 Твой вопрос о проекте (или 'quit' для выхода): ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 До свидания!")
            break
            
        if not user_input:
            continue
        
        # Подготавливаем контекст проекта
        context = f"Структура проекта:\n{project_manager.format_file_tree()}\n\n"
        
        # Добавляем содержимое ключевых файлов
        context += "Содержимое ключевых файлов:\n"
        for file_path in key_files:
            content = project_manager.get_file_content(file_path)
            context += f"\n--- {file_path.relative_to(project_manager.project_path)} ---\n"
            context += content + "\n"
        
        # Генерируем ответ
        print("\n🤔 Думаю...")
        response = ollama_client.generate_response(user_input, context)
        
        print(f"\n💡 Ответ ассистента:\n{response}")

if __name__ == "__main__":
    main()