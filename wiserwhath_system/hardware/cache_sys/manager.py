"""Gerenciador de Cache do Sistema (Hardware Level)."""
import os
import shutil
from pathlib import Path

class CacheManager:
    """Gerencia e centraliza arquivos de cache (__pycache__)."""
    
    def __init__(self, project_root, storage_path):
        """
        Inicializa o gerenciador de cache.
        
        Args:
            project_root (str/Path): Raiz do projeto para escanear
            storage_path (str/Path): Local para salvar os caches (disk/storage/cache)
        """
        self.project_root = Path(project_root).resolve()
        self.storage_path = Path(storage_path).resolve()
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Pastas a ignorar
        self.ignore_dirs = {'.venv', 'venv', '.git', '.idea', '.vscode', 'node_modules', 'disk'}
        
    def relocate_caches(self):
        """
        Escaneia, move e centraliza todos os __pycache__.
        
        Returns:
            dict: Estatísticas da operação
        """
        stats = {'found': 0, 'moved': 0, 'errors': 0}
        
        # Percorre todo o projeto
        for root, dirs, files in os.walk(self.project_root):
            # Modifica dirs in-place para pular pastas ignoradas
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            # Ignora se estiver dentro do storage path (evita loop)
            if str(self.storage_path) in str(Path(root).resolve()):
                continue

            if '__pycache__' in dirs:
                source_cache = Path(root) / '__pycache__'
                
                try:
                    # Calcula caminho relativo limpo
                    # Ex: C:/.../image/src/kickstart -> src/kickstart
                    rel_path = Path(root).relative_to(self.project_root)
                    
                    # Destino: disk/storage/cache/src/kickstart
                    # Não criamos uma subpasta __pycache__ no destino, apenas salvamos os .pyc lá
                    dest_dir = self.storage_path / rel_path
                    
                    stats['found'] += 1
                    
                    # Garante que o destino existe
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Move arquivos .pyc
                    for pyc_file in source_cache.glob('*.pyc'):
                        try:
                            # Copia o arquivo
                            shutil.copy2(pyc_file, dest_dir / pyc_file.name)
                            stats['moved'] += 1
                        except Exception as e:
                            print(f"Erro ao copiar {pyc_file.name}: {e}")
                            stats['errors'] += 1
                            
                except Exception as e:
                    print(f"Erro ao processar pasta {source_cache}: {e}")
                    stats['errors'] += 1
                    
        return stats

    def clear_central_cache(self):
        """Limpa o cache centralizado."""
        try:
            # Remove todo o conteúdo de storage/cache
            for item in self.storage_path.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            return True
        except Exception as e:
            print(f"Erro ao limpar cache central: {e}")
            return False
