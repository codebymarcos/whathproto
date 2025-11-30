"""Carregador de Mini Apps dinâmicos."""
import json
import importlib.util
import sys
from pathlib import Path
from kivy.app import App

class AppLoader:
    """Gerencia o carregamento e execução de apps em disk/app."""
    
    def __init__(self, apps_dir):
        """
        Inicializa o loader.
        Args:
            apps_dir (Path): Caminho para a pasta de apps (disk/app)
        """
        self.apps_dir = Path(apps_dir)
        self.loaded_apps = {} # Cache de apps carregados
        
    def list_apps(self):
        """
        Lista apps disponíveis verificando manifest.json.
        Returns:
            list: Lista de dicionários com metadados dos apps
        """
        apps = []
        if not self.apps_dir.exists():
            return apps
            
        for item in self.apps_dir.iterdir():
            if item.is_dir():
                manifest_path = item / "manifest.json"
                if manifest_path.exists():
                    try:
                        with open(manifest_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            # Adiciona o caminho da pasta ao manifesto
                            data['path'] = str(item)
                            data['id'] = data.get('id', item.name)
                            apps.append(data)
                    except Exception as e:
                        print(f"Erro ao ler manifesto de {item.name}: {e}")
        return apps

    def load_app(self, app_id):
        """
        Carrega o módulo do app e retorna a classe da página.
        """
        # Encontra o app na lista
        apps = self.list_apps()
        app_data = next((a for a in apps if a['id'] == app_id), None)
        
        if not app_data:
            print(f"App {app_id} não encontrado.")
            return None
            
        app_path = Path(app_data['path'])
        entry_point = app_path / app_data['entry_point']
        class_name = app_data['class_name']
        
        try:
            # Importação dinâmica
            spec = importlib.util.spec_from_file_location(f"dynamic_app_{app_id}", entry_point)
            module = importlib.util.module_from_spec(spec)
            
            # Adiciona o diretório do app ao sys.path para imports relativos funcionarem
            if str(app_path) not in sys.path:
                sys.path.insert(0, str(app_path))
            
            spec.loader.exec_module(module)
            
            # Obtém a classe
            app_class = getattr(module, class_name)
            return app_class
        except Exception as e:
            print(f"Erro ao carregar app {app_id}: {e}")
            return None

    def launch_app(self, app_id):
        """Instancia o app e navega para ele."""
        app_class = self.load_app(app_id)
        if app_class:
            # Instancia a página
            page_instance = app_class()
            
            # Adiciona ao Nav
            app = App.get_running_app()
            if hasattr(app, 'nav'):
                # Remove rota anterior se existir para recarregar
                if app_id in app.nav._routes:
                    # TODO: Implementar remoção limpa no Nav se necessário
                    pass
                
                # Adiciona (ou substitui) a rota
                app.nav.add(app_id, page_instance)
                
                # Navega
                app.nav.go(app_id)
                return True
        return False
