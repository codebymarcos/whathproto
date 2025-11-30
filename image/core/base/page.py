"""Módulo de Página Base - Simples e robusto."""
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.app import App


class Page(BoxLayout):
    """Classe base para páginas com gerenciamento automático de fundo e barra de status."""
    
    def __init__(self, bg_color=(1, 1, 1, 1), bg_image=None, reset_timer_on_touch=True, **kwargs):
        """Inicializa a página com cor de fundo ou imagem (padrão: branco)."""
        super().__init__(orientation='vertical', **kwargs)
        self.bg_color = bg_color
        self.bg_image_path = bg_image
        self.reset_timer_on_touch = reset_timer_on_touch
        
        self._draw_background()
        self._draw_status_bar_indicator()
        
        # Registra evento de toque global se habilitado
        if self.reset_timer_on_touch:
            self.bind(on_touch_down=self._handle_touch)
            
    def _draw_background(self):
        """Desenha o fundo (imagem ou cor sólida)."""
        if self.bg_image_path:
            # Usa imagem de fundo
            with self.canvas.before:
                self.bg_rect = Rectangle(source=self.bg_image_path, size=self.size, pos=self.pos)
            self.bind(size=self._update_bg, pos=self._update_bg)
        else:
            # Usa cor sólida
            with self.canvas.before:
                Color(*self.bg_color)
                self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_bg, pos=self._update_bg)
            
    def _draw_status_bar_indicator(self):
        """Desenha o indicador da barra de status no topo."""
        with self.canvas.after:
            # Barra semi-transparente no topo
            Color(1, 1, 1, 0.3)
            self.status_bar = RoundedRectangle(size=(40, 4), pos=(0, 0), radius=[2])
            
        self.bind(size=self._update_status_bar, pos=self._update_status_bar)
        
    def _update_bg(self, *args):
        """Atualiza geometria do fundo."""
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
        
    def _update_status_bar(self, *args):
        """Atualiza posição da barra de status (centralizada no topo)."""
        self.status_bar.size = (40, 4)
        self.status_bar.pos = (self.center_x - 20, self.top - 10)
    
    def _handle_touch(self, instance, touch):
        """Reseta o timer de inatividade ao tocar."""
        app = App.get_running_app()
        if hasattr(app, 'manager'):
            app.manager.reset_inactivity_timer()
        # Propaga o evento para widgets filhos
        return False
        
    def on_touch_down(self, touch):
        """Captura início do toque para detectar swipe da barra de status."""
        # Se o toque for no topo da tela (últimos 10% ou 30px)
        if touch.y > self.height * 0.9:
            touch.ud['status_bar_drag'] = True
            touch.ud['start_y'] = touch.y
            
        return super().on_touch_down(touch)
        
    def on_touch_up(self, touch):
        """Detecta swipe down da barra de status."""
        if touch.ud.get('status_bar_drag'):
            dy = touch.ud['start_y'] - touch.y
            
            # Swipe para baixo (> 30px)
            if dy > 30:
                self._open_processes_app()
                return True
                
        return super().on_touch_up(touch)
        
    def _open_processes_app(self):
        """Abre o app de processos."""
        print("→ Abrindo Processos (Swipe Down)")
        app = App.get_running_app()
        if hasattr(app, 'app_loader'):
            # Tenta lançar o app de processos
            # Primeiro verifica se já está carregado, senão carrega
            success = app.app_loader.launch_app('processes_app')
            if not success:
                print("Erro ao abrir app de processos")
    
    def on_show(self):
        """Hook chamado quando a página é exibida."""
        pass
    
    def on_hide(self):
        """Hook chamado quando a página é ocultada."""
        pass
