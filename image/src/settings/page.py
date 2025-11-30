"""Página de configurações."""
from core import Page

class Settings(Page):
    """Página de configurações."""
    
    def __init__(self):
        """Inicializa com fundo cinza claro."""
        super().__init__(bg_color=(0.95, 0.95, 0.95, 1))
    
    def on_show(self):
        """Log ao exibir página."""
        print("→ Entrou em Configurações")
