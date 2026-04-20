# Slovio AI

Slovio AI is a fully functional JARVIS-like personal assistant.

## Setup Instructions

1. Install requirements:
   `pip install -r requirements.txt`
   `playwright install chromium`
2. Create an `.env` file or export your API keys (Anthropic, OpenAI, ElevenLabs).
3. If using local LLM, ensure Ollama is running (`ollama serve`).

## Changing AI Brain
Edit `config.py` and set `BRAIN` to `"claude"`, `"openai"`, or `"ollama"`.

## Adding Workflows
Place JSON workflows in the `workflows/` directory. Use voice commands like "create workflow" to generate them dynamically.

## Running
Run `python main.py`

## Voice Commands
- "Slovio" (Wake word)
- "create workflow [description]"
- "list workflows"
- "run [workflow_name] now"
- "pause [workflow_name]"
- "stop" or "exit"
