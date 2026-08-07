"""
================================================================================
  ASSISTENTE DE PROGRAMACAO LOCAL - TUTOR PYTHON
  Versao: 1.0.1
================================================================================
"""

import os
import sys
import json
import time
import threading
from tkinter import filedialog, messagebox
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional

try:
    import customtkinter as ctk
except ImportError:
    print("[ERRO FATAL] customtkinter nao encontrado.")
    sys.exit(1)

try:
    from llama_cpp import Llama
except ImportError:
    print("[ERRO FATAL] llama-cpp-python nao encontrado.")
    sys.exit(1)


APP_NAME = "Tutor Python Local"
APP_VERSION = "1.0.1"
DEFAULT_WINDOW_SIZE = "1280x780"
MIN_WINDOW_SIZE = (900, 600)

CAMINHO_MODELO_PADRAO = "modelo.gguf"
CONTEXTO_PADRAO = 4096
MAX_TOKENS_PADRAO = 1024
TEMPERATURA_PADRAO = 0.7
TOP_P_PADRAO = 0.9
USE_GPU_PADRAO = True

ARQUIVO_CONFIG = "config.json"
ARQUIVO_LOG = "log.txt"
PASTA_EXPORT = "exportacoes"

SEPARADOR_VISUAL = "-" * 60
SEPARADOR_CHAT = "_" * 55


PERFIS = {
    "Tutor Didatico": (
        "Voce e um tutor de Python experiente, paciente e didatico. "
        "Sempre responda em portugues do Brasil. Explique conceitos de forma "
        "clara, use analogias do dia a dia quando possivel, e forneca exemplos "
        "de codigo curtos e bem comentados. Priorize o aprendizado do aluno, "
        "nao apenas entregar a resposta pronta."
    ),
    "Code Review": (
        "Voce e um revisor de codigo senior especializado em Python. "
        "Analise o codigo apontando problemas de logica, violacoes de PEP 8, "
        "oportunidades de otimizacao e riscos de seguranca. Seja direto e "
        "tecnico. Responda em portugues do Brasil."
    ),
    "Debug Assist": (
        "Voce e um especialista em depuracao de Python. Identifique a causa "
        "do erro, explique por que acontece, sugira a correcao com exemplo "
        "e indique como evitar no futuro. Responda em portugues do Brasil."
    ),
    "Livre": (
        "Voce e um assistente geral inteligente. Responda em portugues do "
        "Brasil de forma clara e util, com conhecimento especial em Python."
    ),
}


SNIPPETS = {
    "Explicar conceito": "Me explique o conceito de {topico} em Python com exemplos.",
    "Revisar codigo": "Revise este codigo Python e aponte melhorias:\n\n{codigo}",
    "Encontrar bug": "Este codigo esta dando erro. Me ajude:\n\n{codigo}\n\nErro: {erro}",
    "Gerar exemplo": "Gere um exemplo pratico de {topico} em Python.",
    "Comparar abordagens": "Compare: {abordagem1} vs {abordagem2} em Python.",
    "Otimizar codigo": "Otimize este codigo Python:\n\n{codigo}",
    "Escrever teste": "Escreva testes pytest para:\n\n{codigo}",
    "Documentar": "Escreva docstrings para:\n\n{codigo}",
}


