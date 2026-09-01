from datetime import datetime

from aquarov.core.dto import (
    BoundingBox,
    Detection,
    MissionStatus,
    SensorReading,
    Telemetry,
)


def test_bounding_box():
    bbox = BoundingBox(
        x1=10.0,
        y1=20.0,
        x2=110.0,
        y2=120.0,
    )

    assert bbox.x1 == 10.0
    assert bbox.y1 == 20.0
    assert bbox.x2 == 110.0
    assert bbox.y2 == 120.0


def test_detection_uses_bounding_box():
    bbox = BoundingBox(10.0, 20.0, 110.0, 120.0)

    detection = Detection(
        label="fish",
        confidence=0.95,
        bbox=bbox,
    )

    assert detection.label == "fish"
    assert detection.confidence == 0.95
    assert detection.bbox is bbox
    assert isinstance(detection.timestamp, datetime)


def test_telemetry():
    telemetry = Telemetry(
        depth=12.5,
        heading=180.0,
        pitch=1.5,
        roll=-2.0,
        battery=87.0,
    )

    assert telemetry.depth == 12.5
    assert telemetry.heading == 180.0
    assert telemetry.battery == 87.0


def test_sensor_reading():
    reading = SensorReading(
        sensor_name="temperature",
        value=28.5,
        unit="C",
    )

    assert reading.sensor_name == "temperature"
    assert reading.value == 28.5
    assert reading.unit == "C"
    assert isinstance(reading.timestamp, datetime)


def test_mission_status():
    mission = MissionStatus(
        mission_type="shipwreck_survey",
        mission_id="MISSION-001",
        active=True,
        elapsed_seconds=120.5,
    )

    assert mission.mission_type == "shipwreck_survey"
    assert mission.mission_id == "MISSION-001"
    assert mission.active is True
    assert mission.elapsed_seconds == 120.5
