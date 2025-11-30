"""Ponto de entrada do aplicativo."""
import sys
from pathlib import Path

# Adiciona a raiz do projeto ao path para importar setup_cache
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Configura o cache ANTES de qualquer outro import
from setup_cache import CACHE_DIR

from config import APP_CONFIG, TIME_CONFIG
from kivy.config import Config

# Configurações críticas do Kivy
Config.set('graphics', 'width', str(APP_CONFIG['screen_width']))
Config.set('graphics', 'height', str(APP_CONFIG['screen_height']))
Config.set('graphics', 'resizable', '0')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivymd.app import MDApp
from kivy.core.text import LabelBase
from core import Nav, AppManager, AppLoader

# Importa do wiserwhath_system
from filesystem import FileSystemDriver
from backend import APIClient, LocalStorage
from local_backend import LocalProcessor

# Importa páginas dos módulos
from src.kickstart import Kickstart
from src.interactive_home import InteractiveHome
from src.drop import Drop
from src.quick_settings import QuickSettings
from src.clock import Clock as ClockPage
from src.settings import Settings
from src.about import About

class WatchApp(MDApp):
    """Classe principal da aplicação usando KivyMD."""
    
    def build(self):
        """Constrói a interface do usuário."""
        self.title = APP_CONFIG['title']
        
        # Registra a fonte customizada "Pacifico"
        LabelBase.register(name="Pacifico", fn_regular="assets/fonts/Pacifico-Regular.ttf")
        
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        
        # Inicializa o gerenciador global
        self.manager = AppManager(timeout_seconds=TIME_CONFIG['inactivity_timeout'])
        
        # Inicializa o driver de sistema de arquivos
        self.fs_driver = FileSystemDriver()
        
        # Inicializa o backend (Online)
        self.api_client = APIClient()
        
        # Inicializa o backend (Offline/Local)
        self.local_processor = LocalProcessor()
        
        # Inicializa o armazenamento local
        storage_path = self.fs_driver.disk_path / "storage"
        self.local_storage = LocalStorage(storage_path)
        print(f"→ Backend inicializado (Online & Local)")
        print(f"→ Python Cache: {CACHE_DIR}")
        
        # Inicializa o Loader de Apps
        apps_path = self.fs_driver.disk_path / "app"
        self.app_loader = AppLoader(apps_path)
        print(f"→ AppLoader inicializado")
        
        # Cria navegação
        nav = Nav()
        nav.add('kickstart', Kickstart())
        nav.add('interactive_home', InteractiveHome())
        nav.add('drop', Drop())
        nav.add('quick_settings', QuickSettings())
        nav.add('clock', ClockPage())
        nav.add('settings', Settings())
        nav.add('about', About())
        
        self.nav = nav
        nav.kickstart()
        
        # Inicia o timer de inatividade após o kickstart
        self.manager.start_inactivity_timer()
        
        return nav

if __name__ == '__main__':
    WatchApp().run()