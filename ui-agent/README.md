# UI Agent
A polished, modern CLI for local Computer Use / UI Automation.
It leverages Google Gemini 1.5 Flash Vision API to process screen captures and locate UI elements dynamically based on natural language descriptions, and uses `pyautogui` to execute clicks and typing safely.

## Prerequisites
- Python 3.9+
- A Google API Key (`GEMINI_API_KEY`)

## Installation

You can install this CLI tool globally on your system using `pip`.

1. **Clone or Navigate to the project directory** (where `pyproject.toml` is located):
   ```bash
   cd /home2/home/dovndev/Projects/Slovio-AI/ui-agent
   ```

2. **Install globally**:
   ```bash
   pip install .
   ```
   *(Alternatively, use `pipx install .` if you prefer to install it in an isolated environment but still have it available globally on your PATH).*

## Usage

### 1. Set your API Key
You can export it in your shell so you don't have to enter it every time:
```bash
export GEMINI_API_KEY="AIzaSyYourKeyHere..."
```
*(If you run the command without it, the CLI will securely prompt you for it).*

### 2. Available Commands

**Click on a UI Element**
```bash
ui-agent click "The blue Submit button in the bottom right corner"
```
It will:
1. Take a screenshot via `mss`
2. Send the image and description to Gemini 1.5 Flash
3. Parse the returning coordinates (normalized 0-1000)
4. Correlate to your actual screen pixel resolution
5. Move the mouse and click with a 2-second fail-safe delay.

*Customize the safety delay:*
```bash
ui-agent click "Close icon" --delay 5
```

**Type Text**
```bash
ui-agent type "Hello World!" --delay 2
```

## Safety First
- `pyautogui.FAILSAFE = True` is enabled. You can abort any action (while it's waiting during the delay, or while the mouse is moving) by abruptly dragging your mouse pointer to any of the 4 absolute corners of your screen.
