"""Lógica interna do app de armazenamento."""
from kivy.app import App

def get_storage_info():
    """
    Obtém informações formatadas sobre o armazenamento.
    
    Returns:
        dict: Informações do disco ou None se erro
    """
    app = App.get_running_app()
    if hasattr(app, 'fs_driver'):
        return app.fs_driver.get_disk_info()
    return None

def list_contents(limit=10):
    """
    Lista o conteúdo do disco.
    
    Args:
        limit: Número máximo de itens a retornar
        
    Returns:
        list: Lista de itens ou None se erro
    """
    app = App.get_running_app()
    if hasattr(app, 'fs_driver'):
        contents = app.fs_driver.list_disk_contents()
        if contents:
            return contents[:limit]
    return None

def format_size(size_bytes):
    """Formata bytes para MB."""
    return f"{size_bytes / (1024 * 1024):.2f} MB"

def format_item_text(item):
    """Formata texto de exibição de um item."""
    name = item['name']
    size = item['size']
    is_dir = item['is_dir']
    
    icon = "📁" if is_dir else "📄"
    size_text = "DIR" if is_dir else f"{size} bytes"
    
    return f"{icon} {name}\n{size_text}"
