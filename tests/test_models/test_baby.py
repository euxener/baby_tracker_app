# tests/test_models/test_baby.py

import unittest
import pytest
from datetime import datetime, timedelta
from models import milestone
from models.baby import Baby
from models.growth_record import GrowthRecord
from models.milestone import Milestone
from models.daily_log import DailyLog

class TestBaby:
    def test_init(self):
        """Test Baby initialization."""
        
        # Setup
        name = "Test Baby"
        birthdate = datetime(2023, 1, 1)
        gender = "Male"
        notes = "Test notes"
        
        # Execute
        baby = Baby(name, birthdate, gender, notes)
        
        # Assert
        assert baby.name == name
        assert baby.birthdate == birthdate
        assert baby.gender == gender
        assert baby.notes == notes
        assert baby.growth_records == []
        assert baby.milestones == []
        assert baby.daily_logs == []
        assert baby.id is not None
        
    def test_calculate_age(self):
        """Test age calculation."""
        # Setup
        birthdate = datetime(2023, 1, 1)
        baby = Baby("Test Baby", birthdate)
        
        # Execute with specific date
        as_of_date = datetime(2024, 2, 15)
        age = baby.calculate_age(as_of_date)
        
        # Assert
        assert age["years"] == 1
        assert age["months"] == 1
        assert age["days"] == 15
        assert age["total_days"] == 410 # 365 + 31 + 14
        
    def test_add_growth_record(self):
        """Test adding a growth record."""
        # Setup
        baby = Baby("Test Baby", datetime(2023, 1, 1))
        record = GrowthRecord(baby.id, datetime.now(), 10.5, 75.0, 45.0, "Test notes")
        
        # Execute
        baby.add_growth_record(record)
        
        # Assert
        assert len(baby.growth_records) == 1
        assert baby.growth_records[0] == record
        
    def test_add_milestone(self):
        """Test adding a milestone."""
        # Setup
        baby = Baby("Test Baby", datetime(2023, 1, 1))
        milestone = Milestone(baby.id, "First steps", "physical", datetime.now())
        
        # Execute
        baby.add_milestone(milestone)
        
        # Assert
        assert len(baby.milestones) == 1
        assert baby.milestones[0] == milestone
    
    def test_add_daily_log(self):
        """Test adding a daily log."""
        # Setup
        baby = Baby("Test Baby", datetime(2023, 1, 1))
        log = DailyLog(baby.id, datetime.now().date(), datetime.now().time(), "general", "Test notes")
        
        # Execute
        baby.add_daily_log(log)
        
        # Assert
        assert len(baby.daily_logs) == 1
        assert baby.daily_logs[0] == log
        
    def test_to_dict(self):
        """Test converting to dictionary."""
        
        # Setup
        name = "Test Baby"
        birthdate = datetime(2023, 1, 1)
        gender = "Male"
        notes = "Test notes"
        baby = Baby(name, birthdate, gender, notes)
        
        # Execute
        baby_dict = baby.to_dict()
        
        # Assert
        assert baby_dict["id"] == baby.id
        assert baby_dict["name"] == name
        assert baby_dict["birthdate"] == birthdate
        assert baby_dict["gender"] == gender
        assert baby_dict["notes"] == notes