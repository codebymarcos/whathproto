"""Animações específicas do Kickstart."""
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from core import Txt
from config import TIME_CONFIG


class TypewriterText(FloatLayout):
    """Animação de texto sendo escrito letra por letra."""
    
    def __init__(self, text="hello", font_size=50, font_name="Pacifico", 
                 color=(1, 1, 1, 1), shadow=False, **kwargs):
        """
        Inicializa a animação de texto.
        
        Args:
            text: Texto a ser animado
            font_size: Tamanho da fonte
            font_name: Nome da fonte
            color: Cor do texto (R, G, B, A)
            shadow: Se True, adiciona sombra ao texto (padrão: False)
        """
        super().__init__(**kwargs)
        
        self.target_text = text
        self.char_index = 0
        self.animation_event = None  # Referência ao evento do Clock
        self.callback = None
        self.has_shadow = shadow
        
        # Adiciona sombra se habilitado
        if self.has_shadow:
            with self.canvas.before:
                Color(0, 0, 0, 0.5)  # Preto semi-transparente
                self.shadow = Rectangle(pos=(0, 0), size=(0, 0))
        
        # Cria o label com parâmetros configuráveis
        self.label = Txt(
            text="", 
            size=font_size, 
            color=color, 
            font_name=font_name
        )
        
        # Centraliza o label no FloatLayout
        self.label.size_hint = (1, None)
        self.label.height = 100
        self.label.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        
        self.add_widget(self.label)
        
        # Vincula atualização da sombra
        if self.has_shadow:
            self.label.bind(pos=self.update_shadow, size=self.update_shadow)
    
    def update_shadow(self, *args):
        """Atualiza posição da sombra."""
        if self.has_shadow:
            self.shadow.pos = (self.label.x + 2, self.label.y - 2)
            self.shadow.size = self.label.size
        
    def start_animation(self, callback=None, speed=None):
        """
        Inicia a animação de escrita.
        
        Args:
            callback: Função a ser chamada ao completar
            speed: Velocidade customizada (segundos por letra)
        """
        # Cancela animação anterior se existir
        if self.animation_event:
            self.animation_event.cancel()
        
        self.char_index = 0
        self.label.text = ""
        self.callback = callback
        
        # Usa velocidade customizada ou padrão do config
        typing_speed = speed if speed is not None else TIME_CONFIG['kickstart_typing_speed']
        
        # Inicia o efeito de máquina de escrever
        self.animation_event = Clock.schedule_interval(self._type_next_char, typing_speed)
    
    def stop_animation(self):
        """Para a animação imediatamente."""
        if self.animation_event:
            self.animation_event.cancel()
            self.animation_event = None
    
    def skip_animation(self):
        """Pula direto para o texto completo."""
        self.stop_animation()
        self.label.text = self.target_text
        if self.callback:
            self.callback()
    
    def set_text(self, new_text):
        """
        Atualiza o texto sem iniciar animação.
        
        Args:
            new_text: Novo texto a ser exibido
        """
        self.target_text = new_text
    
    def _type_next_char(self, dt):
        """Adiciona a próxima letra."""
        try:
            if self.char_index < len(self.target_text):
                self.label.text += self.target_text[self.char_index]
                self.char_index += 1
            else:
                # Texto completo, chama callback se existir
                if self.callback:
                    # Pequeno delay antes do callback para garantir leitura
                    Clock.schedule_once(lambda dt: self.callback(), 0.1)
                return False  # Para o agendamento
        except Exception as e:
            print(f"Erro na animação de texto: {e}")
            return False
    
    def on_parent(self, widget, parent):
        """Limpa recursos quando o widget é removido."""
        if parent is None:
            self.stop_animation()
