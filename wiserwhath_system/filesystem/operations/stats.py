"""Operações de estatísticas e informações."""
from pathlib import Path

def get_disk_info(path):
    """Retorna informações sobre o uso do disco."""
    try:
        if not path.exists():
            return {'path': str(path), 'exists': False, 'total_size': 0, 'file_count': 0}
            
        total_size = sum(
            f.stat().st_size 
            for f in path.rglob('*') 
            if f.is_file()
        )
        
        file_count = sum(1 for _ in path.rglob('*') if _.is_file())
        
        return {
            'path': str(path),
            'total_size': total_size,
            'file_count': file_count,
            'exists': True
        }
    except Exception as e:
        print(f"Erro ao obter info do disco: {e}")
        return {}
