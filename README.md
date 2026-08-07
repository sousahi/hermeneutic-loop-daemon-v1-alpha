<h1 align="center">hermeneutic-loop-daemon</h1>

<p align="center">
  <em>Sua IA. Suas regras. Seu modo.</em>
</p>

<p align="center">
  <sub>Uma máquina que ainda lembra como ensinar — agora também pela janela.</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/sousahi/hermeneutic-loop-daemon-v1-alpha?color=a01010&style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/vers%C3%A3o-2.0.0--alpha-a01010?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/modo-local%20%7C%20nuvem-a01010?style=flat-square" alt="Mode">
  <img src="https://img.shields.io/badge/telemetry-none-a01010?style=flat-square" alt="Telemetry">
  <img src="https://img.shields.io/badge/lock--in-zero-a01010?style=flat-square" alt="Lock-in">
  <img src="https://img.shields.io/github/languages/top/sousahi/hermeneutic-loop-daemon-v1-alpha?color=a01010&style=flat-square" alt="Language">
</p>

<p align="center">
  <strong>Licença:</strong> MIT · Copyright (c) 2026 HermeX · sousahi collective · by ByteHub
</p>

---

## O que é isso

Um daemon de diálogo recursivo com **dupla natureza**. Opera em dois modos, escolhidos pelo operador:

- **Local (GGUF)** — modelo na sua máquina, zero internet, privacidade absoluta
- **Nuvem (Hugging Face)** — sem download, funciona em qualquer PC, grátis

Mesmo código. Mesma interface. Mesma filosofia. **Você decide onde a conversa acontece.**

Se você chegou aqui procurando um tutor de Python privado — você encontrou. Se chegou procurando conveniência sem abrir mão da soberania — também encontrou.

## Princípios

- **Soberania é escolha, não dogma.** Local quando importa. Nuvem quando convém.
- **Você segura a chave.** Sempre. Em ambos os modos.
- **Zero lock-in.** Troque de provedor com um clique.
- **Transparência total.** Saiba exatamente pra onde vai cada token.
- **Privacidade não é feature. É premissa.**
- **Ensinamos devagar.** A pressa é inimiga da compreensão.

## Capacidades observadas

- **Modo dual** — Local (GGUF) e Nuvem (Hugging Face) com troca instantânea
- **Fallback automático** — se a nuvem falhar, o daemon cai pro Local sem você perceber
- **6 modelos HF disponíveis** — Qwen3, Llama 3.3, DeepSeek, Mistral, Gemma, Phi-4
- **Tutorial integrado** — guia completo dentro do app pra gerar seu token HF
- Diálogo contínuo com memória de contexto
- Múltiplos modos de interpretação (didático, revisão, depuração, livre)
- Geração token-a-token com interrupção voluntária
- Exportação do ciclo hermenêutico em três formatos (TXT, MD, JSON)
- Métricas de velocidade, volume e **origem** em tempo real
- Persistência automática de estado entre sessões
- Cinco paletas cromáticas para o ambiente visual
- Atalhos de teclado para operadores experientes

## Comparativo de modos

| Aspecto | Local (GGUF) | Nuvem (Hugging Face) |
|:--------|:-------------|:---------------------|
| Download obrigatório | ~6 GB | Zero |
| Requisito de hardware | GPU recomendada | Qualquer PC |
| Tempo até primeiro "olá" | 30-60 min | 2-3 min |
| Privacidade máxima | ✅ Total | ✅ Direto pro HF |
| Conveniência máxima | ❌ | ✅ |
| Funciona offline | ✅ | ❌ |
| Custo | Zero | Zero (tier grátis) |

**Use Local quando:** privacidade absoluta, offline, sessão longa, dados sensíveis.

**Use Nuvem quando:** primeira vez, PC sem GPU, teste rápido, conveniência.

**Use ambos:** fallback automático cobre os dois cenários.

## Requisitos do operador

- Python 3.10 ou superior (recomendado 3.12)
- Sistema operacional moderno (Windows, Linux, macOS)

**Para modo Local:**
- GPU NVIDIA recomendada (funciona em CPU, mais lento)
- ~6 GB de espaço para o substrato cognitivo
- `llama-cpp-python` instalado

**Para modo Nuvem:**
- Conexão com a internet
- Conta gratuita no Hugging Face
- Token pessoal (gerado em 30 segundos)
- `huggingface_hub` instalado

## Ritual de inicialização

