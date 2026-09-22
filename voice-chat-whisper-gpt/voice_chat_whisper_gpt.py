#!/usr/bin/env python3
"""
voice_chat_whisper_gpt.py

Chat por voz multi-idiomas usando:
  - OpenAI Whisper API  -> Speech-to-Text (transcrição da fala)
  - OpenAI Chat API     -> geração da resposta (ChatGPT)
  - gTTS (Google TTS)   -> Text-to-Speech (fala da resposta)

Melhoria em relação ao laboratório original da DIO: interface de linha de
comando (CLI) mais robusta, com menu interativo, opção de digitar OU falar,
tratamento de erros (chave de API ausente, microfone indisponível,
dependências faltando), histórico de conversa mantido durante a sessão e
log salvo em arquivo .txt ao final.

Requisitos (ver requirements.txt):
    pip install openai gTTS sounddevice scipy playsound==1.2.2

Configuração:
    Defina sua chave da OpenAI como variável de ambiente antes de rodar:
        export OPENAI_API_KEY="sua-chave-aqui"      (Linux/macOS)
        set OPENAI_API_KEY=sua-chave-aqui            (Windows/cmd)

Uso:
    python voice_chat_whisper_gpt.py
    python voice_chat_whisper_gpt.py --lang en --duration 6
    python voice_chat_whisper_gpt.py --model gpt-4o-mini --no-audio-output
"""

import argparse
import datetime
import os
import sys
import tempfile

# ---------------------------------------------------------------------------
# Verificação de dependências com mensagens de erro amigáveis
# ---------------------------------------------------------------------------

def _falta_dependencia(nome_pacote: str, pip_nome: str | None = None) -> None:
    pip_nome = pip_nome or nome_pacote
    print(f"\n[ERRO] O pacote '{nome_pacote}' não está instalado.")
    print(f"       Instale com: pip install {pip_nome}\n")
    sys.exit(1)


try:
    from openai import OpenAI
except ImportError:
    _falta_dependencia("openai")

try:
    from gtts import gTTS
except ImportError:
    _falta_dependencia("gtts", "gTTS")

try:
    import sounddevice as sd
    from scipy.io.wavfile import write as write_wav
except ImportError:
    sd = None
    write_wav = None
    # Só é obrigatório se o usuário optar por gravar áudio; verificado depois.

try:
    from playsound import playsound
except ImportError:
    playsound = None
    # Só é obrigatório para tocar a resposta em áudio; verificado depois.


# ---------------------------------------------------------------------------
# Configuração / constantes
# ---------------------------------------------------------------------------

SAMPLE_RATE = 44100
CANAIS = 1
MENSAGEM_SISTEMA = (
    "Você é um assistente prestativo que responde de forma clara, "
    "objetiva e amigável, no idioma em que o usuário está falando."
)


# ---------------------------------------------------------------------------
# Funções principais
# ---------------------------------------------------------------------------

def obter_cliente_openai() -> "OpenAI":
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("\n[ERRO] Variável de ambiente OPENAI_API_KEY não definida.")
        print("       Defina sua chave antes de rodar o script. Exemplo:")
        print('       export OPENAI_API_KEY="sua-chave-aqui"\n')
        sys.exit(1)
    return OpenAI(api_key=api_key)


