## Template para criação de apps do VWApp.

Para usar precisa-se instalar o cookiecutter.

Documentação: https://cookiecutter.readthedocs.io/en/1.7.0/index.html

### Pip

```
pip3 install cookiecutter
```

### MACOS

```
$ brew install cookiecutter
```

### Ubuntu

```
$ sudo apt-get install cookiecutter
```

### Uso

Ai instalar o cookiecutter é só pegar a url do template e gerar o pacote.

```
cookiecutter https://github.com/<UserName>/<nome-do-template>.git
OU
cookiecutter local-template/
```

### Filtros

O filtros são funções python que ficam ao lado direito do valor que será aplicado o filtro separado por um pipe.

```
{{Victor Deon | lower | replace(' ', '-') }}
```

Filtros padrões:

* **lower**: Deixa os caracteres minusculos.
* **replace(target, value)**: Troca todos os target pelos values.
* **dictsort**: Usado para ordenar o dicionários.

### Python

Pode-se usar o cookiecutter com python tb.

```
from cookiecutter.main import cookiecutter
from datetime import datetime

cookiecutter(
    'https://github.com/VictorDeon/vwapp-cookiecutter.git',
    # Um dicionário de contexto que substitui a configuração padrão e do usuário.
    extra_context={
        "project_name": 'TheGreatest',
        "timestamp": datetime.utcnow().isoformat(),
        "file_types": {
            "png": {
                "name": "Portable Network Graphic",
                "library": "libpng",
                "apps": [
                    "GIMP"
                ]
            },
            "bmp": {
                "name": "Bitmap",
                "library": "libbmp",
                "apps": [
                    "Paint",
                    "GIMP"
                ]
            }
        }
    },
    # Remove o uso do shell para sobrescrever as opções.
    no_input=True,
    # Sobrescreva o conteúdo do diretório de saída, se ele já existir.
    overwrite_if_exists=False,
    # Local onde será gerado o resultado do cookiecutter.
    output_dir='.'
)
```