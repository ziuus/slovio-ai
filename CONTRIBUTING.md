## Contributing

Thanks for contributing to Slovio AI.

### Before opening a pull request

- Open an issue describing the improvement or bug.
- Keep pull requests focused on one problem.
- Verify desktop automation commands still work after your change.

### Local setup

#### Ubuntu ARM64

Install the required packages before setting up the virtual environment:

```bash
sudo apt update

sudo apt install -y \
python3-venv \
python3-dev \
portaudio19-dev \
libsdl2-dev \
libsdl2-image-dev \
libsdl2-mixer-dev \
libsdl2-ttf-dev \
libfreetype6-dev
```

Then set up Python:

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

Notes:
- `pygame` may fail to install without SDL and freetype development packages
- `pyaudio` should be installed inside the virtual environment
- Playwright Chromium was not available on `ubuntu26.04-arm64` during testing, so a system Chromium installation was used instead
- Browser executable paths may require manual configuration depending on the distribution
- Desktop automation behavior may differ between Wayland and X11 sessions

#### macOS Apple Silicon

Set up Python:

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
playwright install chromium
```

Required permissions for desktop automation:

- Accessibility
- Screen Recording
- Automation

These can be enabled in:

```text
System Settings → Privacy & Security
```

Notes:
- macOS may not provide the `python` command by default, use `python3`
- Voice startup may fail if `PyAudio` is not installed correctly
- Browser automation depends on a valid Chromium executable path

#### Common issues

- If voice features continuously retry or fail to start, install PyAudio inside the virtual environment
- If Playwright cannot locate Chromium, configure the browser executable path manually
- Refreshing or closing the frontend browser tab may trigger WebSocket disconnect events during local development

### Pull request checklist

- Explain what changed and why.
- Link the related issue.
- Note any platform-specific requirements.