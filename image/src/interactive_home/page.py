"""Página Interactive Home - Tela Limpa."""
from kivy.app import App
from kivy.clock import Clock
from datetime import datetime
from core import Page, Txt
from kivy.uix.boxlayout import BoxLayout

class InteractiveHome(Page):
    """Home limpa com relógio."""
    
    def __init__(self):
        """Inicializa com imagem de fundo."""
        super().__init__(bg_image="assets/plan.jpeg")
        
        # Container centralizado para o relógio
        clock_container = BoxLayout(orientation='vertical', spacing=0, size_hint=(1, 1))
        
        # Espaçador superior para centralizar
        clock_container.add_widget(BoxLayout(size_hint_y=0.4))
        
        # Relógio Grande
        self.time_label = Txt(
            text="--:--", 
            size=60, 
            bold=True, 
            color=(1, 1, 1, 1),
            font_name="Pacifico"
        )
        clock_container.add_widget(self.time_label)
        
        # Data
        self.date_label = Txt(
            text="--/--", 
            size=18, 
            color=(1, 1, 1, 0.9)
        )
        clock_container.add_widget(self.date_label)
        
        # Espaçador inferior
        clock_container.add_widget(BoxLayout(size_hint_y=0.6))
        
        self.add_widget(clock_container)
        
        # Atualiza relógio
        Clock.schedule_interval(self._update_clock, 1.0)
        self._update_clock(0)
    
    def _update_clock(self, dt):
        """Atualiza hora e data."""
        now = datetime.now()
        self.time_label.text = now.strftime("%H:%M")
        self.date_label.text = now.strftime("%a, %d %b")
    
    def on_show(self):
        """Log ao exibir."""
        print("→ Interactive Home")
