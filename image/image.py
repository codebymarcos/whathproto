"""Ponto de entrada do aplicativo."""
import sys
from pathlib import Path

# Adiciona wiserwhath_system ao path
wiserwhath_path = Path(__file__).parent.parent / "wiserwhath_system"
if str(wiserwhath_path) not in sys.path:
    sys.path.insert(0, str(wiserwhath_path))

from config import APP_CONFIG, TIME_CONFIG
from kivy.config import Config
from kivy.clock import Clock  # Import necessário para agendamento

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
from hardware import CacheManager

# Importa páginas dos módulos
from src.kickstart import Kickstart
from src.interactive_home import InteractiveHome
from src.drop import Drop
from src.clock import Clock as ClockPage  # Renomeado para evitar conflito
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
        
        # Inicializa o Gerenciador de Cache (Hardware)
        cache_dest = storage_path / "cache"
        project_root = Path(__file__).parent
        self.cache_manager = CacheManager(project_root, cache_dest)
        
        # Executa cache inicial
        self._run_cache_update(0)
        
        # Agenda execução periódica a cada 60 segundos (1 minuto)
        Clock.schedule_interval(self._run_cache_update, 60.0)
        print(f"→ Cache System agendado (60s)")
        
        # Inicializa o Loader de Apps
        apps_path = self.fs_driver.disk_path / "app"
        self.app_loader = AppLoader(apps_path)
        print(f"→ AppLoader inicializado")
        
        # Cria navegação
        nav = Nav()
        nav.add('kickstart', Kickstart())
        nav.add('interactive_home', InteractiveHome())
        nav.add('drop', Drop())
        nav.add('clock', ClockPage())
        nav.add('settings', Settings())
        nav.add('about', About())
        
        self.nav = nav
        nav.kickstart()
        
        # Inicia o timer de inatividade após o kickstart
        self.manager.start_inactivity_timer()
        
        return nav

    def _run_cache_update(self, dt):
        """Executa a atualização do cache em background."""
        try:
            # Em um app real, isso deveria rodar em uma Thread separada para não travar a UI
            # Como é uma operação de disco, pode ser lenta
            stats = self.cache_manager.relocate_caches()
            if stats['moved'] > 0:
                print(f"⚡ Cache System: {stats['moved']} novos arquivos processados")
        except Exception as e:
            print(f"Erro no Cache System: {e}")

if __name__ == '__main__':
    WatchApp().run()