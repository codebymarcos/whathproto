"""Página Drop - Menu de Aplicativos."""
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle
from core import Page, Txt, AppGrid

class Drop(Page):
    """Tela Drop com menu de aplicativos em container."""
    
    def __init__(self):
        """Inicializa com fundo estilo drawer."""
        super().__init__(bg_color=(0.1, 0.1, 0.1, 0.95))
        
        # Cabeçalho
        header = BoxLayout(size_hint_y=None, height=60, padding=20)
        header.add_widget(Txt(text="Aplicativos", size=24, bold=True, color=(1, 1, 1, 1), halign='left'))
        self.add_widget(header)
        
        # Container Principal com Padding
        main_container = BoxLayout(padding=[15, 0, 15, 15])
        
        # Container de Fundo dos Apps (Card)
        apps_container = BoxLayout(orientation='vertical')
        
        # Fundo do container de apps
        with apps_container.canvas.before:
            Color(0.2, 0.2, 0.2, 0.8)  # Cinza escuro
            self.apps_bg = RoundedRectangle(pos=apps_container.pos, size=apps_container.size, radius=[20])
            
        apps_container.bind(
            pos=lambda *args: setattr(self.apps_bg, 'pos', apps_container.pos),
            size=lambda *args: setattr(self.apps_bg, 'size', apps_container.size)
        )
        
        # ScrollView DENTRO do container
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        
        # Grid de apps
        self.app_grid = AppGrid(padding=15)
        # Garante que o grid cresça para permitir scroll
        self.app_grid.bind(minimum_height=self.app_grid.setter('height'))
        
        scroll.add_widget(self.app_grid)
        apps_container.add_widget(scroll)
        
        main_container.add_widget(apps_container)
        self.add_widget(main_container)
    
    def on_show(self):
        """Carrega apps ao exibir."""
        print("→ Drop (App Menu)")
        self._load_apps()
    
    def _load_apps(self):
        """Carrega apps dinamicamente."""
        app = App.get_running_app()
        
        # Limpa grid
        self.app_grid.clear_widgets()
        self.app_grid.rows = []
        self.app_grid.current_row = None
        
        if hasattr(app, 'app_loader'):
            apps = app.app_loader.list_apps()
            
            colors = [
                (0.2, 0.4, 0.8, 1),
                (0.8, 0.2, 0.4, 1),
                (0.2, 0.7, 0.3, 1),
                (0.9, 0.6, 0.1, 1),
                (0.6, 0.2, 0.8, 1),
                (0.1, 0.6, 0.8, 1),
            ]
            
            for i, app_data in enumerate(apps):
                icon = app_data.get('icon', 'application')
                name = app_data.get('name', 'App')
                app_id = app_data['id']
                color = colors[i % len(colors)]
                
                self.app_grid.add_app(
                    icon=icon,
                    name=name,
                    callback=lambda aid=app_id: self._launch_app(aid),
                    bg_color=color
                )
    
    def _launch_app(self, app_id):
        """Lança um app."""
        print(f"Lançando app: {app_id}")
        app = App.get_running_app()
        if hasattr(app, 'app_loader'):
            app.app_loader.launch_app(app_id)
