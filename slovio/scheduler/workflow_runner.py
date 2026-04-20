import asyncio
from core.permissions import PermissionGate
from core.logger import log_action, log_error

class WorkflowRunner:
    def __init__(self):
        self.gate = PermissionGate()

    async def run(self, workflow):
        steps = workflow.get("steps", [])
        results = {}
        pending_steps = {s["id"]: s for s in steps}
        
        while pending_steps:
            ready_steps = []
            for s_id, step in pending_steps.items():
                deps = step.get("depends_on", [])
                if all(d in results and results[d]["status"] == "success" for d in deps):
                    ready_steps.append(step)
            
            if not ready_steps:
                break # Circular dependency or failed dependency
                
            tasks = []
            for step in ready_steps:
                tasks.append(self._execute_step(workflow["name"], step))
                
            completed = await asyncio.gather(*tasks, return_exceptions=True)
            for step, res in zip(ready_steps, completed):
                results[step["id"]] = res
                del pending_steps[step["id"]]

    async def _execute_step(self, wf_name, step):
        action = step.get("action")
        params = step.get("params", {})
        result_obj = {"status": "error", "output": None, "error": None}
        
        try:
            self.gate.check(action, params)
            # Use the existing execute_tool logic from core loop map
            from core.loop import execute_tool, run as ask_slovio_run
            if action == "ask_slovio":
                out = await ask_slovio_run(params.get("goal"), use_vision=params.get("use_vision", False))
                result_obj["output"] = out
                result_obj["status"] = "success"
            else:
                out = await execute_tool(action, params)
                result_obj["output"] = out
                result_obj["status"] = "success"
                
            log_action(wf_name, step["id"], "success")
        except Exception as e:
            result_obj["error"] = str(e)
            log_error(f"Workflow {wf_name} Step {step['id']}", str(e))
            
        return result_obj
