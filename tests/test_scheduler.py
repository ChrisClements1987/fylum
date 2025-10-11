"""
Tests for scheduler module (TDD - tests written first)
"""

import pytest
from datetime import datetime, timedelta
from src.scheduler.manager import ScheduleManager, Schedule


def test_schedule_creation():
    """Test creating a new schedule"""
    schedule = Schedule(
        id="test-1",
        name="Daily Downloads Clean",
        cron_expression="0 9 * * *",
        enabled=True
    )
    
    assert schedule.id == "test-1"
    assert schedule.name == "Daily Downloads Clean"
    assert schedule.enabled is True


def test_schedule_manager_initialization():
    """Test ScheduleManager can be initialized"""
    manager = ScheduleManager()
    assert manager is not None
    assert hasattr(manager, 'schedules')


def test_add_schedule():
    """Test adding a schedule to manager"""
    manager = ScheduleManager()
    
    schedule = Schedule(
        id="test-1",
        name="Test Schedule",
        cron_expression="0 9 * * *",
        enabled=True
    )
    
    manager.add_schedule(schedule)
    assert len(manager.get_all_schedules()) == 1
    assert manager.get_schedule("test-1") == schedule


def test_remove_schedule():
    """Test removing a schedule"""
    manager = ScheduleManager()
    
    schedule = Schedule(
        id="test-1",
        name="Test Schedule",
        cron_expression="0 9 * * *",
        enabled=True
    )
    
    manager.add_schedule(schedule)
    assert len(manager.get_all_schedules()) == 1
    
    manager.remove_schedule("test-1")
    assert len(manager.get_all_schedules()) == 0


def test_update_schedule():
    """Test updating an existing schedule"""
    manager = ScheduleManager()
    
    schedule = Schedule(
        id="test-1",
        name="Original Name",
        cron_expression="0 9 * * *",
        enabled=True
    )
    
    manager.add_schedule(schedule)
    
    updated = Schedule(
        id="test-1",
        name="Updated Name",
        cron_expression="0 10 * * *",
        enabled=False
    )
    
    manager.update_schedule(updated)
    result = manager.get_schedule("test-1")
    
    assert result.name == "Updated Name"
    assert result.cron_expression == "0 10 * * *"
    assert result.enabled is False


def test_enable_disable_schedule():
    """Test enabling/disabling a schedule"""
    manager = ScheduleManager()
    
    schedule = Schedule(
        id="test-1",
        name="Test Schedule",
        cron_expression="0 9 * * *",
        enabled=True
    )
    
    manager.add_schedule(schedule)
    
    manager.disable_schedule("test-1")
    assert manager.get_schedule("test-1").enabled is False
    
    manager.enable_schedule("test-1")
    assert manager.get_schedule("test-1").enabled is True


def test_get_all_schedules():
    """Test retrieving all schedules"""
    manager = ScheduleManager()
    
    schedule1 = Schedule(id="test-1", name="Schedule 1", cron_expression="0 9 * * *")
    schedule2 = Schedule(id="test-2", name="Schedule 2", cron_expression="0 10 * * *")
    
    manager.add_schedule(schedule1)
    manager.add_schedule(schedule2)
    
    all_schedules = manager.get_all_schedules()
    assert len(all_schedules) == 2


def test_schedule_persistence():
    """Test schedules can be saved and loaded"""
    manager = ScheduleManager()
    
    schedule = Schedule(
        id="test-1",
        name="Test Schedule",
        cron_expression="0 9 * * *",
        enabled=True
    )
    
    manager.add_schedule(schedule)
    manager.save_schedules()
    
    new_manager = ScheduleManager()
    new_manager.load_schedules()
    
    loaded_schedule = new_manager.get_schedule("test-1")
    assert loaded_schedule is not None
    assert loaded_schedule.name == "Test Schedule"


def test_schedule_execution_tracking():
    """Test tracking when schedules are executed"""
    schedule = Schedule(
        id="test-1",
        name="Test Schedule",
        cron_expression="0 9 * * *"
    )
    
    assert schedule.last_run is None
    assert schedule.next_run is None
    
    schedule.update_last_run()
    assert schedule.last_run is not None
    assert isinstance(schedule.last_run, datetime)


def test_cron_expression_validation():
    """Test cron expressions are validated"""
    # Valid cron expression should work
    schedule = Schedule(
        id="test-1",
        name="Valid Schedule",
        cron_expression="0 9 * * *"
    )
    assert schedule.is_valid_cron() is True
    
    # Invalid cron expression should fail
    invalid_schedule = Schedule(
        id="test-2",
        name="Invalid Schedule",
        cron_expression="invalid cron"
    )
    assert invalid_schedule.is_valid_cron() is False


def test_schedule_next_run_calculation():
    """Test calculating next run time"""
    schedule = Schedule(
        id="test-1",
        name="Daily at 9 AM",
        cron_expression="0 9 * * *"
    )
    
    from datetime import timezone
    next_run = schedule.calculate_next_run()
    assert next_run is not None
    assert isinstance(next_run, datetime)
    assert next_run > datetime.now(timezone.utc)
