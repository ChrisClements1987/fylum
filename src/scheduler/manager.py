"""
Schedule management for Fylum V2.0.0
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import json
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


class Schedule(BaseModel):
    """Represents a cleaning schedule"""
    id: str
    name: str
    cron_expression: str
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    
    def is_valid_cron(self) -> bool:
        """Validate cron expression"""
        try:
            CronTrigger.from_crontab(self.cron_expression)
            return True
        except (ValueError, TypeError):
            return False
    
    def calculate_next_run(self) -> Optional[datetime]:
        """Calculate next run time based on cron expression"""
        try:
            trigger = CronTrigger.from_crontab(self.cron_expression)
            from datetime import timezone
            now = datetime.now(timezone.utc)
            next_time = trigger.get_next_fire_time(None, now)
            self.next_run = next_time
            return next_time
        except (ValueError, TypeError):
            return None
    
    def update_last_run(self):
        """Update last run timestamp"""
        self.last_run = datetime.now()


class ScheduleManager:
    """Manages cleaning schedules"""
    
    def __init__(self, storage_path: str = "schedules.json"):
        self.storage_path = Path(storage_path)
        self.schedules: dict[str, Schedule] = {}
        self.scheduler = BackgroundScheduler()
    
    def add_schedule(self, schedule: Schedule):
        """Add a new schedule"""
        schedule.calculate_next_run()
        self.schedules[schedule.id] = schedule
        
        if schedule.enabled:
            self._register_job(schedule)
    
    def remove_schedule(self, schedule_id: str):
        """Remove a schedule"""
        if schedule_id in self.schedules:
            self._unregister_job(schedule_id)
            del self.schedules[schedule_id]
    
    def update_schedule(self, schedule: Schedule):
        """Update an existing schedule"""
        self._unregister_job(schedule.id)
        schedule.calculate_next_run()
        self.schedules[schedule.id] = schedule
        
        if schedule.enabled:
            self._register_job(schedule)
    
    def get_schedule(self, schedule_id: str) -> Optional[Schedule]:
        """Get a schedule by ID"""
        return self.schedules.get(schedule_id)
    
    def get_all_schedules(self) -> List[Schedule]:
        """Get all schedules"""
        return list(self.schedules.values())
    
    def enable_schedule(self, schedule_id: str):
        """Enable a schedule"""
        if schedule_id in self.schedules:
            self.schedules[schedule_id].enabled = True
            self._register_job(self.schedules[schedule_id])
    
    def disable_schedule(self, schedule_id: str):
        """Disable a schedule"""
        if schedule_id in self.schedules:
            self.schedules[schedule_id].enabled = False
            self._unregister_job(schedule_id)
    
    def save_schedules(self):
        """Save schedules to disk"""
        data = {
            schedule_id: schedule.model_dump(mode='json')
            for schedule_id, schedule in self.schedules.items()
        }
        
        with open(self.storage_path, "w") as f:
            json.dump(data, f, indent=2, default=str)
    
    def load_schedules(self):
        """Load schedules from disk"""
        if not self.storage_path.exists():
            return
        
        try:
            with open(self.storage_path, "r") as f:
                data = json.load(f)
            
            for schedule_id, schedule_data in data.items():
                schedule = Schedule(**schedule_data)
                self.add_schedule(schedule)
        except (json.JSONDecodeError, IOError):
            pass
    
    def _register_job(self, schedule: Schedule):
        """Register a job with APScheduler"""
        try:
            trigger = CronTrigger.from_crontab(schedule.cron_expression)
            self.scheduler.add_job(
                func=self._execute_clean,
                trigger=trigger,
                id=schedule.id,
                name=schedule.name,
                replace_existing=True
            )
        except (ValueError, TypeError):
            pass
    
    def _unregister_job(self, schedule_id: str):
        """Unregister a job from APScheduler"""
        try:
            self.scheduler.remove_job(schedule_id)
        except:
            pass
    
    def _execute_clean(self):
        """Execute the clean operation (called by scheduler)"""
        from src import config
        from src.engine import RuleEngine
        from src.processor import FileProcessor
        
        try:
            cfg = config.load_config()
            engine = RuleEngine(config=cfg, dry_run=False)
            actions = engine.process_directories()
            
            if actions:
                processor = FileProcessor(rename_format=cfg.rename_format, dry_run=False)
                processor.process_actions(actions)
        except Exception as e:
            print(f"Scheduled clean failed: {e}")
    
    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
