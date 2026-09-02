from aquarov.missions.aquaculture import AquacultureInspectionMission


def test_aquaculture_mission_starts_inactive() -> None:
    mission = AquacultureInspectionMission("aqua-001")

    assert mission.active is False
    assert mission.observations == []


def test_aquaculture_mission_execute() -> None:
    mission = AquacultureInspectionMission("aqua-001")

    result = mission.execute()

    assert result.success is True
    assert result.mission_id == "aqua-001"
    assert result.mission_type == "aquaculture_inspection"


def test_record_fish_observation() -> None:
    mission = AquacultureInspectionMission("aqua-001")

    mission.start()
    mission.record_fish_observation(count=120, activity="normal")

    assert mission.inspection_summary["fish_count"] == 120
    assert mission.inspection_summary["fish_activity"] == "normal"
    assert mission.observations == [
        {"type": "fish", "count": 120, "activity": "normal"}
    ]


def test_record_fish_observation_rejects_negative_count() -> None:
    mission = AquacultureInspectionMission("aqua-001")
    mission.start()

    try:
        mission.record_fish_observation(-1)
        assert False
    except ValueError as exc:
        assert str(exc) == "fish count must not be negative"


def test_record_net_condition() -> None:
    mission = AquacultureInspectionMission("aqua-001")

    mission.start()
    mission.record_net_condition(
        damaged=True,
        location="north-east",
        severity="high",
    )

    assert mission.inspection_summary["net_damage_detected"] is True
    assert mission.observations[0]["type"] == "net_condition"
    assert mission.observations[0]["damaged"] is True


def test_record_marine_debris() -> None:
    mission = AquacultureInspectionMission("aqua-001")

    mission.start()
    mission.record_marine_debris(
        detected=True,
        description="plastic rope",
        location="south side",
    )

    assert mission.inspection_summary["marine_debris_detected"] is True
    assert mission.observations[0]["type"] == "marine_debris"


def test_record_environmental_observation() -> None:
    mission = AquacultureInspectionMission("aqua-001")

    mission.start()
    mission.record_environmental_observation(
        {
            "temperature": 28.5,
            "ph": 7.8,
            "dissolved_oxygen": 6.2,
        }
    )

    assert mission.inspection_summary["environmental_observations"] == 1
    assert mission.observations[0]["type"] == "environment"
    assert mission.observations[0]["measurements"]["temperature"] == 28.5


def test_aquaculture_mission_collects_multiple_observations() -> None:
    mission = AquacultureInspectionMission("aqua-001")

    mission.start()
    mission.record_fish_observation(150, "active")
    mission.record_net_condition(True, "west", "medium")
    mission.record_marine_debris(True, "plastic", "bottom")
    mission.record_environmental_observation(
        {"temperature": 29.0, "ph": 8.0}
    )

    assert len(mission.observations) == 4
    assert mission.inspection_summary["fish_count"] == 150
    assert mission.inspection_summary["fish_activity"] == "active"
    assert mission.inspection_summary["net_damage_detected"] is True
    assert mission.inspection_summary["marine_debris_detected"] is True
    assert mission.inspection_summary["environmental_observations"] == 1
