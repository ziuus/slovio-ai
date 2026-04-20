import os
import sys
import time
import json
import typer
import pyautogui
import mss
import google.generativeai as genai
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="UI Automation Agent using Gemini 1.5 Flash Vision API")
console = Console()

# Safety First: Ensure FAILSAFE is enabled
pyautogui.FAILSAFE = True

def setup_gemini():
    """Ensure Gemini API key is available and configure the SDK."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        api_key = typer.prompt("GEMINI_API_KEY not found in environment. Please enter your API Key", hide_input=True)
        os.environ["GEMINI_API_KEY"] = api_key
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

def take_screenshot(output_path="screen.png"):
    """Capture the primary screen using mss and return dimensions."""
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # primary monitor
        sct.shot(mon=1, output=output_path)
    return monitor

@app.command()
def click(
    description: str, 
    delay: int = typer.Option(2, "--delay", "-d", help="Delay in seconds before clicking to allow aborting via FAILSAFE")
):
    """
    Take a full-screen screenshot, send it to Gemini asking for the exact bounding box 
    of the description, and click on it.
    """
    model = setup_gemini()
    screen_path = "screen.png"
    
    with console.status(f"[bold green]Taking screenshot and finding '{description}'...[/bold green]", spinner="dots"):
        monitor = take_screenshot(screen_path)
        screen_width = monitor["width"]
        screen_height = monitor["height"]
        
        try:
            sample_file = genai.upload_file(path=screen_path, display_name="Screenshot")
        except Exception as e:
            console.print(f"[bold red]Failed to upload image to Gemini API: {e}[/bold red]")
            os.remove(screen_path)
            raise typer.Exit(1)
            
        prompt = f"""
        Find the exact bounding box for the UI element matching: '{description}'.
        Return ONLY a JSON array of 4 integers: [ymin, xmin, ymax, xmax] 
        where the coordinates are normalized to 0-1000.
        It is absolutely critical that you only respond with the JSON array, no markdown formatting if possible.
        Example: [100, 200, 300, 400]
        """
        
        try:
            response = model.generate_content([sample_file, prompt])
        finally:
            genai.delete_file(sample_file.name)
            os.remove(screen_path)

    # Parse JSON bounds
    try:
        text_resp = response.text.strip()
        # Clean markdown code blocks if present
        if text_resp.startswith("```json"):
            text_resp = text_resp[7:-3].strip()
        elif text_resp.startswith("```"):
            text_resp = text_resp[3:-3].strip()
            
        coords = json.loads(text_resp)
        if len(coords) != 4:
            raise ValueError(f"Expected 4 coordinates, got {len(coords)}")
            
        ymin, xmin, ymax, xmax = coords
        
        # Denormalize to screen resolution
        real_x_min = int((xmin / 1000) * screen_width)
        real_y_min = int((ymin / 1000) * screen_height)
        real_x_max = int((xmax / 1000) * screen_width)
        real_y_max = int((ymax / 1000) * screen_height)
        
        center_x = (real_x_min + real_x_max) // 2
        center_y = (real_y_min + real_y_max) // 2
        
        # Display resolved data nicely
        table = Table(title="Resolved Coordinates", show_header=True, header_style="bold magenta")
        table.add_column("Normalized [y_m, x_m, y_x, x_x]", style="cyan")
        table.add_column("Actual Screen Pixels [X, Y Center]", style="yellow")
        table.add_row(str(coords), f"{center_x}, {center_y}")
        console.print(table)
        
    except Exception as e:
        console.print(f"[bold red]Error parsing coordinates from Gemini response:[/bold red] {e}")
        console.print(f"[dim]Raw response: {response.text}[/dim]")
        raise typer.Exit(1)
        
    # Execute with safety delay
    console.print(f"[bold yellow]Waiting {delay} seconds before clicking... (Move mouse to screen corner to abort!)[/bold yellow]")
    time.sleep(delay)
    
    try:
        pyautogui.moveTo(center_x, center_y, duration=0.25, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        console.print("[bold green]Click executed successfully![/bold green]")
    except pyautogui.FailSafeException:
        console.print("[bold red]Action aborted by FAILSAFE (mouse moved to corner).[/bold red]")
        raise typer.Exit(1)

@app.command()
def type(
    text: str, 
    delay: int = typer.Option(1, "--delay", "-d", help="Delay in seconds before typing")
):
    """
    Type the provided text string using pyautogui.
    """
    console.print(f"[bold yellow]Waiting {delay} seconds before typing... (Move mouse to screen corner to abort!)[/bold yellow]")
    time.sleep(delay)
    
    try:
        pyautogui.write(text, interval=0.01)
        console.print(f"[bold green]Successfully typed: '{text}'[/bold green]")
    except pyautogui.FailSafeException:
        console.print("[bold red]Action aborted by FAILSAFE (mouse moved to corner).[/bold red]")
        raise typer.Exit(1)

def cli():
    app()

if __name__ == "__main__":
    app()
