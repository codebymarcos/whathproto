"""Página Kickstart."""
from kivy.clock import Clock
from kivy.app import App
from core import Page
from config import TIME_CONFIG
from .animations import TypewriterText


class Kickstart(Page):
    """Página inicial com animação de texto e imagem de fundo."""
    
    def __init__(self):
        """Inicializa com imagem de fundo."""
        super().__init__(bg_image="assets/plan.jpeg")
        
        # Adiciona a animação de texto
        self.animation = TypewriterText(text="hello")
        self.add_widget(self.animation)
    
    def on_show(self):
        """Inicia animação ao exibir."""
        print("→ Kickstart Iniciado")
        Clock.schedule_once(self._start_animation, 0.1)
        
    def _start_animation(self, dt):
        """Inicia a animação de escrita."""
        self.animation.start_animation(callback=self._schedule_transition)
    
    def _schedule_transition(self):
        """Agenda transição após animação completa."""
        Clock.schedule_once(self._go_next, TIME_CONFIG['kickstart_exit_delay'])
        
    def _go_next(self, dt):
        """Navega para a próxima tela."""
        app = App.get_running_app()
        if hasattr(app, 'nav'):
            app.nav.go('interactive_home')