def gravar_audio(duracao: int, caminho_saida: str) -> bool:
    """Grava áudio do microfone por `duracao` segundos e salva como WAV."""
    if sd is None or write_wav is None:
        print("\n[ERRO] Gravação de áudio requer 'sounddevice' e 'scipy'.")
        print("       Instale com: pip install sounddevice scipy\n")
        return False

    try:
        print(f"🎙️  Gravando por {duracao}s... fale agora.")
        audio = sd.rec(
            int(duracao * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CANAIS,
            dtype="int16",
        )
        sd.wait()
        write_wav(caminho_saida, SAMPLE_RATE, audio)
        print("✅ Gravação concluída.")
        return True
    except Exception as exc:  # dispositivo de áudio indisponível, permissão, etc.
        print(f"\n[ERRO] Não foi possível gravar áudio: {exc}")
        print("       Verifique se há um microfone conectado e com permissão de uso.\n")
        return False


def transcrever_audio(cliente: "OpenAI", caminho_audio: str, idioma: str | None) -> str | None:
    """Envia o áudio para a API Whisper da OpenAI e retorna o texto transcrito."""
    try:
        with open(caminho_audio, "rb") as arquivo_audio:
            kwargs = {"model": "whisper-1", "file": arquivo_audio}
            if idioma:
                kwargs["language"] = idioma
            resposta = cliente.audio.transcriptions.create(**kwargs)
        return resposta.text.strip()
    except Exception as exc:
        print(f"\n[ERRO] Falha ao transcrever áudio com Whisper: {exc}\n")
        return None


def perguntar_chatgpt(cliente: "OpenAI", modelo: str, historico: list) -> str | None:
    """Envia o histórico da conversa ao ChatGPT e retorna a resposta em texto."""
    try:
        resposta = cliente.chat.completions.create(
            model=modelo,
            messages=historico,
        )
        return resposta.choices[0].message.content.strip()
    except Exception as exc:
        print(f"\n[ERRO] Falha ao consultar o ChatGPT: {exc}\n")
        return None


def falar_resposta(texto: str, idioma_tts: str, tocar_audio: bool) -> str | None:
    """Converte texto em fala com gTTS, salva em .mp3 e (opcionalmente) reproduz."""
    try:
        tts = gTTS(text=texto, lang=idioma_tts)
        caminho_mp3 = os.path.join(
            tempfile.gettempdir(), f"resposta_{datetime.datetime.now():%H%M%S}.mp3"
        )
        tts.save(caminho_mp3)
    except Exception as exc:
        print(f"\n[ERRO] Falha ao gerar áudio com gTTS: {exc}\n")
        return None

    if tocar_audio:
        if playsound is None:
            print("[AVISO] 'playsound' não instalado — pulando reprodução automática.")
            print("        Instale com: pip install playsound==1.2.2")
        else:
            try:
                playsound(caminho_mp3)
            except Exception as exc:
                print(f"[AVISO] Não foi possível reproduzir o áudio automaticamente: {exc}")

    return caminho_mp3


def salvar_log(historico: list, caminho_log: str) -> None:
    try:
        with open(caminho_log, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"Log da conversa — {datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n")
            arquivo.write("=" * 60 + "\n\n")
            for mensagem in historico:
                if mensagem["role"] == "system":
                    continue
                papel = "Você" if mensagem["role"] == "user" else "Assistente"
                arquivo.write(f"{papel}: {mensagem['content']}\n\n")
        print(f"📝 Conversa salva em: {caminho_log}")
    except Exception as exc:
        print(f"[AVISO] Não foi possível salvar o log da conversa: {exc}")


# ---------------------------------------------------------------------------
# Menu / loop principal
# ---------------------------------------------------------------------------

def exibir_menu() -> str:
    print("\n" + "-" * 40)
    print("1) 🎙️  Falar")
    print("2) ⌨️  Digitar mensagem")
    print("3) 🚪 Sair")
    print("-" * 40)
    return input("Escolha uma opção [1-3]: ").strip()


def executar_chat(args: argparse.Namespace) -> None:
    cliente = obter_cliente_openai()
    historico = [{"role": "system", "content": MENSAGEM_SISTEMA}]

    print("=" * 60)
    print(" Chat por voz — Whisper + ChatGPT + gTTS ".center(60, "="))
    print("=" * 60)
    print(f"Modelo de chat : {args.model}")
    print(f"Idioma (dica)  : {args.lang or 'detecção automática'}")
    print(f"Duração grav.  : {args.duration}s")
    print(f"Áudio de saída : {'desativado' if args.no_audio_output else 'ativado'}")

    try:
        while True:
            escolha = exibir_menu()

            if escolha == "3":
                print("\nEncerrando. Até a próxima! 👋")
                break

            if escolha == "1":
                caminho_wav = os.path.join(tempfile.gettempdir(), "entrada_usuario.wav")
                if not gravar_audio(args.duration, caminho_wav):
                    continue
                texto_usuario = transcrever_audio(cliente, caminho_wav, args.lang)
                if not texto_usuario:
                    print("[AVISO] Não foi possível entender o áudio. Tente novamente.")
                    continue
                print(f"🗣️  Você disse: {texto_usuario}")

            elif escolha == "2":
                texto_usuario = input("Digite sua mensagem: ").strip()
                if not texto_usuario:
                    print("[AVISO] Mensagem vazia, tente novamente.")
                    continue

            else:
                print("[AVISO] Opção inválida. Escolha 1, 2 ou 3.")
                continue

            historico.append({"role": "user", "content": texto_usuario})

            resposta = perguntar_chatgpt(cliente, args.model, historico)
            if not resposta:
                historico.pop()  # remove a pergunta que não teve resposta válida
                continue

            historico.append({"role": "assistant", "content": resposta})
            print(f"🤖 Assistente: {resposta}")

            if not args.no_audio_output:
                idioma_tts = args.lang or "pt"
                falar_resposta(resposta, idioma_tts, tocar_audio=True)

    except KeyboardInterrupt:
        print("\n\nInterrompido pelo usuário (Ctrl+C).")

    finally:
        if len(historico) > 1:
            caminho_log = os.path.join(
                os.getcwd(), f"conversa_{datetime.datetime.now():%Y%m%d_%H%M%S}.txt"
            )
            salvar_log(historico, caminho_log)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Chat por voz multi-idiomas com Whisper (STT), ChatGPT e gTTS (TTS)."
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="Modelo de chat da OpenAI a ser usado (padrão: gpt-4o-mini).",
    )
    parser.add_argument(
        "--lang",
        default=None,
        help=(
            "Código de idioma (ex.: pt, en, es). Usado como dica para o Whisper "
            "e como idioma da resposta em áudio (gTTS). Se omitido, o Whisper "
            "detecta automaticamente e a fala usa 'pt'."
        ),
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=5,
        help="Duração em segundos de cada gravação de voz (padrão: 5).",
    )
    parser.add_argument(
        "--no-audio-output",
        action="store_true",
        help="Desativa a geração/reprodução de áudio da resposta (apenas texto).",
    )
    return parser


def main() -> None:
    parser = criar_parser()
    args = parser.parse_args()
    executar_chat(args)


if __name__ == "__main__":
    main()
