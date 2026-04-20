import subprocess
import os

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

def run_python_script(path, args=[]):
    return run_command(f"python {path} " + " ".join(args))

def run_script_at_path(path):
    if path.endswith(".py"):
        return run_python_script(path)
    elif path.endswith(".sh"):
        return run_command(f"bash {path}")
    elif path.endswith(".bat"):
        return run_command(path)
    return "Unknown script type"

def list_files(path):
    try:
        return "\n".join(os.listdir(path))
    except Exception as e:
        return str(e)

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Wrote to {path}"

def file_exists(path):
    return os.path.exists(path)

def create_folder(path):
    os.makedirs(path, exist_ok=True)
    return f"Created folder {path}"
