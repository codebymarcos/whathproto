"""Sistema de navegação simples."""
from kivy.uix.screenmanager import ScreenManager, Screen


class Route(Screen):
    """Wrapper de página para o ScreenManager."""
    
    def __init__(self, page, **kw):
        """Inicializa rota com uma página."""
        super().__init__(**kw)
        self.page = page
        self.add_widget(page)
    
    def on_enter(self):
        """Chama hook on_show da página."""
        if hasattr(self.page, 'on_show'):
            self.page.on_show()
    
    def on_leave(self):
        """Chama hook on_hide da página."""
        if hasattr(self.page, 'on_hide'):
            self.page.on_hide()


class Nav(ScreenManager):
    """Gerenciador de navegação entre páginas."""
    
    def __init__(self, **kw):
        """Inicializa o navegador."""
        super().__init__(**kw)
        self._routes = {}
    
    def add(self, name, page):
        """Adiciona uma página ao navegador."""
        route = Route(page, name=name)
        self._routes[name] = route
        self.add_widget(route)
        return self
    
    def go(self, name, direction='left'):
        """Navega para uma página específica."""
        if name in self._routes:
            self.transition.direction = direction
            self.current = name
        return self
    
    def kickstart(self):
        """Vai para a página inicial (Kickstart)."""
        return self.go('kickstart', 'right')
