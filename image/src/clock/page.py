"""Página de relógio."""
from kivy.clock import Clock as KivyClock
from kivy.app import App
from core import Page, Txt
from config import TIME_CONFIG


class Clock(Page):
    """Tela de relógio exibida após inatividade."""
    
    def __init__(self):
        """Inicializa com imagem de fundo."""
        super().__init__(bg_image="assets/plan.jpeg")
        
        # Label para hora
        self.time_label = Txt(text="00:00", size=80, color=(1, 1, 1, 1), bold=True)
        self.time_label.pos_hint = {'center_x': 0.5, 'center_y': 0.55}
        self.add_widget(self.time_label)
        
        # Label para data
        self.date_label = Txt(text="00/00/0000", size=20, color=(1, 1, 1, 1))
        self.date_label.pos_hint = {'center_x': 0.5, 'center_y': 0.4}
        self.add_widget(self.date_label)
        
        self.update_event = None
    
    def on_show(self):
        """Inicia atualização do relógio."""
        print("→ Relógio Ativado")
        self._update_time()
        # Atualiza usando intervalo do config
        self.update_event = KivyClock.schedule_interval(
            lambda dt: self._update_time(), 
            TIME_CONFIG['clock_update_interval']
        )
        
        # Registra toque para voltar
        self.bind(on_touch_down=self._on_touch)
    
    def on_hide(self):
        """Para atualização do relógio."""
        if self.update_event:
            self.update_event.cancel()
    
    def _update_time(self):
        """Atualiza hora e data."""
        app = App.get_running_app()
        if hasattr(app, 'manager'):
            self.time_label.text = app.manager.get_current_time()
            self.date_label.text = app.manager.get_current_date()
    
    def _on_touch(self, instance, touch):
        """Ao tocar, volta para a home."""
        app = App.get_running_app()
        if hasattr(app, 'manager'):
            app.manager.reset_inactivity_timer()
