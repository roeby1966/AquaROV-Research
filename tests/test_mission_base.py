from datetime import datetime

import pytest

from aquarov.missions.base import MissionBase


class 
DummyMission(MissionBase):

    def execute(self):
        self.start()
        self.add_observation(
            {
                "type": "test",
                "value": 1,
            }
        )
        return self.stop()


def test_mission_requires_mission_id() -> None:
    with pytest.raises(ValueError, match="mission_id must not be empty"):
        TestMission("")


def test_mission_starts_inactive() -> None:
    mission = DummyMission("mission-001")

    assert mission.active is False
    assert mission.started_at is None
    assert mission.completed_at is None
    assert mission.observations == []


def test_start_activates_mission() -> None:
    mission = DummyMission("mission-001")

    mission.start()

    assert mission.active is True
    assert isinstance(mission.started_at, datetime)
    assert mission.completed_at is None


def test_start_is_idempotent() -> None:
    mission = DummyMission("mission-001")

    mission.start()
    first_started_at = mission.started_at

    mission.start()

    assert mission.started_at == first_started_at
    assert mission.active is True


def test_add_observation_requires_active_mission() -> None:
    mission = TestMission("mission-001")

    with pytest.raises(RuntimeError, match="mission is not active"):
        mission.add_observation({"type": "test"})


def test_add_observation_stores_copy() -> None:
    mission = DummyMission("mission-001")
    observation = {"type": "fish", "count": 10}

    mission.start()
    mission.add_observation(observation)

    observation["count"] = 20

    assert mission.observations == [
        {"type": "fish", "count": 10}
    ]


def test_stop_returns_successful_result() -> None:
    mission = DummyMission("mission-001")

    mission.start()
    mission.add_observation(
        {
            "type": "fish",
            "count": 10,
        }
    )

    result = mission.stop()

    assert mission.active is False
    assert result.success is True
    assert result.mission_id == "mission-001"
    assert result.mission_type == "test"
    assert result.completed_at is not None
    assert result.observations == [
        {
            "type": "fish",
            "count": 10,
        }
    ]


def test_stop_inactive_mission_returns_failed_result() -> None:
    mission = DummyMission("mission-001")

    result = mission.stop()

    assert result.success is False
    assert result.mission_id == "mission-001"
    assert result.mission_type == "test"
    assert result.completed_at is None


def test_execute_runs_mission() -> None:
    mission = DummyMission("mission-001")

    result = mission.execute()

    assert result.success is True
    assert result.mission_id == "mission-001"
    assert result.mission_type == "test"
    assert result.observations == [
        {
            "type": "test",
            "value": 1,
        }
    ]
