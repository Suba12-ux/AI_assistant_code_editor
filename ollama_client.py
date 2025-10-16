import ollama
from config import Config

class OllamaClient:
    def __init__(self):
        self.model = Config.OLLAMA_MODEL
        self.client = ollama.Client(Config.OLLAMA_URL)
        
    def generate_response(self, prompt, context=""):
        """Генерирует ответ с помощью Ollama"""
        try:
            # Системный промпт для программирования
            system_prompt = f"""Ты - AI ассистент для программирования. У тебя есть доступ к файлам проекта.

Контекст проекта:
{context}

Отвечай кратко и по делу. Если нужно больше информации - попроси уточнить."""
            
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response['message']['content']
            
        except Exception as e:
            return f"Ошибка при обращении к Ollama: {e}"
    
    def list_models(self):
        """Показывает доступные модели"""
        try:
            models = self.client.list()
            return [model['name'] for model in models['models']]
        except Exception as e:
            return f"Ошибка: {e}"