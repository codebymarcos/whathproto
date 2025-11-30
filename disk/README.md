# Disk - Armazenamento do Smartwatch

Esta pasta contém todos os dados e aplicativos do protótipo do smartwatch.

## Estrutura

```
disk/
├── app/              # Aplicativos instalados
│   ├── demo/         # App de demonstração
│   └── storage/      # App de gerenciamento de armazenamento
│
└── storage/          # Dados persistentes (LocalStorage)
    └── *.json        # Arquivos de configuração e cache
```

## Diretórios

### `/app`
Contém todos os mini-apps instalados no smartwatch.

Cada app deve ter:
- `manifest.json` - Metadados (nome, ícone, entry point)
- `main.py` - Código principal com classe que herda de `Page`

### `/storage`
Armazenamento de dados persistentes usado pelo `LocalStorage`.

Os apps podem salvar configurações, cache e outros dados aqui usando:
```python
app.local_storage.set("chave", valor)
app.local_storage.get("chave")
```

## Acesso via Código

O sistema fornece acesso ao disco através de:

```python
from kivy.app import App

app = App.get_running_app()

# FileSystem Driver
app.fs_driver.list_disk_contents()
app.fs_driver.read_file("arquivo.txt")
app.fs_driver.write_file("arquivo.txt", "conteúdo")

# Local Storage (persistência)
app.local_storage.set("config", {"tema": "escuro"})
config = app.local_storage.get("config")

# App Loader
apps = app.app_loader.list_apps()
```

## Notas

- Todo o conteúdo desta pasta é **persistente**
- Apps podem criar subpastas conforme necessário
- O sistema gerencia automaticamente a criação de diretórios
