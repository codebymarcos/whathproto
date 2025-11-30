"""Módulo de Página Base - Simples e robusto."""
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.app import App


class Page(BoxLayout):
    """Classe base para páginas."""
    
    def __init__(self, bg_color=(1, 1, 1, 1), bg_image=None, reset_timer_on_touch=True, **kwargs):
        """Inicializa a página."""
        super().__init__(orientation='vertical', **kwargs)
        self.bg_color = bg_color
        self.bg_image_path = bg_image
        self.reset_timer_on_touch = reset_timer_on_touch
        
        self._draw_background()
        
        # Registra evento de toque
        if self.reset_timer_on_touch:
            self.bind(on_touch_down=self._handle_touch)
            
    def _draw_background(self):
        """Desenha o fundo."""
        if self.bg_image_path:
            with self.canvas.before:
                self.bg_rect = Rectangle(source=self.bg_image_path, size=self.size, pos=self.pos)
            self.bind(size=self._update_bg, pos=self._update_bg)
        else:
            with self.canvas.before:
                Color(*self.bg_color)
                self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_bg, pos=self._update_bg)
            
    def _update_bg(self, *args):
        """Atualiza fundo."""
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
    
    def _handle_touch(self, instance, touch):
        """Reseta timer."""
        app = App.get_running_app()
        if hasattr(app, 'manager'):
            app.manager.reset_inactivity_timer()
        return False
        
    def on_touch_down(self, touch):
        """Detecta início do toque."""
        touch.ud['start_x'] = touch.x
        touch.ud['start_y'] = touch.y
        
        # Detecta toque no topo para processos
        if touch.y > self.height - 30:
            touch.ud['status_bar_drag'] = True
            
        return super().on_touch_down(touch)
        
    def on_touch_up(self, touch):
        """Detecta swipes."""
        if 'start_x' in touch.ud and 'start_y' in touch.ud:
            dy = touch.ud['start_y'] - touch.y
            dx = touch.x - touch.ud['start_x']
            
            # Swipe Down (Processos)
            if touch.ud.get('status_bar_drag') and dy > 30:
                self._open_processes_app()
                return True
            
            # Swipe Right (Quick Settings)
            if dx > 50 and abs(dy) < 50:
                self._open_quick_settings()
                return True
                
            # Swipe Left (Drop)
            if dx < -50 and abs(dy) < 50:
                self._open_drop()
                return True
                
        return super().on_touch_up(touch)
        
    def _open_processes_app(self):
        """Abre app de processos."""
        print("→ Abrindo Processos (Swipe Down)")
        app = App.get_running_app()
        if hasattr(app, 'app_loader'):
            app.app_loader.launch_app('processes_app')
    
    def _open_quick_settings(self):
        """Abre quick settings."""
        print("→ Abrindo Quick Settings (Swipe Right)")
        app = App.get_running_app()
        if hasattr(app, 'nav'):
            # Usa 'current' para verificar a tela atual
            if app.nav.current != 'quick_settings':
                app.nav.go('quick_settings', direction='left')
                
    def _open_drop(self):
        """Abre página Drop."""
        print("→ Abrindo Drop (Swipe Left)")
        app = App.get_running_app()
        if hasattr(app, 'nav'):
            # Usa 'current' para verificar a tela atual
            if app.nav.current == 'interactive_home':
                app.nav.go('drop', direction='right')
    
    def on_show(self):
        """Hook chamado quando a página é exibida."""
        pass
    
    def on_hide(self):
        """Hook chamado quando a página é ocultada."""
        pass
