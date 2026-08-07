\# Tutor Python Local



Assistente de programação 100% local, privado e offline, focado em ensino de Python. Roda inteiramente na sua máquina usando um modelo GGUF via `llama-cpp-python`, com interface gráfica moderna feita em `customtkinter`.



Nenhum dado é enviado para a internet. Tudo roda local.



\## Funcionalidades



\- Chat com streaming de resposta (token por token)

\- 4 perfis de assistente: Tutor Didático, Code Review, Debug Assist, Livre

\- 5 paletas de cores: Verde Matrix, Azul Ocean, Roxo Cyber, Laranja Sunset, Vermelho Dark

\- Controle de parâmetros do modelo: temperatura, max tokens, top-p

\- 8 snippets rápidos de prompts comuns

\- Exportação de conversa em TXT, Markdown e JSON

\- Barra de status com métricas em tempo real (tokens, velocidade)

\- Botão "Parar" para interromper geração

\- Sistema de log interno

\- Atalhos de teclado completos

\- Persistência automática de configurações



\## Requisitos



\- Python 3.10 ou superior (recomendado 3.12)

\- Windows 10/11, Linux ou macOS

\- GPU NVIDIA recomendada (funciona em CPU também)

\- \~6 GB de espaço para o modelo



\## Instalação



\### 1. Clonar o repositório



```bash

git clone https://github.com/SEU\_USUARIO/tutor-python-local.git

cd tutor-python-local

```



\### 2. Instalar dependências



```bash

pip install customtkinter llama-cpp-python

```



Para usar GPU NVIDIA (recomendado):



```bash

pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu122

```



\### 3. Baixar o modelo



Baixe um modelo GGUF compatível (ex: Qwen3.5-9B Q4\_K\_M) e coloque na raiz do projeto com o nome `modelo.gguf`.



Sugestão: \[Qwen3.5-9B-Claude-4.6-HighIQ GGUF](https://huggingface.co/mradermacher/Qwen3.5-9B-Claude-4.6-HighIQ-INSTRUCT-HERETIC-UNCENSORED-GGUF)



\### 4. Executar



```bash

python app.py

```



\## Atalhos



| Atalho | Ação |

|--------|------|

| `Enter` | Nova linha |

| `Ctrl+Enter` | Enviar mensagem |

| `Ctrl+N` | Nova conversa |

| `Ctrl+S` | Exportar conversa |

| `Ctrl+L` | Abrir log |

| `Esc` | Parar geração |



\## Estrutura



```

tutor-python-local/

├── app.py              # Aplicação principal

├── .gitignore

├── README.md

├── config.json         # Gerado automaticamente

├── log.txt             # Gerado automaticamente

├── exportacoes/        # Conversas exportadas

└── modelo.gguf         # Baixe separadamente

```



\## Configuração



Na primeira execução, o arquivo `config.json` é criado automaticamente com:



\- Caminho do modelo

\- Uso de GPU

\- Parâmetros de inferência (temperatura, max\_tokens, top\_p)

\- Perfil ativo

\- Paleta de cores

\- Modo de aparência



Edite manualmente ou use a sidebar da aplicação.



\## Troubleshooting



\*\*Erro: `nmake not found` ao instalar llama-cpp-python\*\*

Use wheel pré-compilado:

```bash

pip install llama-cpp-python --only-binary=:all: --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

```



\*\*Erro: caminho longo no Windows\*\*

Ative LongPathsEnabled no registro:

```powershell

New-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force

```



\*\*Modelo lento\*\*

Verifique se está usando GPU. O log mostra `GPU=True` quando carregado corretamente.



\## Licença



MIT

