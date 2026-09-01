"""
AquaROV Research - Data Transfer Objects

Hardware-agnostic data structures shared across the AquaROV core.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class BoundingBox:
    """Bounding box coordinates for an object detection."""

    x1: float
    y1: float
    x2: float
    y2: float


@dataclass
class Detection:
    """A single AI object detection result."""

    label: str
    confidence: float
    bbox: BoundingBox
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Telemetry:
    """Current ROV telemetry data."""

    depth: float
    heading: float
    pitch: float
    roll: float
    battery: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class SensorReading:
    """A generic sensor measurement."""

    sensor_name: str
    value: float
    unit: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class MissionStatus:
    """Current status of an ROV mission."""

    mission_type: str
    mission_id: str
    active: bool
    elapsed_seconds: float


__all__ = [
    "BoundingBox",
    "Detection",
    "Telemetry",
    "SensorReading",
    "MissionStatus",
    ]
