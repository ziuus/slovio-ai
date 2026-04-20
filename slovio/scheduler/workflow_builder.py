import json
import os
import config
from brain.llm import ask

SYSTEM_PROMPT = """
You map natural language to a JSON workflow. 
Schema:
{
  "name": "workflow_name",
  "trigger": {"type": "schedule", "cron": "..."} | {"type": "once", "datetime": "..."} | {"type": "interval", "hours": 1},
  "steps": [{"id": "s1", "action": "tool_name", "params": {}, "depends_on": []}]
}
Available tools: speak, run_shell_command, ask_slovio, browser_navigate, wait...
Produce ONLY valid JSON.
"""

def build_from_text(description):
    messages = [{"role": "user", "content": f"Build a workflow for: {description}"}]
    response = ask(messages, [], SYSTEM_PROMPT)
    try:
        wf = json.loads(response.content)
        print("Generated Workflow:\n", json.dumps(wf, indent=2))
        confirm = input("Save and register workflow? (y/n): ")
        if confirm.lower() == 'y':
            name = wf.get("name", "new_workflow")
            path = os.path.join(config.WORKFLOWS_DIR, f"{name}.json")
            os.makedirs(config.WORKFLOWS_DIR, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(wf, f, indent=2)
            # Would register dynamically in a real app holding ref to scheduler
            print(f"Workflow {name} saved.")
            return wf
    except Exception as e:
        print(f"Error parsing workflow: {e}")

def modify_workflow(name, instruction):
    path = os.path.join(config.WORKFLOWS_DIR, f"{name}.json")
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        wf = json.load(f)
    messages = [{"role": "user", "content": f"Modify this workflow: {json.dumps(wf)}\\nInstruction: {instruction}"}]
    response = ask(messages, [], SYSTEM_PROMPT)
    try:
        updated = json.loads(response.content)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(updated, f, indent=2)
    except:
        pass
