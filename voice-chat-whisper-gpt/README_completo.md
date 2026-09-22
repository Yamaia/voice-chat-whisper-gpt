# 🎙️ Voice Chat — Whisper + ChatGPT + gTTS

> Um assistente de conversação por voz, multi-idiomas, que une **Speech-to-Text** (Whisper), **geração de linguagem natural** (ChatGPT) e **Text-to-Speech** (gTTS) em uma experiência de conversa fluida via terminal.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![OpenAI](https://img.shields.io/badge/OpenAI-Whisper%20%2B%20ChatGPT-412991?logo=openai)
![gTTS](https://img.shields.io/badge/TTS-gTTS-4285F4?logo=google)
![Status](https://img.shields.io/badge/status-concluído-brightgreen)

---

## 📑 Sumário

- [Sobre o projeto](#-sobre-o-projeto)
- [Demonstração](#-demonstração)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Tecnologias utilizadas](#-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Como usar](#-como-usar)
- [Opções de linha de comando](#-opções-de-linha-de-comando)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Melhorias em relação ao laboratório original](#-melhorias-em-relação-ao-laboratório-original)
- [Possíveis evoluções](#-possíveis-evoluções)
- [Créditos](#-créditos)
- [Licença](#-licença)

---

## 📌 Sobre o projeto

Este projeto foi desenvolvido como desafio de portfólio da **[DIO](https://www.dio.me/)**, a partir do laboratório *"Conversando Por Voz Com o ChatGPT Utilizando Whisper (OpenAI) e Python"*. A proposta original combina três tecnologias da OpenAI e do Google para permitir que o usuário converse por voz com o ChatGPT em diferentes idiomas:

1. O usuário fala uma pergunta ou mensagem;
2. O **Whisper** (API da OpenAI) transcreve o áudio em texto;
3. O texto é enviado ao **ChatGPT**, que gera uma resposta;
4. O **gTTS** converte a resposta em áudio, que é reproduzido de volta ao usuário.

Nesta versão, o projeto foi reorganizado como um **script Python robusto para uso local via terminal**, com uma interface de linha de comando (CLI) melhorada em relação ao laboratório original.

---

## 🎬 Demonstração

```
============================================================
=============== Chat por voz — Whisper + ChatGPT + gTTS ===============
============================================================
Modelo de chat : gpt-4o-mini
Idioma (dica)  : detecção automática
Duração grav.  : 5s
Áudio de saída : ativado

----------------------------------------
1) 🎙️  Falar
2) ⌨️  Digitar mensagem
3) 🚪 Sair
----------------------------------------
Escolha uma opção [1-3]: 1
🎙️  Gravando por 5s... fale agora.
✅ Gravação concluída.
🗣️  Você disse: Qual a capital do Japão?
🤖 Assistente: A capital do Japão é Tóquio.
```

---

## ✨ Funcionalidades

- 🎙️ **Entrada por voz** — grava áudio do microfone e transcreve com Whisper.
- ⌨️ **Entrada por texto** — alternativa para quando não é possível ou desejável usar voz.
- 🌍 **Multi-idiomas** — funciona em qualquer idioma suportado pelo Whisper e pelo gTTS.
- 🔊 **Resposta em áudio** — a resposta do ChatGPT é convertida em fala automaticamente.
- 🧠 **Memória de conversa** — mantém o histórico da sessão para respostas com contexto.
- 📝 **Log automático** — salva a conversa completa em um arquivo `.txt` ao encerrar.
- 🛡️ **Tratamento de erros** — mensagens claras para chave de API ausente, falha de microfone, dependência faltando ou falha nas chamadas de API, sem derrubar o programa.
- ⚙️ **Totalmente configurável via CLI** — modelo, idioma, duração da gravação e modo texto-apenas.

---

## 🏗️ Arquitetura

```
┌─────────────┐     áudio (.wav)     ┌──────────────┐     texto     ┌─────────────┐
│  Microfone   │ ───────────────────▶ │ Whisper API  │ ─────────────▶ │  ChatGPT    │
│ (sounddevice)│                      │   (OpenAI)   │                │   (OpenAI)  │
└─────────────┘                      └──────────────┘                └──────┬──────┘
                                                                              │ texto
                                                                              ▼
┌─────────────┐     áudio (.mp3)     ┌──────────────┐
│  Alto-falante│ ◀─────────────────── │     gTTS      │
│ (playsound)  │                      │ (Google TTS) │
└─────────────┘                      └──────────────┘
```

---

## 🛠️ Tecnologias utilizadas

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.10+ |
| Speech-to-Text | [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text) |
| Geração de resposta | [OpenAI Chat Completions API](https://platform.openai.com/docs/guides/text-generation) |
| Text-to-Speech | [gTTS](https://gtts.readthedocs.io/) |
| Captura de áudio | [sounddevice](https://python-sounddevice.readthedocs.io/) + [scipy](https://scipy.org/) |
| Reprodução de áudio | [playsound](https://pypi.org/project/playsound/) |

---

## ✅ Pré-requisitos

- Python 3.10 ou superior
- Uma [chave de API da OpenAI](https://platform.openai.com/api-keys) com créditos disponíveis
- Microfone funcional (para o modo de entrada por voz)

---

## 📦 Instalação

```bash
# Clone o repositório
git clone https://github.com/<seu-usuario>/<nome-do-repo>.git
cd <nome-do-repo>

# (Opcional, mas recomendado) crie um ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

# Instale as dependências
pip install -r requirements.txt
```

---

## 🔑 Configuração

Defina sua chave da OpenAI como variável de ambiente:

```bash
# Linux/macOS
export OPENAI_API_KEY="sua-chave-aqui"

# Windows (cmd)
set OPENAI_API_KEY=sua-chave-aqui

# Windows (PowerShell)
$env:OPENAI_API_KEY="sua-chave-aqui"
```

---

## ▶️ Como usar

```bash
python voice_chat_whisper_gpt.py
```

Um menu interativo será exibido:

```
1) 🎙️  Falar
2) ⌨️  Digitar mensagem
3) 🚪 Sair
```

Ao encerrar a conversa (opção 3 ou `Ctrl+C`), um arquivo `conversa_AAAAMMDD_HHMMSS.txt` é salvo automaticamente no diretório atual com todo o histórico da sessão.

---

## ⚙️ Opções de linha de comando

| Flag | Descrição | Padrão |
|---|---|---|
| `--model` | Modelo de chat da OpenAI a ser usado | `gpt-4o-mini` |
| `--lang` | Código do idioma (ex.: `pt`, `en`, `es`) usado como dica para o Whisper e idioma da fala no gTTS | detecção automática / `pt` |
| `--duration` | Duração em segundos de cada gravação de voz | `5` |
| `--no-audio-output` | Desativa a geração/reprodução de áudio da resposta (apenas texto) | desativado |

Exemplos:

```bash
python voice_chat_whisper_gpt.py --lang en --duration 6
python voice_chat_whisper_gpt.py --model gpt-4o-mini --no-audio-output
```

---

## 📁 Estrutura do projeto

```
.
├── voice_chat_whisper_gpt.py   # Script principal
├── requirements.txt            # Dependências do projeto
└── README.md                   # Este arquivo
```

---

## 🚀 Melhorias em relação ao laboratório original

O laboratório de referência da DIO roda em um notebook (Google Colab) com fluxo de gravação fixo. Nesta versão:

- Foi criada uma **CLI interativa** com menu (falar / digitar / sair), em vez de um fluxo único de voz obrigatória.
- Foram adicionados **tratamentos de erro** para os principais pontos de falha: chave de API ausente, dependências não instaladas, microfone indisponível e falhas nas chamadas às APIs.
- O **histórico de conversa** passou a ser mantido durante toda a sessão, permitindo respostas com contexto (multi-turno).
- A conversa é **salva automaticamente em log** ao final da sessão.
- Parâmetros como modelo, idioma, duração da gravação e modo texto-apenas ficaram **configuráveis via linha de comando**.

---

## 🔮 Possíveis evoluções

- [ ] Interface gráfica (ex.: com `customtkinter` ou `streamlit`)
- [ ] Suporte a gravação por push-to-talk (iniciar/parar com tecla) em vez de duração fixa
- [ ] Seleção de voz/sotaque no gTTS
- [ ] Histórico persistente entre sessões (não apenas por execução)
- [ ] Empacotamento como executável standalone

---

## 👤 Créditos

Projeto baseado no laboratório da [DIO](https://www.dio.me/) — *"Conversando Por Voz Com o ChatGPT Utilizando Whisper (OpenAI) e Python"*, desenvolvido e adaptado por **Yamaia** como parte do portfólio de projetos.

---

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar, estudar e adaptar.
