"""Página sobre o aplicativo."""
from core import Page

class About(Page):
    """Página sobre o aplicativo."""
    
    def __init__(self):
        """Inicializa com fundo azul claro."""
        super().__init__(bg_color=(0.9, 0.95, 1, 1))
    
    def on_show(self):
        """Log ao exibir página."""
        print("→ Entrou em Sobre")
