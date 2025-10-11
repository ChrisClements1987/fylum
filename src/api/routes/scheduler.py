"""
Scheduler endpoints for managing cleaning schedules
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid

from src.scheduler.manager import ScheduleManager, Schedule

router = APIRouter()
schedule_manager = ScheduleManager()


class ScheduleCreate(BaseModel):
    """Model for creating a schedule"""
    name: str
    cron_expression: str
    enabled: bool = True


class ScheduleResponse(BaseModel):
    """Model for schedule response"""
    id: str
    name: str
    cron_expression: str
    enabled: bool
    last_run: Optional[str] = None
    next_run: Optional[str] = None


@router.get("/", response_model=dict)
async def get_all_schedules():
    """Get all schedules"""
    schedules = schedule_manager.get_all_schedules()
    
    return {
        "schedules": [
            {
                "id": s.id,
                "name": s.name,
                "cron_expression": s.cron_expression,
                "enabled": s.enabled,
                "last_run": s.last_run.isoformat() if s.last_run else None,
                "next_run": s.next_run.isoformat() if s.next_run else None
            }
            for s in schedules
        ]
    }


@router.post("/", status_code=201)
async def create_schedule(schedule_data: ScheduleCreate):
    """Create a new schedule"""
    # Validate cron expression
    temp_schedule = Schedule(
        id="temp",
        name=schedule_data.name,
        cron_expression=schedule_data.cron_expression
    )
    
    if not temp_schedule.is_valid_cron():
        raise HTTPException(status_code=400, detail="Invalid cron expression")
    
    # Create schedule with unique ID
    schedule = Schedule(
        id=str(uuid.uuid4()),
        name=schedule_data.name,
        cron_expression=schedule_data.cron_expression,
        enabled=schedule_data.enabled
    )
    
    schedule_manager.add_schedule(schedule)
    schedule_manager.save_schedules()
    
    return {
        "id": schedule.id,
        "name": schedule.name,
        "cron_expression": schedule.cron_expression,
        "enabled": schedule.enabled,
        "next_run": schedule.next_run.isoformat() if schedule.next_run else None
    }


@router.get("/{schedule_id}")
async def get_schedule(schedule_id: str):
    """Get a specific schedule"""
    schedule = schedule_manager.get_schedule(schedule_id)
    
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    return {
        "id": schedule.id,
        "name": schedule.name,
        "cron_expression": schedule.cron_expression,
        "enabled": schedule.enabled,
        "last_run": schedule.last_run.isoformat() if schedule.last_run else None,
        "next_run": schedule.next_run.isoformat() if schedule.next_run else None
    }


@router.put("/{schedule_id}")
async def update_schedule(schedule_id: str, schedule_data: ScheduleCreate):
    """Update an existing schedule"""
    existing = schedule_manager.get_schedule(schedule_id)
    
    if not existing:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    # Validate cron expression
    temp_schedule = Schedule(
        id="temp",
        name=schedule_data.name,
        cron_expression=schedule_data.cron_expression
    )
    
    if not temp_schedule.is_valid_cron():
        raise HTTPException(status_code=400, detail="Invalid cron expression")
    
    # Update schedule
    updated = Schedule(
        id=schedule_id,
        name=schedule_data.name,
        cron_expression=schedule_data.cron_expression,
        enabled=schedule_data.enabled,
        last_run=existing.last_run,
        created_at=existing.created_at
    )
    
    schedule_manager.update_schedule(updated)
    schedule_manager.save_schedules()
    
    return {
        "id": updated.id,
        "name": updated.name,
        "cron_expression": updated.cron_expression,
        "enabled": updated.enabled
    }


@router.delete("/{schedule_id}", status_code=204)
async def delete_schedule(schedule_id: str):
    """Delete a schedule"""
    existing = schedule_manager.get_schedule(schedule_id)
    
    if not existing:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    schedule_manager.remove_schedule(schedule_id)
    schedule_manager.save_schedules()
    
    return None


@router.post("/{schedule_id}/enable")
async def enable_schedule(schedule_id: str):
    """Enable a schedule"""
    existing = schedule_manager.get_schedule(schedule_id)
    
    if not existing:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    schedule_manager.enable_schedule(schedule_id)
    schedule_manager.save_schedules()
    
    return {"message": "Schedule enabled", "id": schedule_id}


@router.post("/{schedule_id}/disable")
async def disable_schedule(schedule_id: str):
    """Disable a schedule"""
    existing = schedule_manager.get_schedule(schedule_id)
    
    if not existing:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    schedule_manager.disable_schedule(schedule_id)
    schedule_manager.save_schedules()
    
    return {"message": "Schedule disabled", "id": schedule_id}


@router.get("/{schedule_id}/history")
async def get_schedule_history(schedule_id: str):
    """Get execution history for a schedule"""
    existing = schedule_manager.get_schedule(schedule_id)
    
    if not existing:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    # TODO: Implement actual history tracking
    return {
        "runs": [],
        "schedule_id": schedule_id
    }
