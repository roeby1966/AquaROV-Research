"""
AquaROV Research - Mission Base

Hardware-agnostic mission framework for AquaROV.

This module defines the common interface and lifecycle for all
ROV mission modules. Mission-specific implementations can extend
MissionBase without depending on specific hardware, AI accelerators,
or GUI frameworks.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class MissionResult:
    """Result produced by a mission."""

    mission_id: str
    mission_type: str
    success: bool
    started_at: datetime
    completed_at: Optional[datetime] = None
    observations: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class MissionBase(ABC):
    """Base class for all AquaROV mission modules."""

    mission_type: str = "generic"

    def __init__(self, mission_id: str) -> None:
        if not mission_id:
            raise ValueError("mission_id must not be empty")

        self.mission_id = mission_id
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self._active = False
        self._observations: list[dict[str, Any]] = []

    @property
    def active(self) -> bool:
        """Return whether the mission is currently active."""
        return self._active

    @property
    def observations(self) -> list[dict[str, Any]]:
        """Return observations collected during the mission."""
        return list(self._observations)

    def start(self) -> None:
        """Start the mission."""
        if self._active:
            return

        self.started_at = datetime.now()
        self.completed_at = None
        self._observations.clear()
        self._active = True

        self.on_start()

    def stop(self) -> MissionResult:
        """Stop the mission and return its result."""
        if not self._active:
            return self.result(success=False)

        self._active = False
        self.completed_at = datetime.now()

        self.on_stop()

        return self.result(success=True)

    def add_observation(
        self,
        observation: dict[str, Any],
    ) -> None:
        """Add an observation to the current mission."""
        if not self._active:
            raise RuntimeError("mission is not active")

        self._observations.append(dict(observation))

    def result(self, success: bool) -> MissionResult:
        """Build a mission result from the current state."""
        started_at = self.started_at or datetime.now()

        return MissionResult(
            mission_id=self.mission_id,
            mission_type=self.mission_type,
            success=success,
            started_at=started_at,
            completed_at=self.completed_at,
            observations=list(self._observations),
        )

    def on_start(self) -> None:
        """Hook called after the mission starts."""
        pass

    def on_stop(self) -> None:
        """Hook called before the mission result is returned."""
        pass

    @abstractmethod
    def execute(self) -> MissionResult:
        """Execute the mission-specific operation."""
        raise NotImplementedError


__all__ = [
    "MissionBase",
    "MissionResult",
  ]
