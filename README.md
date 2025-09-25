# Mão Amiga - Classificação de Ações Beneficentes

## Configurações para Ambiente de Desenvolvimento

Todo o projeto está sendo desenvolvido dentro de um ambiente virtal do Python (venv). Para inicializar o projeto corretamente, siga as instruções abaixo:

1. Inicialize um ambiente virtual com os seguintes comandos:
   1.1. Ambientes Linux (Ubuntu, Debian etc.)

```sh
python3 -m venv .venv # Só precisa ser executado na primeira vez que baixar o repositório
source .venv/bin/activate # Deve ser executado toda vez que abrir o projeto
```

    1.2. Ambientes Windows (PowerShell)

```ps1
py -m venv .venv

Set-ExecutionPolicy Unrestricted -Scope User  # Garante que seu ambiente permite a execução de scripts. Se "Scope" for definido como "User", só precisa ser executado uma vez
./.venv/bin/Activate.ps1 # Deve ser executado toda vez que abrir o projeto
```

2. Instale todas as dependências necessárias com o `pip`:

```sh
pip install -r requirements.txt
```
