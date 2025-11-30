"""Sistema de armazenamento local de dados (cache/persistência)."""
import json
from pathlib import Path

class LocalStorage:
    """Armazenamento local de dados em JSON."""
    
    def __init__(self, storage_dir):
        """
        Inicializa o armazenamento local.
        
        Args:
            storage_dir: Diretório para armazenar dados
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def set(self, key, value):
        """
        Armazena um valor.
        
        Args:
            key: Chave (nome do arquivo)
            value: Valor (será serializado para JSON)
            
        Returns:
            bool: True se sucesso
        """
        try:
            file_path = self.storage_dir / f"{key}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(value, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar {key}: {e}")
            return False
    
    def get(self, key, default=None):
        """
        Recupera um valor.
        
        Args:
            key: Chave
            default: Valor padrão se não encontrado
            
        Returns:
            Valor armazenado ou default
        """
        try:
            file_path = self.storage_dir / f"{key}.json"
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return default
        except Exception as e:
            print(f"Erro ao ler {key}: {e}")
            return default
    
    def delete(self, key):
        """
        Remove um valor.
        
        Args:
            key: Chave
            
        Returns:
            bool: True se removido
        """
        try:
            file_path = self.storage_dir / f"{key}.json"
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"Erro ao deletar {key}: {e}")
            return False
    
    def exists(self, key):
        """Verifica se uma chave existe."""
        file_path = self.storage_dir / f"{key}.json"
        return file_path.exists()
    
    def list_keys(self):
        """Lista todas as chaves armazenadas."""
        try:
            return [f.stem for f in self.storage_dir.glob("*.json")]
        except Exception as e:
            print(f"Erro ao listar chaves: {e}")
            return []
    
    def clear(self):
        """Remove todos os dados armazenados."""
        try:
            for file in self.storage_dir.glob("*.json"):
                file.unlink()
            return True
        except Exception as e:
            print(f"Erro ao limpar storage: {e}")
            return False
