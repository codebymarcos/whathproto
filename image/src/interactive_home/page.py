"""Página Interactive Home."""
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from core import Page, Notification, Icon, Txt

class InteractiveHome(Page):
    """Home com lista de apps."""
    
    def __init__(self):
        """Inicializa com imagem de fundo."""
        super().__init__(bg_image="assets/plan.jpeg")
        
        # Título
        self.add_widget(Txt(text="Apps", size=24, bold=True, color=(1,1,1,1)))
        
        # Área de rolagem para os apps
        scroll = ScrollView(size_hint=(1, 1))
        
        # Grid para ícones
        self.grid = GridLayout(cols=3, spacing=10, padding=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        scroll.add_widget(self.grid)
        self.add_widget(scroll)
    
    def on_show(self):
        """Carrega lista de apps ao exibir."""
        print("→ Interactive Home")
        self._load_apps()
    
    def _load_apps(self):
        """Carrega apps do disco e cria ícones."""
        self.grid.clear_widgets()
        app = App.get_running_app()
        
        if hasattr(app, 'app_loader'):
            apps = app.app_loader.list_apps()
            
            if not apps:
                self.grid.add_widget(Txt(text="Nenhum app", size=14))
                return
                
            for app_data in apps:
                # Container para ícone + nome
                item = GridLayout(cols=1, size_hint=(None, None), size=(80, 100))
                
                # Ícone
                icon = Icon(icon=app_data.get('icon', 'application'), size=60)
                icon.bind(on_release=lambda x, aid=app_data['id']: self._launch_app(aid))
                
                # Nome
                name = Txt(text=app_data.get('name', 'App'), size=12, color=(1,1,1,1))
                
                item.add_widget(icon)
                item.add_widget(name)
                self.grid.add_widget(item)
    
    def _launch_app(self, app_id):
        """Inicia o app selecionado."""
        print(f"Lançando app: {app_id}")
        app = App.get_running_app()
        if hasattr(app, 'app_loader'):
            success = app.app_loader.launch_app(app_id)
            if not success:
                # Mostra erro se falhar
                notif = Notification(message="Erro ao abrir app", icon="alert-circle")
                self.add_widget(notif)
                notif.show()
    
    def on_touch_down(self, touch):
        """Captura início do toque para detectar swipe."""
        touch.ud['start_x'] = touch.x
        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        """Detecta swipe para a esquerda (ir para Drop)."""
        if 'start_x' in touch.ud:
            dx = touch.x - touch.ud['start_x']
            
            # Swipe para esquerda (< -50px)
            if dx < -50:
                app = App.get_running_app()
                if hasattr(app, 'nav'):
                    app.nav.go('drop', direction='left')
                    return True
        
        return super().on_touch_up(touch)