### 1. Clonar o códex

```bash
git clone https://github.com/sousahi/hermeneutic-loop-daemon-v1-alpha.git
cd hermeneutic-loop-daemon-v1-alpha
```

### 2. Instalar as dependências do runtime

**Instalação mínima (só Nuvem):**

```bash
pip install customtkinter huggingface_hub
```

**Instalação completa (Nuvem + Local):**

```bash
pip install customtkinter huggingface_hub llama-cpp-python
```

Para acelerar o modo Local via GPU NVIDIA:

```bash
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu122
```

Se o seu sistema recusar a compilação, use a roda pré-forjada:

```bash
pip install llama-cpp-python --only-binary=:all: --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```

### 3A. Ativar o modo Nuvem (recomendado pra começar)

1. Crie conta gratuita em [huggingface.co/join](https://huggingface.co/join)
2. Gere seu token em [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
   - Nome: `hermeneutic-loop-daemon`
   - Tipo: **Read**
   - Copie o token (começa com `hf_`)
3. Abra o daemon, selecione **"Nuvem (Hugging Face)"** na barra lateral
4. Cole seu token, escolha um modelo, clique em **"Testar"**
5. Se aparecer ✓ Conectado, está pronto

> 💡 O botão **"Tutorial HF"** na barra lateral abre um guia completo dentro do app.

### 3B. Ativar o modo Local (opcional)

Baixe um modelo GGUF compatível (sugestão: Qwen3.5-9B Q4_K_M) e coloque na raiz do projeto com o nome `modelo.gguf`.

Fonte sugerida: [Qwen3.5-9B-Claude-4.6-HighIQ GGUF](https://huggingface.co/mradermacher/Qwen3.5-9B-Claude-4.6-HighIQ-INSTRUCT-HERETIC-UNCENSORED-GGUF)

### 4. Despertar o daemon

```bash
python app.py
```

- **Modo Nuvem:** primeira resposta em 2-5 segundos
- **Modo Local:** aguarde 20-40 segundos pro modelo carregar na VRAM

## Modelos disponíveis na Nuvem (gratuitos)

| Modelo | Especialidade | Velocidade |
|:-------|:--------------|:-----------|
| `Qwen/Qwen3-8B` | Tutor geral, Python | ⚡ Rápido |
| `meta-llama/Llama-3.3-70B-Instruct` | Raciocínio complexo | 🐢 Médio |
| `deepseek-ai/DeepSeek-V3-0324` | Código avançado | 🐢 Lento |
| `mistralai/Mistral-7B-Instruct-v0.3` | Respostas curtas | ⚡⚡ Muito rápido |
| `google/gemma-2-9b-it` | Didática clara | ⚡ Rápido |
| `microsoft/Phi-4` | Compacto, eficiente | ⚡ Rápido |

Troque de modelo a qualquer momento pelo dropdown. Sem reiniciar.

## Gestos do operador

| Gesto | Efeito |
|:------|:-------|
| `Enter` | Nova linha no pensamento |
| `Ctrl+Enter` | Enviar ao daemon |
| `Ctrl+N` | Reiniciar o ciclo |
| `Ctrl+S` | Preservar o diálogo |
| `Ctrl+L` | Consultar o registro |
| `Esc` | Interromper a interpretação |

## Modos de interpretação

| Modo | Disposição |
|:-----|:-----------|
| **Tutor Didático** | Paciente, analógico, focado no aprendizado |
| **Code Review** | Técnico, direto, atento a PEP 8 e armadilhas |
| **Debug Assist** | Cirúrgico, causal, preventivo |
| **Livre** | Sem amarras, conversação aberta |

## Paletas cromáticas

| Paleta | Disposição visual |
|:-------|:------------------|
| **Verde Matrix** | Identidade padrão. Terminal vivo. |
| **Azul Ocean** | Profundidade. Foco prolongado. |
| **Roxo Cyber** | Cyberpunk. Sessão noturna. |
| **Laranja Sunset** | Calor. Sessão longa. |
| **Vermelho Dark** | Urgência. Debug intenso. |

## Topologia do códex

```
hermeneutic-loop-daemon/
├── app.py              # Núcleo do daemon (v2.0.0-alpha)
├── .gitignore          # Fronteira do repositório
├── README.md           # Este manuscrito
├── LICENSE             # Pacto de uso (MIT)
├── config.json         # Memória persistente (gerada · nunca commite)
├── log.txt             # Registro do ciclo (gerado)
├── exportacoes/        # Diálogos preservados
└── modelo.gguf         # Substrato cognitivo local (opcional no v2)
```

## Segurança do seu token

Quando em modo Nuvem, seu token HF fica salvo em `config.json` na sua máquina.

- `config.json` está no `.gitignore` — **nunca vaza pro Git**
- O daemon **nunca envia** seu token pra lugar nenhum além do Hugging Face
- Nenhum intermediário, nenhum proxy, nenhum backend próprio
- Se suspeitar de vazamento, revogue em [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

**Você segura a chave. Sempre.**

## Notas sobre o silêncio (atualizadas)

No modo Local, o daemon não fala com ninguém. Tudo acontece dentro da caixa onde você o colocou.

No modo Nuvem, suas requisições vão direto do seu PC pro Hugging Face. Nenhum intermediário. Nenhum registro nosso. Nenhum backend próprio.

Em ambos os modos, o arquivo `log.txt` guarda as pegadas. Leia-o antes de perguntar.

---

## Changelog

### v2.0.0-alpha — Sovereign Cloud *(atual)*

> "O daemon aprendeu a olhar pela janela. Mas a porta ainda é sua."

#### Adicionado

- **Modo dual de operação** — alterne entre Local (GGUF) e Nuvem (Hugging Face) com um clique na barra lateral
- **Integração Hugging Face Inference API** — 6 modelos gratuitos disponíveis (Qwen3, Llama 3.3, DeepSeek, Mistral, Gemma, Phi-4)
- **Fallback automático** — se a nuvem falhar (internet, rate limit, HF fora), o daemon cai pro modo Local sem intervenção
- **Campo de token HF** com máscara de segurança (••••) na sidebar
- **Botão "Testar conexão"** — valida seu token HF antes de usar
- **Dropdown de modelos HF** — troque de modelo sem reiniciar
- **Checkbox de fallback** — ative/desative a queda automática pro Local
- **Tutorial integrado** — botão "Tutorial HF" abre guia completo dentro do app
- **Barra de status expandida** — mostra modo ativo (Nuvem · HF / Local · GGUF), modelo, tokens, velocidade
- **Indicador de origem nas respostas** — cada resposta mostra se veio de `nuvem`, `local` ou `local-fallback`
- **Imports opcionais** — `llama-cpp-python` e `huggingface_hub` não quebram o app se ausentes
- **Suporte a ícone personalizado** — `assets/icon.ico` substitui o ícone genérico do Tkinter
- **Validação específica de erros HF** — mensagens claras pra 401 (token inválido), 404 (modelo não encontrado), 429 (rate limit)
- **Badge de versão** no README
- **Seção comparativa** Local vs Nuvem no README
- **Roadmap público** dos próximos ciclos

#### Modificado

- **Nome interno do app** — de `Tutor Python Local` para `hermeneutic-loop-daemon`
- **Tagline** — de "Assistente 100% local" para "Sua IA. Suas regras. Seu modo."
- **Configuração expandida** — novos campos: `modo_operacao`, `token_hf`, `modelo_hf`, `fallback_local`
- **Sidebar reorganizada** — nova seção "MODO DE OPERAÇÃO" no topo, acima de Perfil
- **Boas-vindas atualizadas** — mostram modo ativo ao iniciar
- **Largura da sidebar** — de 280px para 300px (acomoda novos controles)
- **Paleta de badges** — de verde (`#2ecc71`) para vermelho sangue (`#a01010`), alinhando com identidade visual

#### Mantido

- 100% compatível com configurações do v1 (campos antigos continuam funcionando)
- 4 perfis de assistente (Tutor Didático, Code Review, Debug Assist, Livre)
- 5 paletas cromáticas (Verde Matrix, Azul Ocean, Roxo Cyber, Laranja Sunset, Vermelho Dark)
- 8 snippets rápidos
- Streaming token-a-token com interrupção voluntária
- Exportação em TXT, MD, JSON
- Atalhos de teclado (Ctrl+N, Ctrl+S, Ctrl+L, Esc, Ctrl+Enter)
- Sistema de log com memória e arquivo
- Persistência automática de configuração

#### Filosofia

- **v1 dizia:** "Nenhum dado sai da sala."
- **v2 diz:** "Você decide onde a conversa acontece. E você segura a chave."

Ambos válidos. Ambos suportados. Soberania é escolha, não imposição.

---

### v1.0.1 — Genesis

> "Uma máquina que ainda lembra como ensinar."

#### Adicionado

- Interface gráfica moderna com `customtkinter` (tema escuro)
- Integração com `llama-cpp-python` pra rodar modelos GGUF localmente
- Suporte a GPU NVIDIA via CUDA (camadas offload automáticas)
- 4 perfis de assistente com system prompts especializados
- 5 paletas cromáticas completas (cores de fundo, texto, borda, primária)
- Streaming de resposta token-a-token com callback em tempo real
- Botão "Parar" pra interromper geração a qualquer momento
- Controle de parâmetros via sliders (temperatura, max tokens, top-p)
- 8 snippets rápidos de prompts comuns
- Exportação de conversa em 3 formatos (TXT, MD, JSON)
- Barra de status com métricas em tempo real (tokens, velocidade tok/s)
- Janela de log integrada com memória e arquivo persistente
- Atalhos de teclado completos (Ctrl+N, Ctrl+S, Ctrl+L, Esc, Ctrl+Enter)
- Persistência automática de configurações em `config.json`
- Sistema de log com níveis (INFO, AVISO, ERRO) e timestamp
- Tela de boas-vindas com atalhos e status do modelo
- Detecção automática de erros de carregamento com mensagem clara

#### Arquitetura

- `WrapperModelo` — abstração pra inferência GGUF via llama-cpp
- `GerenciadorConversa` — histórico com system prompt mutável
- `GerenciadorLog` — memória circular + arquivo append-only
- `Configuracao` — dataclass com serialização JSON
- `PainelLateral` — scrollable frame com seções colapsáveis
- `BarraStatus` — frame inferior com métricas em tempo real
- `JanelaLog` — toplevel independente com textbox read-only
- `Aplicacao` — classe principal herdando de `ctk.CTk`

#### Filosofia

- 100% local, zero telemetria, zero cloud
- Privacidade como premissa, não feature
- Ensino paciente sobre resposta rápida
- Código aberto MIT, auditável, modificável

---

### v1.0.0 — Primeiro Ciclo

- Commit inicial do daemon
- Estrutura básica do projeto
- Licença MIT
- README inaugural

---

## Próximos ciclos

### v2.1.0 — Multi-Provider
- Anthropic (Claude)
- OpenAI (GPT-4o)
- DeepSeek direto
- Google Gemini
- Dropdown unificado de provedores

### v2.2.0 — Smart Routing
- Tentativa automática entre modos baseada em latência
- Cache de respostas repetidas
- Histórico unificado (local + nuvem no mesmo lugar)

### v2.3.0 — Self-Hosted Backend
- Script pra rodar teu próprio backend proxy
- Docker compose pronto
- Documentação de deploy em Render/Railway/Fly.io

---

## Problemas conhecidos e seus antídotos

**`huggingface_hub` não encontrado**
```bash
pip install huggingface_hub
```

**Token HF inválido**
Verifique se começa com `hf_` e foi copiado completo. Gere um novo em [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

**Modelo HF não encontrado**
Escolha outro no dropdown. `Qwen/Qwen3-8B` é o mais confiável no tier grátis.

**429 Too Many Requests (HF)**
Limite grátis atingido. Aguarde algumas horas, ou ative o fallback pra Local, ou alterne pro modo Local permanentemente.

**`nmake not found` ao instalar `llama-cpp-python`**
Use a roda pré-forjada (passo 2, alternativa). Ou simplesmente não instale — o modo Nuvem não precisa.

**Caminho longo demais no Windows**
Ative o suporte a caminhos longos no registro:

```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

**O daemon local pensa devagar**
Verifique no `log.txt` se a linha `GPU=True` aparece. Se aparecer `GPU=False`, reinstale `llama-cpp-python` com suporte CUDA.

**A janela não abre**
Confirme que o Python é 3.10 ou superior e que as dependências estão instaladas.

---

## Licença

Este projeto está licenciado sob a **MIT License**.

```
MIT License

Copyright (c) 2026 HermeX · sousahi collective · by ByteHub

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Veja o arquivo [LICENSE](LICENSE) para o texto completo.

---

<p align="center">
  <sub>O daemon aprendeu a olhar pela janela. Mas a porta ainda é sua.</sub>
</p>

<p align="center">
  <sub>hermeneutic-loop-daemon · v2.0.0-alpha · MIT · HermeX · by ByteHub</sub>
</p>
