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