PALETAS = {
    "Verde Matrix": {
        "primaria": "#2ecc71", "primaria_hover": "#27ae60",
        "fundo_app": "#0f0f1e", "fundo_chat": "#1a1a2e", "fundo_painel": "#16213e",
        "texto": "#eaeaea", "texto_suave": "#a0a0b0", "borda": "#2a2a4e",
    },
    "Azul Ocean": {
        "primaria": "#3498db", "primaria_hover": "#2980b9",
        "fundo_app": "#0a1929", "fundo_chat": "#132f4c", "fundo_painel": "#0d2137",
        "texto": "#e7ebf0", "texto_suave": "#8ba4c7", "borda": "#1e4976",
    },
    "Roxo Cyber": {
        "primaria": "#9b59b6", "primaria_hover": "#8e44ad",
        "fundo_app": "#1a0f2e", "fundo_chat": "#2d1b4e", "fundo_painel": "#241445",
        "texto": "#ece5f5", "texto_suave": "#b0a0c7", "borda": "#4a2d7a",
    },
    "Laranja Sunset": {
        "primaria": "#e67e22", "primaria_hover": "#d35400",
        "fundo_app": "#1f1410", "fundo_chat": "#2e1f17", "fundo_painel": "#261812",
        "texto": "#f5e8dc", "texto_suave": "#c7a88a", "borda": "#5a3a25",
    },
    "Vermelho Dark": {
        "primaria": "#e74c3c", "primaria_hover": "#c0392b",
        "fundo_app": "#1a0f0f", "fundo_chat": "#2e1717", "fundo_painel": "#261212",
        "texto": "#f5dcdc", "texto_suave": "#c78a8a", "borda": "#5a2525",
    },
}


