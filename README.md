# 🤖 Personal Assistant

> An intelligent, voice-controlled personal assistant inspired by Alexa, powered by Google Gemini and designed to run on a Raspberry Pi 5.

This project brings together the power of large language models and local hardware to create a responsive and customizable assistant. It listens for your voice, understands your commands, and uses an agentic AI core to decide which tools to use for a specific task—from playing music to managing your to-do list.

## 🚀 Features

*   **Voice-First Interface**: Activates with a "Jarvis" wake word and uses speech-to-text to understand commands.
*   **Agentic AI Core**: Leverages a **LangChain** agent powered by **Google Gemini** to intelligently process requests and select the appropriate tool.
*   **Dynamic Tool Use**: Capable of performing actions like:
    *   🎵 Playing music via YouTube Music.
    *   🌐 Searching the web for information.
    *   ✅ Managing a personal to-do list.
*   **Natural Language Response**: Uses Google Cloud's Text-to-Speech for clear and natural-sounding audio feedback.
*   **Raspberry Pi Optimized**: Built to run on a **Raspberry Pi 5** with a connected touch screen for visual feedback and interaction.

## 🛠️ Tech Stack

*   **AI/LLM**: Google Gemini (`gemini-1.5-flash`)
*   **Agent Framework**: LangChain
*   **Speech Recognition**: `SpeechRecognition` with Google's API
*   **Text-to-Speech (TTS)**: Google Cloud Text-to-Speech
*   **Hardware**: Raspberry Pi 5
*   **Core Language**: Python

## ⚠️ Known Issues

### Mac issue with `pyaudio` and `SpeechRecognition`

When executing on an Apple Silicon Mac (M1, M2, etc.), you may encounter issues with `pyaudio` and `SpeechRecognition` as they might be compiled for Intel-based CPUs.

To fix this, you can install Rosetta 2, which enables a Mac with Apple silicon to use apps built for a Mac with an Intel processor.

```console
softwareupdate --install-rosetta
```