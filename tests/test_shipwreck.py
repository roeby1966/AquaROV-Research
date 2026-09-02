from aquarov.missions.shipwreck import ShipwreckSurveyMission


def test_shipwreck_mission_starts_inactive() -> None:
    mission = ShipwreckSurveyMission("wreck-001")
    assert mission.active is False
    assert mission.observations == []


def test_shipwreck_mission_execute() -> None:
    mission = ShipwreckSurveyMission("wreck-001")
    result = mission.execute()
    assert result.success is True
    assert result.mission_id == "wreck-001"
    assert result.mission_type == "shipwreck_survey"


def test_record_object_observation() -> None:
    mission = ShipwreckSurveyMission("wreck-001")
    mission.start()
    mission.record_object_observation("anchor", "metal anchor", "bow")
    assert mission.survey_summary["objects_detected"] == 1
    assert mission.observations[0]["type"] == "object"


def test_record_object_observation_rejects_empty_type() -> None:
    mission = ShipwreckSurveyMission("wreck-001")
    mission.start()
    try:
        mission.record_object_observation("")
        assert False
    except ValueError as exc:
        assert str(exc) == "object_type must not be empty"


def test_record_structural_observation() -> None:
    mission = ShipwreckSurveyMission("wreck-001")
    mission.start()
    mission.record_structural_observation("damaged", "stern", "high", "hull damage")
    assert mission.survey_summary["structural_observations"] == 1
    assert mission.observations[0]["type"] == "structure"


def test_record_coverage() -> None:
    mission = ShipwreckSurveyMission("wreck-001")
    mission.start()
    mission.record_coverage(75.5)
    assert mission.survey_summary["coverage_percent"] == 75.5


def test_record_coverage_rejects_invalid_percent() -> None:
    mission = ShipwreckSurveyMission("wreck-001")
    mission.start()
    try:
        mission.record_coverage(101.0)
        assert False
    except ValueError as exc:
        assert str(exc) == "coverage percent must be between 0 and 100"


def test_record_photogrammetry_frame() -> None:
    mission = ShipwreckSurveyMission("wreck-001")
    mission.start()
    mission.record_photogrammetry_frame("frame-001", "midship")
    assert mission.survey_summary["photogrammetry_frames"] == 1
    assert mission.observations[0]["type"] == "photogrammetry"


def test_record_sonar_observation() -> None:
    mission = ShipwreckSurveyMission("wreck-001")
    mission.start()
    mission.record_sonar_observation("large metallic object", 18.5, 135.0)
    assert mission.survey_summary["sonar_observations"] == 1
    assert mission.observations[0]["type"] == "sonar"


def test_shipwreck_mission_collects_multiple_observations() -> None:
    mission = ShipwreckSurveyMission("wreck-001")
    mission.start()
    mission.record_object_observation("anchor", "metal anchor", "bow")
    mission.record_structural_observation("damaged", "stern", "medium", "hull damage")
    mission.record_coverage(80.0)
    mission.record_photogrammetry_frame("frame-001", "midship")
    mission.record_sonar_observation("unknown object", 20.0, 90.0)
    assert len(mission.observations) == 5
    assert mission.survey_summary["objects_detected"] == 1
    assert mission.survey_summary["structural_observations"] == 1
    assert mission.survey_summary["coverage_percent"] == 80.0
    assert mission.survey_summary["photogrammetry_frames"] == 1
    assert mission.survey_summary["sonar_observations"] == 1
