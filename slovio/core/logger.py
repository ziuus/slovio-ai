import os
import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)))
ACTIONS_LOG = os.path.join(LOG_DIR, "slovio_actions.log")
ERRORS_LOG = os.path.join(LOG_DIR, "slovio_errors.log")

def log_action(workflow_name, step, result):
    ts = datetime.datetime.now().isoformat()
    with open(ACTIONS_LOG, "a") as f:
        f.write(f"[{ts}] WORKFLOW: {workflow_name} | STEP: {step} | RESULT: {result}\n")

def log_error(context, error):
    ts = datetime.datetime.now().isoformat()
    with open(ERRORS_LOG, "a") as f:
        f.write(f"[{ts}] ERROR in {context}: {error}\n")
