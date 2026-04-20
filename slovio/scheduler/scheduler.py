from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
import json
import os
import config
from scheduler.workflow_runner import WorkflowRunner
import asyncio
from datetime import datetime

class SlovioScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.runner = WorkflowRunner()
        self.jobs = {}

    def start(self):
        self.scheduler.start()

    def _sync_run(self, workflow):
        asyncio.run(self.runner.run(workflow))

    def register(self, workflow):
        trigger_def = workflow.get("trigger", {})
        trigger_type = trigger_def.get("type")
        trigger = None
        if trigger_type == "schedule":
            trigger = CronTrigger.from_crontab(trigger_def.get("cron"))
        elif trigger_type == "interval":
            trigger = IntervalTrigger(
                hours=trigger_def.get("hours", 0),
                minutes=trigger_def.get("minutes", 0),
                days=trigger_def.get("days", 0)
            )
        elif trigger_type == "once":
            dt = datetime.fromisoformat(trigger_def.get("datetime"))
            trigger = DateTrigger(run_date=dt)
            
        job = self.scheduler.add_job(
            self._sync_run,
            trigger=trigger,
            args=[workflow],
            id=workflow["name"],
            replace_existing=True
        )
        self.jobs[workflow["name"]] = job

    def pause(self, name):
        if name in self.jobs:
            self.jobs[name].pause()
            
    def resume(self, name):
        if name in self.jobs:
            self.jobs[name].resume()
            
    def delete(self, name):
        if name in self.jobs:
            self.jobs[name].remove()
            del self.jobs[name]

    def list_all(self):
        return [job.id for job in self.scheduler.get_jobs()]

    def load_and_register_all(self):
        if not os.path.exists(config.WORKFLOWS_DIR):
            os.makedirs(config.WORKFLOWS_DIR)
        for f_name in os.listdir(config.WORKFLOWS_DIR):
            if f_name.endswith(".json"):
                path = os.path.join(config.WORKFLOWS_DIR, f_name)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        wf = json.load(f)
                    self.register(wf)
                except Exception as e:
                    print(f"Error loading {f_name}: {e}")

    def run_now(self, name):
        path = os.path.join(config.WORKFLOWS_DIR, f"{name}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                wf = json.load(f)
            self._sync_run(wf)
