from core import Page, Txt, Btn, Icon
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

class ProcessesPage(Page):
    """Gerenciador de processos em background."""
    
    def __init__(self):
        """Inicializa com fundo escuro."""
        super().__init__(bg_color=(0.15, 0.15, 0.15, 1))
        
        # Cabeçalho
        header = BoxLayout(size_hint_y=None, height=50, padding=10)
        header.add_widget(Txt(text="Processos Ativos", size=20, bold=True, color=(1,1,1,1)))
        self.add_widget(header)
        
        # Área de rolagem
        scroll = ScrollView(size_hint=(1, 1))
        self.content = GridLayout(cols=1, spacing=5, padding=10, size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter('height'))
        
        scroll.add_widget(self.content)
        self.add_widget(scroll)
        
        # Botão fechar (simulando voltar para cima)
        close_btn = Btn(text="▲ Fechar", bg=(1, 1, 1, 0.1), size_hint_y=None, height=40)
        close_btn.bind(on_release=self._close)
        self.add_widget(close_btn)
        
    def on_show(self):
        """Atualiza lista ao abrir."""
        self._load_processes()
        
    def _load_processes(self):
        """Lista apps carregados."""
        self.content.clear_widgets()
        app = App.get_running_app()
        
        # Lista apps do sistema (fixos)
        system_apps = [
            ("Home", "home"),
            ("Relógio", "clock-outline"),
            ("Configurações", "cog"),
            ("Sobre", "information")
        ]
        
        self.content.add_widget(Txt(text="Sistema", size=14, color=(0.5, 0.5, 1, 1), bold=True))
        
        for name, icon in system_apps:
            self._add_process_item(name, icon, "Executando")
            
        # Lista apps do usuário (carregados pelo Loader)
        if hasattr(app, 'app_loader'):
            self.content.add_widget(Txt(text="Apps Usuário", size=14, color=(0.5, 1, 0.5, 1), bold=True))
            
            # Apps instalados (simulando processos por enquanto)
            apps = app.app_loader.list_apps()
            for app_data in apps:
                self._add_process_item(
                    app_data.get('name', 'App'),
                    app_data.get('icon', 'application'),
                    "Em espera"
                )

    def _add_process_item(self, name, icon_name, status):
        """Adiciona um item à lista."""
        item = BoxLayout(size_hint_y=None, height=50, padding=5)
        
        # Ícone
        icon = Icon(icon=icon_name, size=30, theme_text_color="Custom", text_color=(1,1,1,1))
        icon.size_hint_x = None
        icon.width = 40
        
        # Info
        info = BoxLayout(orientation='vertical')
        info.add_widget(Txt(text=name, size=16, color=(1,1,1,1), halign='left'))
        info.add_widget(Txt(text=status, size=12, color=(0.7,0.7,0.7,1), halign='left'))
        
        item.add_widget(icon)
        item.add_widget(info)
        
        # Fundo do item
        with item.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(1, 1, 1, 0.05)
            RoundedRectangle(pos=item.pos, size=item.size, radius=[5])
            
        self.content.add_widget(item)

    def _close(self, instance):
        """Fecha voltando para a tela anterior (animação para cima)."""
        app = App.get_running_app()
        app.nav.go('interactive_home', direction='up')
