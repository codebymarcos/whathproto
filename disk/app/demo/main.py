from core import Page, Txt, Btn
from kivy.app import App

class MainPage(Page):
    """Página principal do Mini App."""
    
    def __init__(self):
        """Inicializa com fundo verde."""
        # Fundo verde para diferenciar
        super().__init__(bg_color=(0.1, 0.7, 0.3, 1))
        
        self.add_widget(Txt(text="Olá do Disk!", size=40, bold=True))
        self.add_widget(Txt(text="Este app roda direto do disco.", size=20))
        
        # Botão para voltar
        btn = Btn(text="Voltar", bg=(1, 1, 1, 0.2))
        btn.bind(on_release=self._go_back)
        self.add_widget(btn)
        
    def _go_back(self, instance):
        """Volta para a home."""
        app = App.get_running_app()
        app.nav.go('interactive_home', direction='right')
