"""
Tests for AquaROV Research - Infrastructure Inspection Mission.
"""

import pytest

from aquarov.missions.infrastructure import InfrastructureInspectionMission


def test_initialization():
    mission = InfrastructureInspectionMission()

    assert mission.mission_type == "infrastructure_inspection"

    summary = mission.inspection_summary

    assert summary["structure_observations"] == 0
    assert summary["defects"] == 0
    assert summary["critical_defects"] == 0
    assert summary["coverage_percent"] == 0.0
    assert summary["inspection_records"] == 0


def test_inspection_summary_returns_copy():
    mission = InfrastructureInspectionMission()

    summary = mission.inspection_summary
    summary["defects"] = 999

    assert mission.inspection_summary["defects"] == 0


def test_record_structure_observation():
    mission = InfrastructureInspectionMission()

    result = mission.record_structure_observation(
        structure_type="net",
        condition="good",
        notes="No visible damage",
    )

    assert result["structure_type"] == "net"
    assert result["condition"] == "good"
    assert result["notes"] == "No visible damage"

    assert mission.inspection_summary["structure_observations"] == 1


def test_record_structure_observation_without_notes():
    mission = InfrastructureInspectionMission()

    result = mission.record_structure_observation(
        structure_type="frame",
        condition="fair",
    )

    assert result["structure_type"] == "frame"
    assert result["condition"] == "fair"

    assert mission.inspection_summary["structure_observations"] == 1


def test_record_structure_observation_rejects_empty_structure_type():
    mission = InfrastructureInspectionMission()

    with pytest.raises(ValueError):
        mission.record_structure_observation(
            structure_type="",
            condition="good",
        )


def test_record_structure_observation_rejects_empty_condition():
    mission = InfrastructureInspectionMission()

    with pytest.raises(ValueError):
        mission.record_structure_observation(
            structure_type="net",
            condition="",
        )


def test_record_defect():
    mission = InfrastructureInspectionMission()

    result = mission.record_defect(
        defect_type="tear",
        severity="major",
        location="north side",
        notes="Visible net damage",
    )

    assert result["defect_type"] == "tear"
    assert result["severity"] == "major"
    assert result["location"] == "north side"
    assert result["notes"] == "Visible net damage"

    assert mission.inspection_summary["defects"] == 1


def test_record_critical_defect():
    mission = InfrastructureInspectionMission()

    mission.record_defect(
        defect_type="structural_failure",
        severity="critical",
        location="anchor",
    )

    assert mission.inspection_summary["defects"] == 1
    assert mission.inspection_summary["critical_defects"] == 1


def test_record_non_critical_defect():
    mission = InfrastructureInspectionMission()

    mission.record_defect(
        defect_type="corrosion",
        severity="minor",
        location="frame",
    )

    assert mission.inspection_summary["defects"] == 1
    assert mission.inspection_summary["critical_defects"] == 0


def test_record_defect_rejects_empty_defect_type():
    mission = InfrastructureInspectionMission()

    with pytest.raises(ValueError):
        mission.record_defect(
            defect_type="",
            severity="major",
            location="frame",
        )


def test_record_defect_rejects_empty_severity():
    mission = InfrastructureInspectionMission()

    with pytest.raises(ValueError):
        mission.record_defect(
            defect_type="corrosion",
            severity="",
            location="frame",
        )


def test_record_coverage():
    mission = InfrastructureInspectionMission()

    result = mission.record_coverage(75.5)

    assert result == 75.5
    assert mission.inspection_summary["coverage_percent"] == 75.5


def test_record_coverage_zero():
    mission = InfrastructureInspectionMission()

    result = mission.record_coverage(0)

    assert result == 0.0
    assert mission.inspection_summary["coverage_percent"] == 0.0


def test_record_coverage_one_hundred():
    mission = InfrastructureInspectionMission()

    result = mission.record_coverage(100)

    assert result == 100.0
    assert mission.inspection_summary["coverage_percent"] == 100.0


def test_record_coverage_rejects_below_zero():
    mission = InfrastructureInspectionMission()

    with pytest.raises(ValueError):
        mission.record_coverage(-1)


def test_record_coverage_rejects_above_one_hundred():
    mission = InfrastructureInspectionMission()

    with pytest.raises(ValueError):
        mission.record_coverage(101)


def test_record_inspection_record():
    mission = InfrastructureInspectionMission()

    result = mission.record_inspection_record(
        record_id="INS-001",
        inspection_type="routine",
        metadata={"operator": "AquaROV"},
    )

    assert result["record_id"] == "INS-001"
    assert result["inspection_type"] == "routine"
    assert result["metadata"] == {"operator": "AquaROV"}

    assert mission.inspection_summary["inspection_records"] == 1


def test_record_inspection_record_copies_metadata():
    mission = InfrastructureInspectionMission()

    metadata = {
        "operator": "AquaROV",
    }

    result = mission.record_inspection_record(
        record_id="INS-002",
        inspection_type="routine",
        metadata=metadata,
    )

    metadata["operator"] = "changed"

    assert result["metadata"]["operator"] == "AquaROV"


def test_record_inspection_record_rejects_empty_record_id():
    mission = InfrastructureInspectionMission()

    with pytest.raises(ValueError):
        mission.record_inspection_record(
            record_id="",
            inspection_type="routine",
        )


def test_record_inspection_record_rejects_empty_inspection_type():
    mission = InfrastructureInspectionMission()

    with pytest.raises(ValueError):
        mission.record_inspection_record(
            record_id="INS-003",
            inspection_type="",
        )


def test_multiple_observations_and_defects():
    mission = InfrastructureInspectionMission()

    mission.record_structure_observation(
        structure_type="net",
        condition="good",
    )

    mission.record_structure_observation(
        structure_type="frame",
        condition="fair",
    )

    mission.record_defect(
        defect_type="tear",
        severity="major",
        location="north",
    )

    mission.record_defect(
        defect_type="failure",
        severity="critical",
        location="east",
    )

    mission.record_coverage(80)

    summary = mission.inspection_summary

    assert summary["structure_observations"] == 2
    assert summary["defects"] == 2
    assert summary["critical_defects"] == 1
    assert summary["coverage_percent"] == 80.0


def test_execute_returns_completed_result():
    mission = InfrastructureInspectionMission()

    result = mission.execute()

    assert result is not None
    assert result["status"] == "completed"
