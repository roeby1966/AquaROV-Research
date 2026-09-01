"""
AquaROV Research - Sensor Manager

Hardware-agnostic sensor management for the AquaROV core.

Sensor-specific drivers can be connected through the SensorBackend
interface without changing the core sensor manager.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Iterable

from .dto import SensorReading


class SensorBackend(ABC):
    """Interface for a hardware-specific sensor backend."""

    @abstractmethod
    def read(self) -> SensorReading:
        """Read the current value from the sensor."""
        raise NotImplementedError


class SensorManager:
    """Manage multiple sensor backends."""

    def __init__(self) -> None:
        self._sensors: Dict[str, SensorBackend] = {}

    def register(
        self,
        sensor_name: str,
        backend: SensorBackend,
    ) -> None:
        """Register a sensor backend."""
        if not sensor_name:
            raise ValueError("sensor_name must not be empty")

        self._sensors[sensor_name] = backend

    def unregister(self, sensor_name: str) -> None:
        """Remove a registered sensor."""
        self._sensors.pop(sensor_name, None)

    def read(self, sensor_name: str) -> SensorReading:
        """Read one registered sensor."""
        try:
            backend = self._sensors[sensor_name]
        except KeyError as exc:
            raise KeyError(
                f"Sensor '{sensor_name}' is not registered"
            ) from exc

        return backend.read()

    def read_all(self) -> Iterable[SensorReading]:
        """Read all registered sensors."""
        for backend in self._sensors.values():
            yield backend.read()

    def has_sensor(self, sensor_name: str) -> bool:
        """Return whether a sensor is registered."""
        return sensor_name in self._sensors

    def sensor_names(self) -> tuple[str, ...]:
        """Return the names of all registered sensors."""
        return tuple(self._sensors)
