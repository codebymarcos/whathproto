"""Interface do app de armazenamento - Design Minimalista."""
from core import Page, Txt, Btn, Icon, Notification
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle, Line
import logic
import shutil
from pathlib import Path

class StoragePage(Page):
    """App de gerenciamento de armazenamento - Design P&B Minimalista."""
    
    def __init__(self):
        """Inicializa com design limpo preto e branco."""
        super().__init__(bg_color=(1, 1, 1, 1))  # Fundo branco puro
        
        # Cabeçalho minimalista
        header = BoxLayout(size_hint_y=None, height=70, padding=15, spacing=10)
        
        # Ícone simples
        disk_icon = Icon(icon="harddisk", size=35, theme_text_color="Custom", text_color=(0, 0, 0, 1))
        disk_icon.size_hint_x = None
        disk_icon.width = 45
        
        # Título
        title_box = BoxLayout(orientation='vertical', spacing=2)
        title_box.add_widget(Txt(text="Armazenamento", size=20, bold=True, color=(0, 0, 0, 1), halign='left'))
        title_box.add_widget(Txt(text="Gerenciador de disco", size=11, color=(0.4, 0.4, 0.4, 1), halign='left'))
        
        header.add_widget(disk_icon)
        header.add_widget(title_box)
        self.add_widget(header)
        
        # Linha divisória
        divider1 = BoxLayout(size_hint_y=None, height=1, padding=[15, 0])
        with divider1.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            divider1_rect = RoundedRectangle(pos=divider1.pos, size=divider1.size)
        divider1.bind(pos=lambda *args: setattr(divider1_rect, 'pos', divider1.pos),
                      size=lambda *args: setattr(divider1_rect, 'size', divider1.size))
        self.add_widget(divider1)
        
        # Card de estatísticas (minimalista)
        self.stats_card = BoxLayout(orientation='vertical', size_hint_y=None, height=100, padding=15, spacing=8)
        self.add_widget(self.stats_card)
        
        # Botão Limpar Cache
        cache_btn_container = BoxLayout(size_hint_y=None, height=60, padding=[15, 5])
        cache_btn = Btn(text="🗑️ Limpar Cache", size_hint=(1, None), height=45)
        cache_btn.md_bg_color = (0.95, 0.95, 0.95, 1)
        cache_btn.text_color = (0.2, 0.2, 0.2, 1)
        cache_btn.bind(on_release=self._clear_cache)
        cache_btn_container.add_widget(cache_btn)
        self.add_widget(cache_btn_container)
        
        # Linha divisória
        divider2 = BoxLayout(size_hint_y=None, height=1, padding=[15, 0])
        with divider2.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            divider2_rect = RoundedRectangle(pos=divider2.pos, size=divider2.size)
        divider2.bind(pos=lambda *args: setattr(divider2_rect, 'pos', divider2.pos),
                      size=lambda *args: setattr(divider2_rect, 'size', divider2.size))
        self.add_widget(divider2)
        
        # Label "Arquivos"
        files_header = BoxLayout(size_hint_y=None, height=40, padding=[15, 10])
        files_header.add_widget(Txt(text="Arquivos", size=14, bold=True, color=(0, 0, 0, 1), halign='left'))
        self.add_widget(files_header)
        
        # ScrollView para lista de arquivos
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        
        # Container para arquivos
        self.content = GridLayout(cols=1, spacing=0, padding=[15, 0, 15, 15], size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter('height'))
        
        scroll.add_widget(self.content)
        self.add_widget(scroll)
        
        # Botão voltar minimalista
        btn_container = BoxLayout(size_hint_y=None, height=70, padding=15)
        btn = Btn(text="← Voltar", size_hint=(1, None), height=50)
        btn.md_bg_color = (0, 0, 0, 1)
        btn.text_color = (1, 1, 1, 1)
        btn.bind(on_release=self._go_back)
        btn_container.add_widget(btn)
        self.add_widget(btn_container)
        
    def on_show(self):
        """Carrega informações ao exibir."""
        print("→ Storage App")
        self._load_storage_info()
    
    def _clear_cache(self, instance):
        """Limpa o cache do Python."""
        try:
            app = App.get_running_app()
            cache_path = app.fs_driver.disk_path / "storage" / "cache"
            
            if cache_path.exists():
                # Remove todos os arquivos e pastas dentro de cache
                for item in cache_path.iterdir():
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
                
                # Mostra notificação de sucesso
                notif = Notification(message="Cache limpo com sucesso!", icon="check-circle")
                self.add_widget(notif)
                notif.show()
                
                # Recarrega as informações
                self._load_storage_info()
                
                print("✓ Cache limpo")
            else:
                notif = Notification(message="Pasta de cache não encontrada", icon="alert-circle")
                self.add_widget(notif)
                notif.show()
                
        except Exception as e:
            print(f"Erro ao limpar cache: {e}")
            notif = Notification(message="Erro ao limpar cache", icon="alert-circle")
            self.add_widget(notif)
            notif.show()
        
    def _load_storage_info(self):
        """Carrega e exibe informações do disco."""
        self.stats_card.clear_widgets()
        self.content.clear_widgets()
        
        # Obtém informações
        info = logic.get_storage_info()
        
        if info:
            # Grid de estatísticas (2 colunas, minimalista)
            stats_grid = GridLayout(cols=2, spacing=15, size_hint_y=None, height=60)
            
            # Tamanho total
            total_mb = logic.format_size(info.get('total_size', 0))
            stats_grid.add_widget(self._create_stat_item("Tamanho", total_mb))
            
            # Número de arquivos
            file_count = info.get('file_count', 0)
            stats_grid.add_widget(self._create_stat_item("Arquivos", str(file_count)))
            
            self.stats_card.add_widget(stats_grid)
            
            # Caminho (texto pequeno)
            path_text = info.get('path', 'N/A')
            if len(path_text) > 40:
                path_text = "..." + path_text[-37:]
            self.stats_card.add_widget(Txt(text=path_text, size=9, color=(0.5, 0.5, 0.5, 1)))
            
            # Lista de arquivos
            contents = logic.list_contents(limit=20)
            
            if contents:
                for item in contents:
                    file_item = self._create_file_item(item)
                    self.content.add_widget(file_item)
            else:
                empty_box = BoxLayout(size_hint_y=None, height=100, padding=20)
                empty_box.add_widget(Txt(text="Disco vazio", size=13, color=(0.6, 0.6, 0.6, 1)))
                self.content.add_widget(empty_box)
        else:
            self.stats_card.add_widget(
                Txt(text="Erro ao obter informações", size=13, color=(0.8, 0, 0, 1))
            )
    
    def _create_stat_item(self, label, value):
        """Cria um item de estatística minimalista."""
        box = BoxLayout(orientation='vertical', spacing=4)
        box.add_widget(Txt(text=label, size=10, color=(0.5, 0.5, 0.5, 1)))
        box.add_widget(Txt(text=value, size=18, bold=True, color=(0, 0, 0, 1)))
        return box
    
    def _create_file_item(self, item):
        """Cria um item de arquivo minimalista."""
        name = item['name']
        size = item['size']
        is_dir = item['is_dir']
        
        # Container do item
        item_box = BoxLayout(size_hint_y=None, height=55, padding=[0, 8], spacing=12)
        
        # Linha divisória superior
        with item_box.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            line = Line(points=[0, 0, 0, 0], width=1)
        
        def update_line(*args):
            line.points = [item_box.x, item_box.top, item_box.right, item_box.top]
        
        item_box.bind(pos=update_line, size=update_line)
        
        # Ícone (símbolo unicode simples)
        icon_text = "📁" if is_dir else "📄"
        icon_label = Txt(text=icon_text, size=24, halign='center')
        icon_label.size_hint_x = None
        icon_label.width = 40
        
        # Info
        info_box = BoxLayout(orientation='vertical', spacing=2)
        
        # Nome (truncado)
        display_name = name if len(name) <= 25 else name[:22] + "..."
        info_box.add_widget(Txt(text=display_name, size=13, color=(0, 0, 0, 1), halign='left'))
        
        # Tamanho
        size_text = "Pasta" if is_dir else f"{size} bytes"
        if not is_dir and size > 1024:
            size_text = f"{size / 1024:.1f} KB"
        if not is_dir and size > 1024 * 1024:
            size_text = f"{size / (1024 * 1024):.1f} MB"
        info_box.add_widget(Txt(text=size_text, size=10, color=(0.5, 0.5, 0.5, 1), halign='left'))
        
        item_box.add_widget(icon_label)
        item_box.add_widget(info_box)
        
        return item_box
        
    def _go_back(self, instance):
        """Volta para a home."""
        app = App.get_running_app()
        app.nav.go('interactive_home', direction='right')
