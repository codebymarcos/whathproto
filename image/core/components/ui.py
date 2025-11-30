"""Componentes UI - Usando KivyMD."""
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivy.graphics import Color, RoundedRectangle


class Btn(MDFillRoundFlatButton):
    """Botão arredondado usando KivyMD."""
    
    def __init__(self, text='', bg=(0.2, 0.6, 1, 1), fg=(1, 1, 1, 1), radius=10, **kw):
        """Inicializa botão KivyMD."""
        super().__init__(text=text, **kw)
        self.md_bg_color = bg
        self.text_color = fg


class Txt(MDLabel):
    """Rótulo de texto usando KivyMD."""
    
    def __init__(self, text='', size=16, color=(0, 0, 0, 1), bold=False, font_name=None, **kw):
        """Inicializa MDLabel com suporte a fonte customizada."""
        super().__init__(text=text, **kw)
        
        if font_name:
            self.font_name = font_name
        else:
            self.font_style = "Body1"
            
        self.theme_text_color = "Custom"
        self.text_color = color
        self.font_size = size
        self.bold = bold
        self.halign = "center"
        self.size_hint_y = None
        self.height = size * 2


class Icon(MDIconButton):
    """Botão de ícone usando KivyMD (MDIconButton)."""
    
    def __init__(self, icon='cog', size=60, **kw):
        """Inicializa botão de ícone."""
        super().__init__(icon=icon, **kw)
        self.icon_size = str(size // 2) + "sp"
        self.size_hint = (None, None)
        self.size = (size, size)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
