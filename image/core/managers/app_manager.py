"""Gerenciador global do aplicativo."""
from kivy.clock import Clock
from kivy.app import App
from datetime import datetime


class AppManager:
    """Gerencia comportamentos globais do aplicativo."""
    
    def __init__(self, timeout_seconds=3):
        """Inicializa o gerenciador."""
        self.timeout_seconds = timeout_seconds
        self.timeout_event = None
        self.is_clock_visible = False
        
    def start_inactivity_timer(self):
        """Inicia o timer de inatividade."""
        self.reset_inactivity_timer()
        
    def reset_inactivity_timer(self):
        """Reseta o timer de inatividade."""
        # Cancela o timer anterior se existir
        if self.timeout_event:
            self.timeout_event.cancel()
        
        # Agenda novo timeout
        self.timeout_event = Clock.schedule_once(self._on_timeout, self.timeout_seconds)
        
        # Esconde o relógio se estiver visível
        if self.is_clock_visible:
            self._hide_clock()
    
    def _on_timeout(self, dt):
        """Chamado quando o timeout é atingido."""
        print("→ Timeout de inatividade atingido")
        self._show_clock()
    
    def _show_clock(self):
        """Exibe a tela de relógio."""
        self.is_clock_visible = True
        app = App.get_running_app()
        if hasattr(app, 'nav'):
            # Navega para a tela de relógio (vamos criar)
            app.nav.go('clock', direction='up')
    
    def _hide_clock(self):
        """Esconde a tela de relógio."""
        self.is_clock_visible = False
        app = App.get_running_app()
        if hasattr(app, 'nav'):
            # Volta para a home
            app.nav.go('interactive_home', direction='down')
    
    def get_current_time(self):
        """Retorna a hora atual formatada."""
        return datetime.now().strftime("%H:%M")
    
    def get_current_date(self):
        """Retorna a data atual formatada."""
        return datetime.now().strftime("%d/%m/%Y")
