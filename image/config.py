"""Configurações globais do aplicativo."""

# Configurações da aplicação
APP_CONFIG = {
    'title': 'Watch Prototype',
    'screen_width': 280,
    'screen_height': 260
}

# Configurações de tempo (em segundos)
TIME_CONFIG = {
    'kickstart_duration': 3.0,      # Duração total da tela inicial
    'kickstart_typing_speed': 0.15, # Velocidade de digitação (por letra)
    'kickstart_exit_delay': 1.0,    # Tempo de espera após digitar antes de sair
    'inactivity_timeout': 15.0,     # Tempo sem uso para mostrar relógio
    'notification_duration': 3.0,   # Tempo de exibição da notificação
    'clock_update_interval': 1.0    # Intervalo de atualização do relógio
}

# Rotas (Mapeamento de nomes para classes/arquivos)
ROUTES = {
    'kickstart': 'kickstart',
    'interactive_home': 'interactive_home',
    'drop': 'drop',
    'clock': 'clock',
    'settings': 'settings',
    'about': 'about'
}

# Constantes de rotas para uso no código
ROUTE_KICKSTART = 'kickstart'
ROUTE_INTERACTIVE_HOME = 'interactive_home'
ROUTE_DROP = 'drop'
ROUTE_CLOCK = 'clock'
ROUTE_SETTINGS = 'settings'
ROUTE_ABOUT = 'about'