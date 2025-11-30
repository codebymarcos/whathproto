"""Operações de gerenciamento de arquivos."""
from pathlib import Path

def delete(base_path, filename):
    """Deleta um arquivo."""
    file_path = base_path / filename
    try:
        if file_path.exists():
            file_path.unlink()
            return True
    except Exception as e:
        print(f"Erro ao deletar arquivo {filename}: {e}")
    return False

def list_contents(path):
    """Lista conteúdo de um diretório."""
    contents = []
    try:
        if path.exists():
            for item in path.iterdir():
                info = {
                    'name': item.name,
                    'path': str(item),
                    'is_dir': item.is_dir(),
                    'is_file': item.is_file(),
                    'size': item.stat().st_size if item.is_file() else 0,
                    'modified': item.stat().st_mtime
                }
                contents.append(info)
    except Exception as e:
        print(f"Erro ao listar diretório {path}: {e}")
    return contents

def list_modules(path):
    """Lista módulos Python (.py)."""
    modules = []
    try:
        if path.exists():
            for item in path.glob("*.py"):
                if item.name != "__init__.py":
                    modules.append({
                        'name': item.stem,
                        'path': str(item),
                        'size': item.stat().st_size
                    })
    except Exception as e:
        print(f"Erro ao listar módulos em {path}: {e}")
    return modules
