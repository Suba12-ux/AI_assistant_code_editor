import os
import fnmatch
from pathlib import Path
from config import Config

class ProjectManager:
    def __init__(self, project_path=None):
        self.project_path = project_path or Config.PROJECT_PATH
        self.file_tree = {}
        self.all_files = []
        
    def should_ignore(self, path):
        """Проверяет, нужно ли игнорировать файл/папку"""
        for pattern in Config.IGNORE_PATTERNS:
            if fnmatch.fnmatch(path.name, pattern) or pattern in str(path):
                return True
        return False
    
    def scan_project(self):
        """Рекурсивно сканирует проект и строит дерево файлов"""
        print(f"🔍 Сканирую проект: {self.project_path}")
        
        self.file_tree = self._scan_directory(self.project_path)
        return self.file_tree
    
    def _scan_directory(self, directory, level=0):
        """Рекурсивно сканирует директорию"""
        result = {}
        
        try:
            items = sorted(os.listdir(directory))
        except PermissionError:
            return {"error": f"Permission denied: {directory}"}
        
        for item in items:
            item_path = Path(directory) / item
            
            if self.should_ignore(item_path):
                continue
                
            if item_path.is_dir():
                result[item] = {
                    "type": "directory",
                    "content": self._scan_directory(item_path, level + 1)
                }
            else:
                result[item] = {
                    "type": "file",
                    "size": item_path.stat().st_size
                }
                self.all_files.append(item_path)
        
        return result
    
    def get_file_content(self, file_path, max_lines=200):
        """Читает содержимое файла с ограничением по размеру"""
        try:
            if file_path.stat().st_size > Config.MAX_FILE_SIZE:
                return f"Файл слишком большой ({file_path.stat().st_size} байт). Пропускаю..."
                
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Ограничиваем количество строк
                lines = content.split('\n')
                if len(lines) > max_lines:
                    return '\n'.join(lines[:max_lines]) + f"\n\n... и еще {len(lines) - max_lines} строк"
                return content
                
        except Exception as e:
            return f"Ошибка чтения файла: {e}"
    
    def format_file_tree(self, tree=None, indent=0):
        """Форматирует дерево файлов в читаемую строку"""
        if tree is None:
            tree = self.file_tree
            
        result = ""
        prefix = "  " * indent
        
        for name, info in tree.items():
            if info["type"] == "directory":
                result += f"{prefix}📁 {name}/\n"
                result += self.format_file_tree(info["content"], indent + 1)
            else:
                result += f"{prefix}📄 {name} ({info['size']} байт)\n"
                
        return result
    
    def find_files_by_extension(self, extension):
        """Находит все файлы с определенным расширением"""
        return [f for f in self.all_files if f.suffix == extension]
    
    def get_key_files(self):
        """Возвращает ключевые файлы проекта"""
        key_files = []
        priority_extensions = ['.py', '.js', '.ts', '.json', '.md', 'Dockerfile', 'requirements.txt']
        
        for ext in priority_extensions:
            key_files.extend(self.find_files_by_extension(ext))
            
        # Ограничиваем количество файлов для первого анализа
        return key_files[:10]