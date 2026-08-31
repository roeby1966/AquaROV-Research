from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Detection:
    """Generic AI detection result."""

    label: str
    confidence: float
    x1: float
    y1: float
    x2: float
    y2: float
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Telemetry:
    """ROV telemetry data."""

    depth: float
    heading: float
    pitch: float
    roll: float
    battery: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class SensorReading:
    """Generic underwater sensor reading."""

    sensor_name: str
    value: float
    unit: str
    timestamp: datetime


@dataclass
class MissionStatus:
    """Current AquaROV mission status."""

    mission_type: str
    mission_id: str
    active: bool
    elapsed_seconds: float
