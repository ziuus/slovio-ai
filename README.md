# 🌌 Slovio AI

> **Agentic Orbital Command — A world-class, JARVIS-like personal assistant designed for autonomous desktop orchestration.**

Slovio AI is a sophisticated neural interface that bridges natural language intent with native system execution. Built for the modern engineer, it combines real-time voice intelligence, spatial recall, and an advanced **UI Agent** capable of vision-based desktop automation to handle complex workflows with zero friction.

## ⚡ Core Features

- **Neural Interface**: Cinematic, glassmorphic "Orbital Command" dashboard featuring GSAP-powered micro-interactions and atmospheric depth.
- **Vision-Based UI Agent**: Leverages **Gemini-1.5 Flash Vision** to autonomously navigate, click, and interact with any local application based on high-level descriptions.
- **JARVIS-like Orchestration**: Integrated wake-word detection and voice synthesis for a true "eyes-free" engineering experience.
- **Autonomous Workflows**: Dynamically build and execute multi-step JSON workflows for browser automation, shell execution, and system management.
- **Spatial Memory**: Persistent state tracking and long-term memory for intelligent recall of past interactions and data.

## 🛠 Tech Stack

- **Engine**: Python 3.10+
- **Frontend**: HTML5 / Tailwind CSS / GSAP (Glassmorphic Staging)
- **Intelligence**: Google Gemini (Vision/Text) + OpenAI + Anthropic
- **Automation**: PyAutoGUI + MSS (Screen Capture) + Playwright
- **Voice**: Wake-word detection + ElevenLabs / Local TTS

## 🚀 Getting Started

1. **Environment Setup**:
   ```bash
   pip install -r slovio/requirements.txt
   playwright install chromium
   ```

2. **Configure Brain**:
   Provide your API keys in `slovio/.env`.

3. **Launch Orbital Command**:
   ```bash
   python slovio/main.py
   ```

4. **Deploy UI Agent**:
   ```bash
   cd ui-agent && pip install .
   ui-agent click "Open the terminal"
   ```

## 📂 Project Structure

- `slovio/`: Core AI engine, workflow scheduler, and WebSocket server.
- `ui-agent/`: Vision-based desktop automation CLI.
- `static/`: High-fidelity neural interface assets.

---
*Slovio AI: The Neural Layer of the Autonomous Desktop.*