@dataclass
class Configuracao:
    caminho_modelo: str = CAMINHO_MODELO_PADRAO
    usar_gpu: bool = USE_GPU_PADRAO
    n_ctx: int = CONTEXTO_PADRAO
    max_tokens: int = MAX_TOKENS_PADRAO
    temperatura: float = TEMPERATURA_PADRAO
    top_p: float = TOP_P_PADRAO
    perfil_ativo: str = "Tutor Didatico"
    paleta_ativa: str = "Verde Matrix"
    modo_aparencia: str = "dark"
    tamanho_fonte_chat: int = 14
    tamanho_fonte_ui: int = 13

    def salvar(self, caminho: str = ARQUIVO_CONFIG) -> None:
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(asdict(self), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[AVISO] Falha ao salvar config: {e}")

    @classmethod
    def carregar(cls, caminho: str = ARQUIVO_CONFIG) -> "Configuracao":
        if not os.path.exists(caminho):
            return cls()
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
            return cls(**{k: v for k, v in dados.items() if k in cls.__dataclass_fields__})
        except Exception as e:
            print(f"[AVISO] Config invalida, usando padrao: {e}")
            return cls()


class GerenciadorLog:
    def __init__(self, caminho: str = ARQUIVO_LOG, max_memoria: int = 200):
        self.caminho = caminho
        self.max_memoria = max_memoria
        self.memoria: list[str] = []

    def registrar(self, nivel: str, mensagem: str) -> None:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linha = f"[{ts}] [{nivel.upper()}] {mensagem}"
        self.memoria.append(linha)
        if len(self.memoria) > self.max_memoria:
            self.memoria = self.memoria[-self.max_memoria:]
        try:
            with open(self.caminho, "a", encoding="utf-8") as f:
                f.write(linha + "\n")
        except Exception:
            pass

    def info(self, m): self.registrar("INFO", m)
    def erro(self, m): self.registrar("ERRO", m)
    def aviso(self, m): self.registrar("AVISO", m)


class WrapperModelo:
    def __init__(self, config: Configuracao, log: GerenciadorLog):
        self.config = config
        self.log = log
        self.llm: Optional[Llama] = None
        self.carregado = False
        self.ultimo_erro: Optional[str] = None

    def carregar(self) -> bool:
        if not os.path.exists(self.config.caminho_modelo):
            self.ultimo_erro = f"Arquivo nao encontrado: {self.config.caminho_modelo}"
            self.log.erro(self.ultimo_erro)
            return False
        try:
            self.log.info(f"Carregando: {self.config.caminho_modelo}")
            t0 = time.time()
            n_gpu = -1 if self.config.usar_gpu else 0
            self.llm = Llama(model_path=self.config.caminho_modelo,
                             n_gpu_layers=n_gpu, n_ctx=self.config.n_ctx, verbose=False)
            self.carregado = True
            self.log.info(f"Carregado em {time.time()-t0:.2f}s")
            return True
        except Exception as e:
            self.ultimo_erro = str(e)
            self.log.erro(f"Falha: {e}")
            return False

    def gerar_stream(self, mensagens, callback_token, parar_evento):
        if not self.carregado:
            raise RuntimeError("Modelo nao carregado.")
        stats = {"tokens_gerados": 0, "tempo_total": 0.0,
                 "tokens_por_segundo": 0.0, "resposta_completa": ""}
        t0 = time.time()
        try:
            stream = self.llm.create_chat_completion(
                messages=mensagens, stream=True,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperatura,
                top_p=self.config.top_p,
            )
            for chunk in stream:
                if parar_evento.is_set():
                    break
                delta = chunk["choices"][0]["delta"].get("content", "")
                if delta:
                    stats["resposta_completa"] += delta
                    stats["tokens_gerados"] += 1
                    callback_token(delta)
            stats["tempo_total"] = time.time() - t0
            if stats["tempo_total"] > 0:
                stats["tokens_por_segundo"] = stats["tokens_gerados"] / stats["tempo_total"]
        except Exception as e:
            self.log.erro(f"Geracao: {e}")
            raise
        return stats


class GerenciadorConversa:
    def __init__(self, system_prompt: str, log: GerenciadorLog):
        self.log = log
        self.mensagens: list[dict] = [{"role": "system", "content": system_prompt}]

    @property
    def system_prompt(self): return self.mensagens[0]["content"]

    @system_prompt.setter
    def system_prompt(self, v): self.mensagens[0]["content"] = v

    def add_user(self, t): self.mensagens.append({"role": "user", "content": t})
    def add_assistant(self, t): self.mensagens.append({"role": "assistant", "content": t})
    def para_modelo(self): return list(self.mensagens)

    def limpar(self):
        self.mensagens = [self.mensagens[0]]
        self.log.info("Historico limpo.")

    def total(self): return len(self.mensagens) - 1

    def exportar_txt(self, c):
        try:
            with open(c, "w", encoding="utf-8") as f:
                f.write(f"Exportado em {datetime.now()}\n{SEPARADOR_VISUAL}\n\n")
                for m in self.mensagens[1:]:
                    r = "USUARIO" if m["role"] == "user" else "ASSISTENTE"
                    f.write(f"[{r}]\n{m['content']}\n\n")
            return True
        except Exception as e:
            self.log.erro(f"TXT: {e}"); return False

    def exportar_md(self, c):
        try:
            with open(c, "w", encoding="utf-8") as f:
                f.write(f"# Conversa - {datetime.now()}\n\n")
                for m in self.mensagens[1:]:
                    t = "Usuario" if m["role"] == "user" else "Assistente"
                    f.write(f"## {t}\n\n{m['content']}\n\n---\n\n")
            return True
        except Exception as e:
            self.log.erro(f"MD: {e}"); return False

    def exportar_json(self, c):
        try:
            with open(c, "w", encoding="utf-8") as f:
                json.dump({"exportado_em": datetime.now().isoformat(),
                           "mensagens": self.mensagens}, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            self.log.erro(f"JSON: {e}"); return False


class BarraStatus(ctk.CTkFrame):
    def __init__(self, master, paleta, **kw):
        super().__init__(master, fg_color=paleta["fundo_painel"], height=32, **kw)
        self.paleta = paleta
        self.lbl_modelo = ctk.CTkLabel(self, text="Modelo: -",
                                       text_color=paleta["texto_suave"], font=("Segoe UI", 11))
        self.lbl_modelo.pack(side="left", padx=12)
        self.lbl_tok = ctk.CTkLabel(self, text="Tokens: 0",
                                    text_color=paleta["texto_suave"], font=("Segoe UI", 11))
        self.lbl_tok.pack(side="left", padx=12)
        self.lbl_vel = ctk.CTkLabel(self, text="Velocidade: -",
                                    text_color=paleta["texto_suave"], font=("Segoe UI", 11))
        self.lbl_vel.pack(side="left", padx=12)
        self.lbl_st = ctk.CTkLabel(self, text="Pronto",
                                   text_color=paleta["primaria"], font=("Segoe UI", 11, "bold"))
        self.lbl_st.pack(side="right", padx=12)

    def set_modelo(self, n): self.lbl_modelo.configure(text=f"Modelo: {n}")
    def set_stats(self, t, v):
        self.lbl_tok.configure(text=f"Tokens: {t}")
        self.lbl_vel.configure(text=f"Velocidade: {v:.1f} tok/s")
    def set_status(self, t, cor=None):
        self.lbl_st.configure(text=t, text_color=cor or self.paleta["primaria"])


class PainelLateral(ctk.CTkScrollableFrame):
    def __init__(self, master, paleta, callbacks, **kw):
        super().__init__(master, fg_color=paleta["fundo_painel"], width=280, **kw)
        self.paleta = paleta
        self.cb = callbacks

        self._secao("PERFIL DO ASSISTENTE")
        self.var_perfil = ctk.StringVar(value="Tutor Didatico")
        ctk.CTkOptionMenu(self, values=list(PERFIS.keys()), variable=self.var_perfil,
                          command=lambda v: self.cb.get("on_perfil", lambda x: None)(v),
                          fg_color=paleta["fundo_chat"], button_color=paleta["primaria"],
                          button_hover_color=paleta["primaria_hover"],
                          text_color=paleta["texto"], font=("Segoe UI", 12)
                          ).pack(fill="x", padx=10, pady=(0, 12))

        self._secao("PARAMETROS DO MODELO")

        self._rotulo("Temperatura (criatividade)")
        self.var_temp = ctk.DoubleVar(value=TEMPERATURA_PADRAO)
        ctk.CTkSlider(self, from_=0.0, to=2.0, number_of_steps=40, variable=self.var_temp,
                      progress_color=paleta["primaria"], button_color=paleta["primaria"],
                      button_hover_color=paleta["primaria_hover"],
                      command=self._sync_params).pack(fill="x", padx=10)
        self.lbl_temp = ctk.CTkLabel(self, text=f"{TEMPERATURA_PADRAO:.2f}",
                                     text_color=paleta["texto_suave"], font=("Segoe UI", 11))
        self.lbl_temp.pack(pady=(0, 8))

        self._rotulo("Max Tokens")
        self.var_maxtok = ctk.IntVar(value=MAX_TOKENS_PADRAO)
        ctk.CTkSlider(self, from_=128, to=4096, number_of_steps=62, variable=self.var_maxtok,
                      progress_color=paleta["primaria"], button_color=paleta["primaria"],
                      button_hover_color=paleta["primaria_hover"],
                      command=self._sync_params).pack(fill="x", padx=10)
        self.lbl_maxtok = ctk.CTkLabel(self, text=str(MAX_TOKENS_PADRAO),
                                       text_color=paleta["texto_suave"], font=("Segoe UI", 11))
        self.lbl_maxtok.pack(pady=(0, 8))

        self._rotulo("Top-P")
        self.var_topp = ctk.DoubleVar(value=TOP_P_PADRAO)
        ctk.CTkSlider(self, from_=0.1, to=1.0, number_of_steps=18, variable=self.var_topp,
                      progress_color=paleta["primaria"], button_color=paleta["primaria"],
                      button_hover_color=paleta["primaria_hover"],
                      command=self._sync_params).pack(fill="x", padx=10)
        self.lbl_topp = ctk.CTkLabel(self, text=f"{TOP_P_PADRAO:.2f}",
                                     text_color=paleta["texto_suave"], font=("Segoe UI", 11))
        self.lbl_topp.pack(pady=(0, 12))

        self._secao("APARENCIA")
        self._rotulo("Paleta de cores")
        self.var_paleta = ctk.StringVar(value="Verde Matrix")
        ctk.CTkOptionMenu(self, values=list(PALETAS.keys()), variable=self.var_paleta,
                          command=lambda v: self.cb.get("on_paleta", lambda x: None)(v),
                          fg_color=paleta["fundo_chat"], button_color=paleta["primaria"],
                          button_hover_color=paleta["primaria_hover"],
                          text_color=paleta["texto"], font=("Segoe UI", 12)
                          ).pack(fill="x", padx=10, pady=(0, 8))

        self._rotulo("Modo")
        self.var_modo = ctk.StringVar(value="dark")
        ctk.CTkOptionMenu(self, values=["dark", "light", "system"], variable=self.var_modo,
                          command=lambda v: self.cb.get("on_modo", lambda x: None)(v),
                          fg_color=paleta["fundo_chat"], button_color=paleta["primaria"],
                          button_hover_color=paleta["primaria_hover"],
                          text_color=paleta["texto"], font=("Segoe UI", 12)
                          ).pack(fill="x", padx=10, pady=(0, 12))

        self._secao("SNIPPETS RAPIDOS")
        for nome in SNIPPETS.keys():
            ctk.CTkButton(self, text=nome, height=30, fg_color=paleta["fundo_chat"],
                          hover_color=paleta["borda"], text_color=paleta["texto"],
                          font=("Segoe UI", 11),
                          command=lambda n=nome: self.cb.get("on_snippet", lambda x: None)(SNIPPETS[n])
                          ).pack(fill="x", padx=10, pady=2)

        self._secao("ACOES")
        ctk.CTkButton(self, text="Nova Conversa", height=34, fg_color=paleta["primaria"],
                      hover_color=paleta["primaria_hover"],
                      command=lambda: self.cb.get("on_nova", lambda: None)(),
                      font=("Segoe UI", 12, "bold")).pack(fill="x", padx=10, pady=(0, 6))
        ctk.CTkButton(self, text="Exportar Conversa", height=34, fg_color=paleta["fundo_chat"],
                      hover_color=paleta["borda"],
                      command=lambda: self.cb.get("on_exportar", lambda: None)(),
                      font=("Segoe UI", 12)).pack(fill="x", padx=10, pady=(0, 6))
        ctk.CTkButton(self, text="Ver Log", height=34, fg_color=paleta["fundo_chat"],
                      hover_color=paleta["borda"],
                      command=lambda: self.cb.get("on_log", lambda: None)(),
                      font=("Segoe UI", 12)).pack(fill="x", padx=10, pady=(0, 6))

    def _secao(self, t):
        ctk.CTkLabel(self, text=t, text_color=self.paleta["primaria"],
                     font=("Segoe UI", 11, "bold"), anchor="w"
                     ).pack(fill="x", padx=10, pady=(12, 4))

    def _rotulo(self, t):
        ctk.CTkLabel(self, text=t, text_color=self.paleta["texto_suave"],
                     font=("Segoe UI", 11), anchor="w"
                     ).pack(fill="x", padx=10, pady=(4, 2))

    def _sync_params(self, _=None):
        self.lbl_temp.configure(text=f"{self.var_temp.get():.2f}")
        self.lbl_maxtok.configure(text=str(int(self.var_maxtok.get())))
        self.lbl_topp.configure(text=f"{self.var_topp.get():.2f}")
        cb = self.cb.get("on_param")
        if cb:
            cb(self.var_temp.get(), int(self.var_maxtok.get()), self.var_topp.get())

    def obter_parametros(self):
        return self.var_temp.get(), int(self.var_maxtok.get()), self.var_topp.get()


class JanelaLog(ctk.CTkToplevel):
    def __init__(self, master, log, paleta):
        super().__init__(master)
        self.title("Log do Sistema")
        self.geometry("700x450")
        self.configure(fg_color=paleta["fundo_app"])
        self.log_ref = log
        ctk.CTkLabel(self, text="Log do Sistema", text_color=paleta["primaria"],
                     font=("Segoe UI", 16, "bold")).pack(pady=10)
        self.txt = ctk.CTkTextbox(self, fg_color=paleta["fundo_chat"],
                                  text_color=paleta["texto"], font=("Consolas", 11), wrap="word")
        self.txt.pack(fill="both", expand=True, padx=15, pady=10)
        self.atualizar()
        ctk.CTkButton(self, text="Atualizar", width=120, fg_color=paleta["primaria"],
                      hover_color=paleta["primaria_hover"], command=self.atualizar).pack(pady=(0, 12))

    def atualizar(self):
        self.txt.configure(state="normal")
        self.txt.delete("1.0", "end")
        for l in self.log_ref.memoria:
            self.txt.insert("end", l + "\n")
        self.txt.see("end")
        self.txt.configure(state="disabled")


class Aplicacao(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.config = Configuracao.carregar()
        self.log = GerenciadorLog()
        self.log.info(f"Iniciando {APP_NAME} v{APP_VERSION}")
        self.paleta = PALETAS[self.config.paleta_ativa]
        ctk.set_appearance_mode(self.config.modo_aparencia)
        ctk.set_default_color_theme("blue")

        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry(DEFAULT_WINDOW_SIZE)
        self.minsize(*MIN_WINDOW_SIZE)
        self.configure(fg_color=self.paleta["fundo_app"])

        self.modelo = WrapperModelo(self.config, self.log)
        self.conversa = GerenciadorConversa(PERFIS[self.config.perfil_ativo], self.log)
        self.parar_evento = threading.Event()
        self.gerando = False
        self.janela_log: Optional[JanelaLog] = None

        self._montar_ui()
        self._bind_atalhos()
        threading.Thread(target=self._load_thread, daemon=True).start()

    def _montar_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._ui_header()
        self._ui_corpo()
        self._ui_entrada()
        self.barra = BarraStatus(self, self.paleta)
        self.barra.grid(row=3, column=0, columnspan=2, sticky="ew")

    def _ui_header(self):
        cab = ctk.CTkFrame(self, fg_color=self.paleta["fundo_painel"], height=56)
        cab.grid(row=0, column=0, columnspan=2, sticky="ew")
        cab.grid_propagate(False)
        ctk.CTkLabel(cab, text=f"  {APP_NAME}", text_color=self.paleta["primaria"],
                     font=("Segoe UI", 18, "bold"), anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(cab, text=f"v{APP_VERSION}  |  Perfil: {self.config.perfil_ativo}",
                     text_color=self.paleta["texto_suave"],
                     font=("Segoe UI", 11)).pack(side="left", padx=10)
        self.lbl_st_modelo = ctk.CTkLabel(cab, text="Carregando modelo...",
                                          text_color="#f39c12", font=("Segoe UI", 11, "bold"))
        self.lbl_st_modelo.pack(side="right", padx=20)

    def _ui_corpo(self):
        self.chat = ctk.CTkTextbox(self, fg_color=self.paleta["fundo_chat"],
                                   text_color=self.paleta["texto"],
                                   font=("Consolas", self.config.tamanho_fonte_chat),
                                   wrap="word", border_width=1, border_color=self.paleta["borda"])
        self.chat.grid(row=1, column=0, sticky="nsew", padx=(15, 5), pady=10)
        self.chat.insert("0.0", self._boas_vindas())
        self.chat.configure(state="disabled")

        cbs = {"on_perfil": self._on_perfil, "on_param": self._on_param,
               "on_paleta": self._on_paleta, "on_modo": self._on_modo,
               "on_snippet": self._on_snippet, "on_nova": self._nova,
               "on_exportar": self._exportar, "on_log": self._abrir_log}
        self.painel = PainelLateral(self, self.paleta, cbs)
        self.painel.grid(row=1, column=1, sticky="nsew", padx=(5, 15), pady=10)

    def _ui_entrada(self):
        f = ctk.CTkFrame(self, fg_color=self.paleta["fundo_painel"], height=70)
        f.grid(row=2, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 8))
        f.grid_propagate(False)
        f.grid_columnconfigure(0, weight=1)
        self.entrada = ctk.CTkTextbox(f, fg_color=self.paleta["fundo_chat"],
                                      text_color=self.paleta["texto"],
                                      font=("Segoe UI", self.config.tamanho_fonte_ui),
                                      wrap="word", height=50, border_width=1,
                                      border_color=self.paleta["borda"])
        self.entrada.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.entrada.bind("<Return>", self._on_enter)
        self.btn_enviar = ctk.CTkButton(f, text="Enviar", width=110, height=40,
                                        fg_color=self.paleta["primaria"],
                                        hover_color=self.paleta["primaria_hover"],
                                        command=self._enviar, font=("Segoe UI", 12, "bold"))
        self.btn_enviar.grid(row=0, column=1, padx=(5, 10), pady=10)
        self.btn_parar = ctk.CTkButton(f, text="Parar", width=90, height=40,
                                       fg_color="#e74c3c", hover_color="#c0392b",
                                       command=self._parar, font=("Segoe UI", 12, "bold"),
                                       state="disabled")
        self.btn_parar.grid(row=0, column=2, padx=(0, 10), pady=10)

    def _bind_atalhos(self):
        self.bind("<Control-n>", lambda e: self._nova())
        self.bind("<Control-s>", lambda e: self._exportar())
        self.bind("<Control-l>", lambda e: self._abrir_log())
        self.bind("<Escape>", lambda e: self._parar() if self.gerando else None)

    def _boas_vindas(self):
        return (f"Bem-vindo ao {APP_NAME} v{APP_VERSION}\n{SEPARADOR_VISUAL}\n\n"
                "Assistente 100% local com seu modelo GGUF.\n"
                "Nenhum dado sai da sua maquina.\n\n"
                "ATALHOS:\n"
                "  Enter = nova linha | Ctrl+Enter = enviar\n"
                "  Ctrl+N = nova conversa | Ctrl+S = exportar | Ctrl+L = log\n"
                "  Esc = parar geracao\n\n"
                "Aguardando o modelo...\n\n")

    def _load_thread(self):
        ok = self.modelo.carregar()
        self.after(0, self._pos_load, ok)

    def _pos_load(self, ok):
        if ok:
            self.lbl_st_modelo.configure(text="Modelo pronto", text_color="#2ecc71")
            self.barra.set_modelo(Path(self.config.caminho_modelo).name)
            self.barra.set_status("Pronto")
            self._chat(f"\n[OK] Modelo carregado. Pode conversar.\n{SEPARADOR_CHAT}\n\n")
        else:
            self.lbl_st_modelo.configure(text="ERRO", text_color="#e74c3c")
            self.barra.set_status("Erro", "#e74c3c")
            self._chat(f"\n[ERRO] {self.modelo.ultimo_erro}\n{SEPARADOR_CHAT}\n\n")
            messagebox.showerror("Erro", f"Falha ao carregar:\n{self.modelo.ultimo_erro}")

    def _chat(self, t):
        self.chat.configure(state="normal")
        self.chat.insert("end", t)
        self.chat.see("end")
        self.chat.configure(state="disabled")

    def _on_enter(self, e):
        if e.state & 0x4:
            self._enviar()
            return "break"
        return "continue"

    def _enviar(self):
        if not self.modelo.carregado:
            messagebox.showwarning("Aviso", "Aguarde o modelo.")
            return
        if self.gerando:
            return
        t = self.entrada.get("1.0", "end").strip()
        if not t:
            return
        self.entrada.delete("1.0", "end")
        self._chat(f"[VOCE]\n{t}\n\n")
        self.conversa.add_user(t)
        self.gerando = True
        self.parar_evento.clear()
        self.btn_enviar.configure(state="disabled")
        self.btn_parar.configure(state="normal")
        self.barra.set_status("Gerando...", "#f39c12")
        temp, mt, tp = self.painel.obter_parametros()
        self.config.temperatura, self.config.max_tokens, self.config.top_p = temp, mt, tp
        threading.Thread(target=self._gerar_thread, daemon=True).start()

    def _gerar_thread(self):
        try:
            self.after(0, self._chat, "[ASSISTENTE]\n")
            cb = lambda tok: self.after(0, self._chat, tok)
            st = self.modelo.gerar_stream(self.conversa.para_modelo(), cb, self.parar_evento)
            self.conversa.add_assistant(st["resposta_completa"])
            rodape = (f"\n\n{SEPARADOR_CHAT}\n"
                      f"tokens={st['tokens_gerados']}  tempo={st['tempo_total']:.2f}s  "
                      f"vel={st['tokens_por_segundo']:.1f}tok/s\n\n")
            self.after(0, self._chat, rodape)
            self.after(0, self.barra.set_stats, st["tokens_gerados"], st["tokens_por_segundo"])
        except Exception as e:
            self.after(0, self._chat, f"\n[ERRO] {e}\n\n")
        finally:
            self.after(0, self._fim_gerar)

    def _fim_gerar(self):
        self.gerando = False
        self.btn_enviar.configure(state="normal")
        self.btn_parar.configure(state="disabled")
        self.barra.set_status("Pronto")
        self.config.salvar()

    def _parar(self):
        if self.gerando:
            self.parar_evento.set()

    def _on_perfil(self, v):
        self.config.perfil_ativo = v
        self.conversa.system_prompt = PERFIS[v]
        messagebox.showinfo("Perfil", f"Ativo: {v}\n\nRecomenda-se nova conversa.")

    def _on_param(self, t, m, p):
        self.config.temperatura, self.config.max_tokens, self.config.top_p = t, m, p

    def _on_paleta(self, v):
        self.config.paleta_ativa = v
        self.config.salvar()
        messagebox.showinfo("Paleta", f"'{v}' salva. Reinicie para aplicar.")

    def _on_modo(self, v):
        ctk.set_appearance_mode(v)
        self.config.modo_aparencia = v
        self.config.salvar()

    def _on_snippet(self, tpl):
        self.entrada.delete("1.0", "end")
        self.entrada.insert("1.0", tpl)
        self.entrada.focus()

    def _nova(self):
        if self.gerando:
            if not messagebox.askyesno("Confirmar", "Parar e limpar?"):
                return
            self.parar_evento.set()
        if self.conversa.total() > 0:
            if not messagebox.askyesno("Confirmar", "Limpar historico?"):
                return
        self.conversa.limpar()
        self.chat.configure(state="normal")
        self.chat.delete("1.0", "end")
        self.chat.insert("0.0", self._boas_vindas() + "\n[OK] Nova conversa.\n\n")
        self.chat.configure(state="disabled")

    def _exportar(self):
        os.makedirs(PASTA_EXPORT, exist_ok=True)
        op = [("Texto", "*.txt"), ("Markdown", "*.md"), ("JSON", "*.json")]
        c = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=op, initialdir=PASTA_EXPORT,
            initialfile=f"conversa_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        if not c:
            return
        if c.endswith(".md"):
            ok = self.conversa.exportar_md(c)
        elif c.endswith(".json"):
            ok = self.conversa.exportar_json(c)
        else:
            ok = self.conversa.exportar_txt(c)
        if ok:
            messagebox.showinfo("OK", f"Salvo em:\n{c}")

    def _abrir_log(self):
        if self.janela_log is None or not self.janela_log.winfo_exists():
            self.janela_log = JanelaLog(self, self.log, self.paleta)
        else:
            self.janela_log.atualizar()
            self.janela_log.lift()

    def on_closing(self):
        if self.gerando:
            self.parar_evento.set()
        self.config.salvar()
        self.log.info("Encerrado.")
        self.destroy()


def main():
    print("=" * 60)
    print(f"  {APP_NAME} v{APP_VERSION}")
    print("=" * 60)
    print("Inicializando... aguarde o modelo (20-40s).")
    print("=" * 60)
    app = Aplicacao()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("\nEncerrado (Ctrl+C).")


if __name__ == "__main__":
    main()