"""Configuração global de cache para todo o projeto WiserWhath."""
import os
import sys
from pathlib import Path

def setup_python_cache():
    """
    Configura o diretório de cache do Python para todo o projeto.
    
    Esta função deve ser chamada no início de QUALQUER script Python
    do projeto para garantir que os arquivos .pyc sejam salvos em
    disk/storage/cache.
    
    Returns:
        Path: Caminho do diretório de cache configurado
    """
    # Detecta a raiz do projeto (onde está este arquivo)
    project_root = Path(__file__).parent.resolve()
    
    # Define o diretório de cache
    cache_dir = project_root / "disk" / "storage" / "cache"
    
    # Cria o diretório se não existir
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Configura a variável de ambiente
    os.environ['PYTHONPYCACHEPREFIX'] = str(cache_dir)
    
    # Adiciona wiserwhath_system ao path se ainda não estiver
    wiserwhath_path = project_root / "wiserwhath_system"
    if str(wiserwhath_path) not in sys.path:
        sys.path.insert(0, str(wiserwhath_path))
    
    return cache_dir

# Executa automaticamente ao importar
CACHE_DIR = setup_python_cache()

if __name__ == '__main__':
    print(f"✓ Cache configurado em: {CACHE_DIR}")
    print(f"✓ PYTHONPYCACHEPREFIX = {os.environ.get('PYTHONPYCACHEPREFIX')}")
