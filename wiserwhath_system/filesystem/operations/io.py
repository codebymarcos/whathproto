"""Operações de Entrada e Saída (I/O)."""
from pathlib import Path

def read(base_path, filename):
    """Lê um arquivo."""
    file_path = base_path / filename
    try:
        if file_path.exists():
            return file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Erro ao ler arquivo {filename}: {e}")
    return None

def write(base_path, filename, content):
    """Escreve em um arquivo."""
    file_path = base_path / filename
    try:
        # Garante que o diretório pai existe
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
        return True
    except Exception as e:
        print(f"Erro ao escrever arquivo {filename}: {e}")
        return False
