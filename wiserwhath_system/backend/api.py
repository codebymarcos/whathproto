"""Cliente de API HTTP para comunicação com backend."""
import json
from urllib import request, error
from urllib.parse import urlencode

class APIClient:
    """Cliente HTTP simples para requisições REST."""
    
    def __init__(self, base_url=None, timeout=10):
        """
        Inicializa o cliente de API.
        
        Args:
            base_url: URL base da API (ex: "http://localhost:5000")
            timeout: Timeout em segundos para requisições
        """
        self.base_url = base_url or ""
        self.timeout = timeout
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'WiserWatch/1.0'
        }
    
    def get(self, endpoint, params=None):
        """
        Faz uma requisição GET.
        
        Args:
            endpoint: Endpoint da API (ex: "/users")
            params: Dicionário de parâmetros de query
            
        Returns:
            dict: Resposta JSON ou None se erro
        """
        url = f"{self.base_url}{endpoint}"
        
        if params:
            url += f"?{urlencode(params)}"
        
        try:
            req = request.Request(url, headers=self.headers, method='GET')
            with request.urlopen(req, timeout=self.timeout) as response:
                data = response.read().decode('utf-8')
                return json.loads(data)
        except error.HTTPError as e:
            print(f"HTTP Error {e.code}: {e.reason}")
            return None
        except error.URLError as e:
            print(f"URL Error: {e.reason}")
            return None
        except Exception as e:
            print(f"Erro na requisição GET: {e}")
            return None
    
    def post(self, endpoint, data=None):
        """
        Faz uma requisição POST.
        
        Args:
            endpoint: Endpoint da API
            data: Dicionário de dados a enviar
            
        Returns:
            dict: Resposta JSON ou None se erro
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            body = json.dumps(data or {}).encode('utf-8')
            req = request.Request(url, data=body, headers=self.headers, method='POST')
            
            with request.urlopen(req, timeout=self.timeout) as response:
                response_data = response.read().decode('utf-8')
                return json.loads(response_data)
        except error.HTTPError as e:
            print(f"HTTP Error {e.code}: {e.reason}")
            return None
        except error.URLError as e:
            print(f"URL Error: {e.reason}")
            return None
        except Exception as e:
            print(f"Erro na requisição POST: {e}")
            return None
    
    def put(self, endpoint, data=None):
        """Faz uma requisição PUT."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            body = json.dumps(data or {}).encode('utf-8')
            req = request.Request(url, data=body, headers=self.headers, method='PUT')
            
            with request.urlopen(req, timeout=self.timeout) as response:
                response_data = response.read().decode('utf-8')
                return json.loads(response_data)
        except Exception as e:
            print(f"Erro na requisição PUT: {e}")
            return None
    
    def delete(self, endpoint):
        """Faz uma requisição DELETE."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            req = request.Request(url, headers=self.headers, method='DELETE')
            
            with request.urlopen(req, timeout=self.timeout) as response:
                response_data = response.read().decode('utf-8')
                return json.loads(response_data) if response_data else {}
        except Exception as e:
            print(f"Erro na requisição DELETE: {e}")
            return None
