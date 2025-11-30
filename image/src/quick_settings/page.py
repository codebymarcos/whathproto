"""Quick Settings - Sidebar de configurações rápidas."""
from core import Page, Txt, Btn, QuickToggle, VolumeSlider
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

class QuickSettings(Page):
    """Sidebar de configurações rápidas (Wi-Fi, Bluetooth, etc)."""
    
    def __init__(self):
        """Inicializa com design minimalista."""
        super().__init__(bg_color=(0.95, 0.95, 0.95, 1))
        
        # Cabeçalho
        header = BoxLayout(size_hint_y=None, height=60, padding=15)
        header.add_widget(Txt(text="Central de Controle", size=18, bold=True, color=(0, 0, 0, 1), halign='left'))
        self.add_widget(header)
        
        # Container Principal (Horizontal)
        main_container = BoxLayout(orientation='horizontal', padding=[15, 0], spacing=15, size_hint_y=None, height=150)
        
        # Coluna Esquerda: Grid de Toggles (2x2)
        # Ajustado para 2 colunas para caber ao lado do volume
        toggles_grid = GridLayout(cols=2, spacing=15, size_hint=(None, None), width=135, height=135)
        
        # Wi-Fi
        self.wifi_toggle = QuickToggle(icon="wifi", callback=self._toggle_wifi)
        toggles_grid.add_widget(self.wifi_toggle)
        
        # Bluetooth
        self.bt_toggle = QuickToggle(icon="bluetooth", callback=self._toggle_bluetooth)
        toggles_grid.add_widget(self.bt_toggle)
        
        # Modo Avião
        self.airplane_toggle = QuickToggle(icon="airplane", callback=self._toggle_airplane)
        toggles_grid.add_widget(self.airplane_toggle)
        
        # Não Perturbe
        self.dnd_toggle = QuickToggle(icon="bell-off", callback=self._toggle_dnd)
        toggles_grid.add_widget(self.dnd_toggle)
        
        main_container.add_widget(toggles_grid)
        
        # Coluna Direita: Volume Slider
        # Ocupa o espaço restante ou tamanho fixo
        volume_container = BoxLayout(size_hint=(None, None), size=(60, 135))
        self.volume_slider = VolumeSlider()
        volume_container.add_widget(self.volume_slider)
        
        main_container.add_widget(volume_container)
        
        self.add_widget(main_container)
        
        # Espaçador
        self.add_widget(BoxLayout())
        
        # Botão fechar
        btn_container = BoxLayout(size_hint_y=None, height=70, padding=15)
        btn = Btn(text="← Fechar", size_hint=(1, None), height=50)
        btn.md_bg_color = (0, 0, 0, 1)
        btn.text_color = (1, 1, 1, 1)
        btn.bind(on_release=self._close)
        btn_container.add_widget(btn)
        self.add_widget(btn_container)
        
    def on_show(self):
        """Atualiza status ao exibir."""
        print("→ Quick Settings")
        self._update_status()
        Clock.schedule_interval(self._update_status, 3.0)
    
    def on_hide(self):
        """Para atualizações ao esconder."""
        Clock.unschedule(self._update_status)
    
    def _update_status(self, dt=None):
        """Atualiza status de Wi-Fi e Bluetooth."""
        try:
            import sys
            from pathlib import Path
            wiserwhath_path = Path(__file__).parent.parent.parent.parent / "wiserwhath_system"
            if str(wiserwhath_path) not in sys.path:
                sys.path.insert(0, str(wiserwhath_path))
            
            from hardware.network import get_wifi_status, get_bluetooth_status
            
            wifi_status = get_wifi_status()
            self.wifi_toggle.set_active(wifi_status['enabled'])
            
            bt_status = get_bluetooth_status()
            self.bt_toggle.set_active(bt_status['enabled'])
            
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")
    
    def _toggle_wifi(self, active):
        try:
            from hardware.network import toggle_wifi
            toggle_wifi()
            self._update_status()
        except Exception as e:
            print(f"Erro ao alternar Wi-Fi: {e}")
    
    def _toggle_bluetooth(self, active):
        try:
            from hardware.network import toggle_bluetooth
            toggle_bluetooth()
            self._update_status()
        except Exception as e:
            print(f"Erro ao alternar Bluetooth: {e}")
            
    def _toggle_airplane(self, active):
        print(f"Modo Avião: {active}")
        
    def _toggle_dnd(self, active):
        print(f"Não Perturbe: {active}")
    
    def _close(self, instance):
        app = App.get_running_app()
        app.nav.go('interactive_home', direction='right')
