"""Página de relógio analógico minimalista."""
from kivy.clock import Clock as KivyClock
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Ellipse, Rotate, PushMatrix, PopMatrix
from core import Page, Txt
from config import TIME_CONFIG
import math
from datetime import datetime

class AnalogClockWidget(Widget):
    """Widget de relógio analógico minimalista."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._update_clock, size=self._update_clock)
        
    def update(self, dt=None):
        """Atualiza os ponteiros."""
        self._update_clock()
        
    def _update_clock(self, *args):
        """Desenha o relógio."""
        self.canvas.clear()
        
        cx, cy = self.center_x, self.center_y
        radius = min(self.width, self.height) / 2 * 0.8
        
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second
        
        with self.canvas:
            # Marcadores de horas (Minimalista: apenas traços nos 12, 3, 6, 9)
            Color(1, 1, 1, 0.8)
            for i in range(0, 12, 3): # 0, 3, 6, 9
                angle = math.radians(i * 30)
                x1 = cx + math.sin(angle) * (radius - 10)
                y1 = cy + math.cos(angle) * (radius - 10)
                x2 = cx + math.sin(angle) * radius
                y2 = cy + math.cos(angle) * radius
                Line(points=[x1, y1, x2, y2], width=2)
            
            # Marcadores menores para as outras horas
            Color(1, 1, 1, 0.4)
            for i in range(12):
                if i % 3 != 0:
                    angle = math.radians(i * 30)
                    x1 = cx + math.sin(angle) * (radius - 5)
                    y1 = cy + math.cos(angle) * (radius - 5)
                    x2 = cx + math.sin(angle) * radius
                    y2 = cy + math.cos(angle) * radius
                    Line(points=[x1, y1, x2, y2], width=1)

            # Ponteiro das Horas
            PushMatrix()
            Rotate(angle=-(hour % 12 + minute / 60) * 30, origin=(cx, cy))
            Color(1, 1, 1, 1)
            # Desenha linha grossa do centro até 50% do raio
            Line(points=[cx, cy, cx, cy + radius * 0.5], width=4, cap='round')
            PopMatrix()
            
            # Ponteiro dos Minutos
            PushMatrix()
            Rotate(angle=-(minute + second / 60) * 6, origin=(cx, cy))
            Color(1, 1, 1, 0.8)
            # Desenha linha média do centro até 70% do raio
            Line(points=[cx, cy, cx, cy + radius * 0.75], width=3, cap='round')
            PopMatrix()
            
            # Ponteiro dos Segundos (Destaque)
            PushMatrix()
            Rotate(angle=-second * 6, origin=(cx, cy))
            Color(1, 0.3, 0.3, 1) # Vermelho suave
            # Linha fina do centro até 85% do raio
            Line(points=[cx, cy, cx, cy + radius * 0.85], width=1.5)
            # Pequena extensão para trás
            Line(points=[cx, cy, cx, cy - radius * 0.15], width=1.5)
            PopMatrix()
            
            # Centro (Pino)
            Color(1, 1, 1, 1)
            Ellipse(pos=(cx - 4, cy - 4), size=(8, 8))
            Color(0.2, 0.2, 0.2, 1)
            Ellipse(pos=(cx - 2, cy - 2), size=(4, 4))


class Clock(Page):
    """Tela de relógio exibida após inatividade."""
    
    def __init__(self):
        """Inicializa com fundo preto."""
        super().__init__(bg_color=(0, 0, 0, 1))  # Fundo preto sólido
        
        # Widget do Relógio Analógico
        # Centralizado perfeitamente
        self.analog_clock = AnalogClockWidget(size_hint=(None, None), size=(220, 220))
        self.analog_clock.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.add_widget(self.analog_clock)
        
        # Data Digital (Opcional - removida para foco total no relógio ou movida para bem discreta)
        # Vou remover para garantir centralização visual perfeita do relógio
        # Se o usuário quiser a data, posso adicionar depois em um local que não interfira
        
        self.update_event = None
    
    def on_show(self):
        """Inicia atualização do relógio."""
        print("→ Relógio Ativado")
        self._update_time()
        # Atualiza a cada segundo
        self.update_event = KivyClock.schedule_interval(
            lambda dt: self._update_time(), 
            1.0
        )
        
        # Registra toque para voltar
        self.bind(on_touch_down=self._on_touch)
    
    def on_hide(self):
        """Para atualização do relógio."""
        if self.update_event:
            self.update_event.cancel()
    
    def _update_time(self):
        """Atualiza hora."""
        # Atualiza widget analógico
        self.analog_clock.update()
    
    def _on_touch(self, instance, touch):
        """Ao tocar, volta para a home."""
        app = App.get_running_app()
        if hasattr(app, 'manager'):
            app.manager.reset_inactivity_timer()
