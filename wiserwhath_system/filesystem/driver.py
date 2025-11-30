"""Driver de sistema de arquivos (Agregador)."""
from pathlib import Path
from .operations import io, management, stats

class FileSystemDriver:
    """Driver principal que agrega funções de sistema de arquivos."""
    
    def __init__(self, disk_path=None, system_path=None):
        """Inicializa caminhos."""
        base_path = Path(__file__).parent.parent.parent
        
        self.disk_path = Path(disk_path) if disk_path else base_path / "disk"
        self.system_path = Path(system_path) if system_path else base_path / "wiserwhath_system"
        
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Garante diretórios."""
        self.disk_path.mkdir(parents=True, exist_ok=True)
        self.system_path.mkdir(parents=True, exist_ok=True)
    
    def list_disk_contents(self):
        """Lista conteúdo do disco."""
        return management.list_contents(self.disk_path)
    
    def list_system_modules(self):
        """Lista módulos do sistema."""
        return management.list_modules(self.system_path)
    
    def read_file(self, filename, from_disk=True):
        """Lê arquivo."""
        base = self.disk_path if from_disk else self.system_path
        return io.read(base, filename)
    
    def write_file(self, filename, content, to_disk=True):
        """Escreve arquivo."""
        base = self.disk_path if to_disk else self.system_path
        return io.write(base, filename, content)
    
    def delete_file(self, filename, from_disk=True):
        """Deleta arquivo."""
        base = self.disk_path if from_disk else self.system_path
        return management.delete(base, filename)
    
    def get_disk_info(self):
        """Obtém info do disco."""
        return stats.get_disk_info(self.disk_path)
