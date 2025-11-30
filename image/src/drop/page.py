"""Página Drop - Tela de notificações/widgets."""
from kivy.app import App
from core import Page, Txt

class Drop(Page):
    """Tela Drop acessível por swipe."""
    
    def __init__(self):
        """Inicializa com imagem de fundo."""
        super().__init__(bg_image="assets/plan.jpeg")
        
        # Título
        self.add_widget(Txt(text="Drop", size=30, bold=True, color=(1, 1, 1, 1)))
        
        # Conteúdo placeholder
        self.add_widget(Txt(text="Arraste para a direita\npara voltar", size=16, color=(1, 1, 1, 1)))
    
    def on_show(self):
        """Log ao exibir."""
        print("→ Drop")
    
    def on_touch_down(self, touch):
        """Captura início do toque para detectar swipe."""
        touch.ud['start_x'] = touch.x
        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        """Detecta swipe para a direita (voltar para home)."""
        if 'start_x' in touch.ud:
            dx = touch.x - touch.ud['start_x']
            
            # Swipe para direita (> 50px)
            if dx > 50:
                app = App.get_running_app()
                if hasattr(app, 'nav'):
                    app.nav.go('interactive_home', direction='right')
                    return True
        
        return super().on_touch_up(touch)
