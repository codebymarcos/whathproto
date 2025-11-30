"""Interface do app de armazenamento."""
from core import Page, Txt, Btn
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import logic  # Import absoluto pois o diretório está no sys.path

class StoragePage(Page):
    """App de gerenciamento de armazenamento."""
    
    def __init__(self):
        """Inicializa com fundo azul."""
        super().__init__(bg_color=(0.2, 0.3, 0.5, 1))
        
        # Título
        self.add_widget(Txt(text="Armazenamento", size=24, bold=True, color=(1,1,1,1)))
        
        # Área de rolagem para informações
        scroll = ScrollView(size_hint=(1, 0.8))
        
        # Container para conteúdo
        self.content = GridLayout(cols=1, spacing=10, padding=10, size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter('height'))
        
        scroll.add_widget(self.content)
        self.add_widget(scroll)
        
        # Botão voltar
        btn = Btn(text="Voltar", bg=(0.8, 0.8, 0.8, 0.3))
        btn.bind(on_release=self._go_back)
        self.add_widget(btn)
        
    def on_show(self):
        """Carrega informações ao exibir."""
        print("→ Storage App")
        self._load_storage_info()
        
    def _load_storage_info(self):
        """Carrega e exibe informações do disco usando lógica separada."""
        self.content.clear_widgets()
        
        # Obtém informações via lógica
        info = logic.get_storage_info()
        
        if info:
            # Exibe informações formatadas
            total_mb = logic.format_size(info.get('total_size', 0))
            self.content.add_widget(
                Txt(text=f"Tamanho: {total_mb}", size=16, color=(1,1,1,1))
            )
            
            file_count = info.get('file_count', 0)
            self.content.add_widget(
                Txt(text=f"Arquivos: {file_count}", size=16, color=(1,1,1,1))
            )
            
            path = info.get('path', 'N/A')
            self.content.add_widget(
                Txt(text=f"Local: {path}", size=12, color=(0.8,0.8,0.8,1))
            )
            
            # Separador
            self.content.add_widget(Txt(text="─" * 20, size=14, color=(1,1,1,1)))
            
            # Lista de arquivos via lógica
            contents = logic.list_contents(limit=10)
            
            if contents:
                self.content.add_widget(
                    Txt(text="Conteúdo:", size=18, bold=True, color=(1,1,1,1))
                )
                
                for item in contents:
                    text = logic.format_item_text(item)
                    self.content.add_widget(
                        Txt(text=text, size=12, color=(1,1,1,1))
                    )
            else:
                self.content.add_widget(
                    Txt(text="Disco vazio", size=14, color=(0.8,0.8,0.8,1))
                )
        else:
            self.content.add_widget(
                Txt(text="Erro ao obter informações", size=14, color=(1,0.5,0.5,1))
            )
        
    def _go_back(self, instance):
        """Volta para a home."""
        app = App.get_running_app()
        app.nav.go('interactive_home', direction='right')
