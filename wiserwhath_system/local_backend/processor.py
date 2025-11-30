"""Processador de dados local (Backend Offline)."""
import math
import random
from datetime import datetime

class LocalProcessor:
    """Realiza processamento de dados localmente."""
    
    def process_data(self, data):
        """
        Processa dados brutos.
        
        Args:
            data: Dicionário ou lista de dados
            
        Returns:
            dict: Resultado do processamento
        """
        # Simula processamento pesado
        result = {
            'timestamp': datetime.now().isoformat(),
            'status': 'processed',
            'analysis': self._analyze(data)
        }
        return result
    
    def _analyze(self, data):
        """Análise interna dos dados."""
        # Lógica simulada
        if isinstance(data, list):
            return {
                'count': len(data),
                'sum': sum(x for x in data if isinstance(x, (int, float))),
                'avg': sum(x for x in data if isinstance(x, (int, float))) / len(data) if data else 0
            }
        return {'type': str(type(data)), 'content_preview': str(data)[:50]}
    
    def calculate_metrics(self):
        """Gera métricas do sistema simuladas."""
        return {
            'cpu_load': random.randint(10, 40),
            'memory_usage': random.randint(200, 500),
            'battery_level': random.randint(80, 100),
            'uptime_seconds': 12345
        }
