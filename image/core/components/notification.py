"""Componente de notificação."""
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from config import TIME_CONFIG


class Notification(BoxLayout):
    """Notificação flutuante com ícone e mensagem."""
    
    def __init__(self, message="", icon="information", duration=None, **kwargs):
        """
        Inicializa a notificação.
        
        Args:
            message: Texto da notificação
            icon: Nome do ícone Material Design
            duration: Duração em segundos (None usa padrão do config)
        """
        super().__init__(orientation='horizontal', **kwargs)
        
        self.message = message
        self.icon_name = icon
        # Usa duração passada ou padrão do config
        self.duration = duration if duration is not None else TIME_CONFIG['notification_duration']
        
        # Configurações de tamanho e posição
        self.size_hint = (0.9, None)
        self.height = 50
        self.pos_hint = {'center_x': 0.5, 'top': 1}
        self.padding = [10, 5]
        self.spacing = 10
        
        # Opacidade inicial (invisível)
        self.opacity = 0
        
        # Desenha o fundo semi-transparente
        with self.canvas.before:
            Color(0, 0, 0, 0.7)  # Preto com 70% de opacidade
            self.bg_rect = RoundedRectangle(
                size=self.size,
                pos=self.pos,
                radius=[15]
            )
        
        self.bind(size=self._update_bg, pos=self._update_bg)
        
        # Adiciona ícone
        self.icon_widget = MDIconButton(
            icon=self.icon_name,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            icon_size="24sp"
        )
        self.icon_widget.size_hint = (None, 1)
        self.icon_widget.width = 40
        self.add_widget(self.icon_widget)
        
        # Adiciona mensagem
        self.label = MDLabel(
            text=self.message,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size="14sp",
            halign="left",
            valign="center"
        )
        self.add_widget(self.label)
    
    def _update_bg(self, *args):
        """Atualiza o fundo."""
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
    
    def show(self):
        """Exibe a notificação com animação."""
        # Animação de entrada (slide down + fade in)
        anim_in = Animation(
            opacity=1,
            pos_hint={'center_x': 0.5, 'top': 0.95},
            duration=0.3,
            t='out_quad'
        )
        anim_in.start(self)
        
        # Agenda a saída
        Clock.schedule_once(self._hide, self.duration)
    
    def _hide(self, dt):
        """Esconde a notificação com animação."""
        # Animação de saída (slide up + fade out)
        anim_out = Animation(
            opacity=0,
            pos_hint={'center_x': 0.5, 'top': 1.1},
            duration=0.3,
            t='in_quad'
        )
        anim_out.bind(on_complete=self._remove)
        anim_out.start(self)
    
    def _remove(self, *args):
        """Remove a notificação da tela."""
        if self.parent:
            self.parent.remove_widget(self)
