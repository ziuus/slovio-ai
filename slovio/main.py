import sys
from types import ModuleType

# Mock pyautogui before it can be imported by anything else
mock_pyautogui = ModuleType("pyautogui")
mock_pyautogui.FAILSAFE = True
mock_pyautogui.size = lambda: (1920, 1080)
mock_pyautogui.moveTo = lambda *args, **kwargs: None
mock_pyautogui.click = lambda *args, **kwargs: None
mock_pyautogui.write = lambda *args, **kwargs: None
mock_pyautogui.typewrite = lambda *args, **kwargs: None
mock_pyautogui.position = lambda: (0, 0)
mock_pyautogui.scroll = lambda *args, **kwargs: None
mock_pyautogui.hotkey = lambda *args, **kwargs: None
mock_pyautogui.press = lambda *args, **kwargs: None
sys.modules["pyautogui"] = mock_pyautogui

import asyncio
import threading
from tools import voice
from scheduler.scheduler import SlovioScheduler
from scheduler.workflow_builder import build_from_text
from core.loop import run
from core.memory import _get_conn

scheduler = SlovioScheduler()

def voice_loop():
    while True:
        if voice.listen_for_wake_word():
            voice.speak("Yes?")
            command = voice.listen()
            if not command:
                continue
            
            print(f"Heard: {command}")
            if "create workflow" in command or "automate" in command or "schedule" in command:
                build_from_text(command)
            elif "list workflows" in command:
                wfs = scheduler.list_all()
                voice.speak(f"Active workflows: {', '.join(wfs)}")
            elif "run" in command and "now" in command:
                name = command.replace("run", "").replace("now", "").strip()
                scheduler.run_now(name)
            elif "pause" in command:
                name = command.replace("pause", "").strip()
                scheduler.pause(name)
            elif "stop" in command or "exit" in command:
                voice.speak("Shutting down Slovio")
                import sys
                sys.exit(0)
            else:
                out = asyncio.run(run(command, use_vision=False))
                voice.speak(out)

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

import sys

def term_loop():
    if not sys.stdin.isatty():
        return
    console.print(Panel("[bold cyan]Welcome to Slovio AI Terminal Interface[/bold cyan]\\nType 'exit' to quit.", title="Slovio AI", expand=False))
    while True:
        try:
            command = console.input("[bold green]Slovio>[/bold green] ")
            if command in ["exit", "q", "quit"]: break
            with console.status("[bold yellow]Slovio is thinking...[/bold yellow]"):
                out = asyncio.run(run(command, use_vision=False))
            console.print(Panel(Markdown(out), title="[bold magenta]Slovio[/bold magenta]", border_style="magenta", expand=False))
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    _get_conn() # Init DB
    scheduler.load_and_register_all()
    scheduler.start()
    console.print("[bold cyan]Slovio AI Background Services Started.[/bold cyan] Say 'Slovio' to activate voice.")
    console.print("[bold purple]Web UI available at http://localhost:8000[/bold purple]")
    
    t = threading.Thread(target=voice_loop, daemon=True)
    t.start()
    
    from server import app
    def start_server():
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    threading.Thread(target=start_server, daemon=True).start()
    
    # Keep the main thread alive if term_loop exists (e.g. in background)
    try:
        term_loop()
    finally:
        while True:
            import time
            time.sleep(10)
