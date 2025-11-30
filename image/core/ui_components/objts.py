"""Componentes UI reutilizáveis - Estilo iOS."""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle
from kivymd.uix.button import MDIconButton
from kivy.uix.slider import Slider
from kivy.animation import Animation


class AppIcon(FloatLayout):
    """Ícone de app estilo iOS - Pequeno e redondo."""
    
    def __init__(self, icon, name, callback=None, bg_color=(0.2, 0.4, 0.8, 1), **kwargs):
        """Cria um ícone de app."""
        # Tamanho reduzido para caber 4 por linha
        super().__init__(size_hint=(None, None), size=(45, 45), **kwargs)
        
        self.callback = callback
        self.bg_color = bg_color
        
        # Container do ícone
        # Ícone ocupa quase todo o espaço
        icon_container = FloatLayout(
            size_hint=(None, None),
            size=(45, 45),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Fundo Redondo (Círculo Perfeito)
        with icon_container.canvas.before:
            Color(*bg_color)
            self.bg_rect = RoundedRectangle(
                pos=icon_container.pos,
                size=icon_container.size,
                radius=[22.5]  # Metade do tamanho para ser círculo
            )
        
        icon_container.bind(
            pos=lambda *args: setattr(self.bg_rect, 'pos', icon_container.pos),
            size=lambda *args: setattr(self.bg_rect, 'size', icon_container.size)
        )
        
        # Ícone
        icon_btn = MDIconButton(
            icon=icon,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            icon_size="24sp"  # Ícone menor
        )
        icon_btn.bind(on_release=self._on_click)
        
        icon_container.add_widget(icon_btn)
        self.add_widget(icon_container)
        self.icon_container = icon_container
    
    def _on_click(self, instance):
        """Animação de clique."""
        # Animação sutil de redução
        anim = Animation(size=(40, 40), duration=0.1) + Animation(size=(45, 45), duration=0.1)
        anim.start(self.icon_container)
        if self.callback:
            self.callback()


class QuickToggle(FloatLayout):
    """Toggle rápido estilo iOS (Apenas ícone)."""
    
    def __init__(self, icon, title="", subtitle="", active=False, callback=None, **kwargs):
        """Cria um toggle rápido."""
        super().__init__(size_hint=(None, None), size=(60, 60), **kwargs)
        
        self.callback = callback
        self.active = active
        
        # Fundo arredondado
        with self.canvas.before:
            self.bg_color = Color(0.2, 0.4, 0.8, 1) if active else Color(0.3, 0.3, 0.3, 0.5)
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[15]
            )
        
        self.bind(
            pos=lambda *args: setattr(self.bg_rect, 'pos', self.pos),
            size=lambda *args: setattr(self.bg_rect, 'size', self.size)
        )
        
        # Ícone
        self.icon_btn = MDIconButton(
            icon=icon,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            icon_size="30sp"
        )
        self.icon_btn.bind(on_release=self._toggle)
        self.add_widget(self.icon_btn)
    
    def _toggle(self, instance):
        """Alterna o estado."""
        self.active = not self.active
        if self.active:
            self.bg_color.rgba = (0.2, 0.4, 0.8, 1)
        else:
            self.bg_color.rgba = (0.3, 0.3, 0.3, 0.5)
        if self.callback:
            self.callback(self.active)
    
    def set_active(self, active):
        """Define o estado externamente."""
        self.active = active
        if active:
            self.bg_color.rgba = (0.2, 0.4, 0.8, 1)
        else:
            self.bg_color.rgba = (0.3, 0.3, 0.3, 0.5)


class VolumeSlider(FloatLayout):
    """Slider de volume vertical minimalista estilo iOS."""
    
    def __init__(self, **kwargs):
        """Cria um slider de volume."""
        super().__init__(size_hint=(None, None), size=(60, 135), **kwargs)
        
        # Fundo (track)
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
            
            # Barra de progresso (fill)
            self.fill_color = Color(1, 1, 1, 1)
            self.fill_rect = RoundedRectangle(pos=self.pos, size=(self.width, 0), radius=[15])
            
        self.bind(pos=self._update_rects, size=self._update_rects)
        
        # Slider invisível para controle
        self.slider = Slider(
            min=0, max=100, value=50,
            orientation='vertical',
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            opacity=0
        )
        self.slider.bind(value=self._on_value_change)
        
        # Ícone de volume
        self.icon = MDIconButton(
            icon="volume-high",
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            pos_hint={'center_x': 0.5, 'y': 0.05},
            icon_size="24sp"
        )
        
        self.add_widget(self.slider)
        self.add_widget(self.icon)
        
        # Inicializa visual
        self._on_value_change(None, 50)
        
    def _update_rects(self, *args):
        """Atualiza geometria."""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self._update_fill()
        
    def _update_fill(self):
        """Atualiza a barra de preenchimento."""
        fill_height = (self.slider.value / 100) * self.height
        self.fill_rect.pos = self.pos
        self.fill_rect.size = (self.width, fill_height)
        
        # Muda cor do ícone se preenchido
        if self.slider.value > 10:
            self.icon.text_color = (0.2, 0.2, 0.2, 1)
        else:
            self.icon.text_color = (0.5, 0.5, 0.5, 1)

    def _on_value_change(self, instance, value):
        """Callback de mudança de valor."""
        self._update_fill()
        print(f"Volume: {int(value)}%")


class AppGrid(BoxLayout):
    """Grid de apps estilo iOS (4 colunas)."""
    def __init__(self, **kwargs):
        padding = kwargs.pop('padding', 10) # Padding menor
        super().__init__(orientation='vertical', spacing=10, padding=padding, **kwargs)
        self.rows = []
        self.current_row = None
    
    def add_app(self, icon, name, callback, bg_color=(0.2, 0.4, 0.8, 1)):
        # 4 apps por linha
        if self.current_row is None or len(self.current_row.children) >= 4:
            self.current_row = BoxLayout(size_hint_y=None, height=45, spacing=10)
            self.rows.append(self.current_row)
            self.add_widget(self.current_row)
        
        app_icon = AppIcon(icon, name, callback, bg_color)
        self.current_row.add_widget(app_icon)
        
        # Preenche espaços vazios
        while len(self.current_row.children) < 4:
            spacer = BoxLayout(size_hint=(None, None), size=(45, 45))
            self.current_row.add_widget(spacer)
