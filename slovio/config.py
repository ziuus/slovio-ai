import os
from dotenv import load_dotenv

load_dotenv()

BRAIN = "nvidia" # "claude" | "openai" | "ollama" | "grok" | "nvidia"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROK_API_KEY = os.getenv("GROK_API_KEY", "")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")

OLLAMA_MODEL = "phi4-mini"
GROK_MODEL = "llama-3.3-70b-versatile" # Premium default for Groq
GROK_BASE_URL = "https://api.groq.com/openai/v1" # Groq API endpoint
NVIDIA_MODEL = "meta/llama-3.1-70b-instruct" # Solid Nvidia NIM default
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

ADMIN_MODE_ENABLED = True
WAKE_WORD = "slovio"
VOICE_ENGINE = "pyttsx3" # "pyttsx3" | "elevenlabs"
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
WORKFLOWS_DIR = os.path.join(os.path.dirname(__file__), "workflows")

ACCESS_LEVELS = {
    "take_screenshot": "auto",
    "click": "auto",
    "double_click": "auto",
    "right_click": "auto",
    "type_text": "auto",
    "press_key": "auto",
    "hotkey": "auto",
    "open_app": "auto",
    "browser_navigate": "auto",
    "browser_click": "auto",
    "browser_type": "auto",
    "browser_get_content": "auto",
    "browser_screenshot": "auto",
    "run_shell_command": "auto",
    "run_python_script": "auto",
    "read_file": "auto",
    "write_file": "auto",
    "speak": "auto",
    "get_clipboard": "auto",
    "set_clipboard": "auto",
    "wait": "auto",
    "ask_slovio": "auto"
}
