import asyncio
from core.permissions import PermissionGate
from core.memory import save_conversation_turn
from core.logger import log_action, log_error
from tools import desktop, shell, voice
# Browser logic will be mapped via injected context or imported directly
from tools.browser import BrowserController

TOOLS_SCHEMA = [
    {"name": "take_screenshot", "description": "Take a screenshot", "input_schema": {"type": "object", "properties": {}}},
    {"name": "click", "description": "Click at x, y", "input_schema": {"type": "object", "properties": {"x": {"type": "integer"}, "y": {"type": "integer"}}}},
    {"name": "double_click", "description": "Double click at x, y", "input_schema": {"type": "object", "properties": {"x": {"type": "integer"}, "y": {"type": "integer"}}}},
    {"name": "right_click", "description": "Right click at x, y", "input_schema": {"type": "object", "properties": {"x": {"type": "integer"}, "y": {"type": "integer"}}}},
    {"name": "type_text", "description": "Type text", "input_schema": {"type": "object", "properties": {"text": {"type": "string"}}}},
    {"name": "press_key", "description": "Press a key", "input_schema": {"type": "object", "properties": {"key": {"type": "string"}}}},
    {"name": "hotkey", "description": "Press a hotkey (comma separated strings)", "input_schema": {"type": "object", "properties": {"keys": {"type": "array", "items": {"type": "string"}}}}},
    {"name": "open_app", "description": "Open application", "input_schema": {"type": "object", "properties": {"app_name": {"type": "string"}}}},
    {"name": "browser_navigate", "description": "Browser navigate", "input_schema": {"type": "object", "properties": {"url": {"type": "string"}}}},
    {"name": "browser_click", "description": "Browser click selector", "input_schema": {"type": "object", "properties": {"selector": {"type": "string"}}}},
    {"name": "browser_type", "description": "Browser type into selector", "input_schema": {"type": "object", "properties": {"selector": {"type": "string"}, "text": {"type": "string"}}}},
    {"name": "browser_get_content", "description": "Browser get content", "input_schema": {"type": "object", "properties": {}}},
    {"name": "browser_screenshot", "description": "Browser screenshot", "input_schema": {"type": "object", "properties": {}}},
    {"name": "run_shell_command", "description": "Run shell command", "input_schema": {"type": "object", "properties": {"command": {"type": "string"}}}},
    {"name": "run_python_script", "description": "Run python script", "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}}},
    {"name": "read_file", "description": "Read file", "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}}},
    {"name": "write_file", "description": "Write to file", "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}}},
    {"name": "speak", "description": "Speak text", "input_schema": {"type": "object", "properties": {"text": {"type": "string"}}}},
    {"name": "get_clipboard", "description": "Get clipboard", "input_schema": {"type": "object", "properties": {}}},
    {"name": "set_clipboard", "description": "Set clipboard", "input_schema": {"type": "object", "properties": {"text": {"type": "string"}}}},
    {"name": "wait", "description": "Wait seconds", "input_schema": {"type": "object", "properties": {"seconds": {"type": "integer"}}}}
]

browser = BrowserController()

async def execute_tool(t_name, t_input):
    if t_name == "take_screenshot": return desktop.take_screenshot()
    elif t_name == "click": return desktop.click(t_input.get("x"), t_input.get("y"))
    elif t_name == "double_click": return desktop.double_click(t_input.get("x"), t_input.get("y"))
    elif t_name == "right_click": return desktop.right_click(t_input.get("x"), t_input.get("y"))
    elif t_name == "type_text": return desktop.type_text(t_input.get("text"))
    elif t_name == "press_key": return desktop.press_key(t_input.get("key"))
    elif t_name == "hotkey": return desktop.hotkey(*t_input.get("keys", []))
    elif t_name == "open_app": return desktop.open_app(t_input.get("app_name"))
    elif t_name.startswith("browser_"):
        if not browser.browser:
            await browser.init()
        if t_name == "browser_navigate": return await browser.navigate(t_input.get("url"))
        elif t_name == "browser_click": return await browser.click(t_input.get("selector"))
        elif t_name == "browser_type": return await browser.type_into(t_input.get("selector"), t_input.get("text"))
        elif t_name == "browser_get_content": return await browser.get_page_content()
        elif t_name == "browser_screenshot": return await browser.screenshot()
    elif t_name == "run_shell_command": return shell.run_command(t_input.get("command"))
    elif t_name == "run_python_script": return shell.run_python_script(t_input.get("path"))
    elif t_name == "read_file": return shell.read_file(t_input.get("path"))
    elif t_name == "write_file": return shell.write_file(t_input.get("path"), t_input.get("content"))
    elif t_name == "speak": voice.speak(t_input.get("text")); return "Spoken"
    elif t_name == "get_clipboard": return desktop.get_clipboard()
    elif t_name == "set_clipboard": return desktop.set_clipboard(t_input.get("text"))
    elif t_name == "wait": await asyncio.sleep(t_input.get("seconds", 1)); return f"Waited {t_input.get('seconds')}s"
    return f"Unknown tool {t_name}"

async def run(goal, use_vision=True):
    from brain.llm import ask
    
    messages = [{"role": "user", "content": goal}]
    gate = PermissionGate()
    system_prompt = "You are Slovio AI, an advanced computer control agent."
    
    for iteration in range(50):
        if use_vision:
            try:
                b64_img = desktop.take_screenshot()
                messages.append({"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_img}"}}]})
            except Exception:
                pass
                
        import json
        response = ask(messages, TOOLS_SCHEMA, system_prompt)
        save_conversation_turn("assistant", response.content)
        
        # Add the assistant message with tool calls to history (only if they exist)
        assistant_msg = {
            "role": "assistant",
            "content": response.content or ""
        }
        if response.tool_uses:
            assistant_msg["tool_calls"] = [
                {
                    "id": tu["id"],
                    "type": "function",
                    "function": {
                        "name": tu["name"],
                        "arguments": json.dumps(tu["input"])
                    }
                } for tu in response.tool_uses
            ]
        messages.append(assistant_msg)

        if response.stop_reason == "end_turn" or response.stop_reason == "stop" or not response.tool_uses:
            return response.content

        for tu in response.tool_uses:
            t_name, t_id, t_input = tu["name"], tu["id"], tu["input"]
            try:
                gate.check(t_name, t_input)
                result = await execute_tool(t_name, t_input)
                log_action("agent_loop", t_name, "Success")
            except Exception as e:
                result = f"Error: {e}"
                log_error("agent_loop", str(e))
            
            # Append tool result with correct role and ID
            messages.append({
                "role": "tool",
                "tool_call_id": t_id,
                "name": t_name,
                "content": str(result)
            })
                
    voice.speak("I reached my step limit, stopping")
    return "Reached iteration limit"
