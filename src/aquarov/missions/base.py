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
from enum import Enum
from typing import Any, Optional


class MissionState(str, Enum):
    """Lifecycle states for an AquaROV mission."""

    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


@dataclass
class MissionResult:
    """Result produced by an AquaROV mission."""

    mission_id: str
    mission_type: str
    success: bool
    started_at: datetime
    completed_at: Optional[datetime] = None
    observations: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    state: MissionState = MissionState.CREATED


class MissionBase(ABC):
    """Base class for all AquaROV mission modules."""

    mission_type: str = "generic"

    def __init__(self, mission_id: str) -> None:
        if not mission_id:
            raise ValueError("mission_id must not be empty")

        self.mission_id = mission_id
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None

        self._state = MissionState.CREATED
        self._observations: list[dict[str, Any]] = []
        self._metadata: dict[str, Any] = {}
        self._error: Optional[str] = None

    @property
    def state(self) -> MissionState:
        """Return the current mission lifecycle state."""
        return self._state

    @property
    def active(self) -> bool:
        """Return whether the mission is currently running."""
        return self._state == MissionState.RUNNING

    @property
    def observations(self) -> list[dict[str, Any]]:
        """Return a copy of observations collected by the mission."""
        return list(self._observations)

    @property
    def metadata(self) -> dict[str, Any]:
        """Return a copy of mission metadata."""
        return dict(self._metadata)

    @property
    def error(self) -> Optional[str]:
        """Return the mission error message, if any."""
        return self._error

    def start(self) -> None:
        """Start the mission.

        A mission can only be started from the CREATED state.
        """

        if self._state == MissionState.RUNNING:
            return

        if self._state != MissionState.CREATED:
            raise RuntimeError(
                f"mission cannot be started from state: {self._state.value}"
            )

        self.started_at = datetime.now()
        self.completed_at = None
        self._observations.clear()
        self._metadata.clear()
        self._error = None
        self._state = MissionState.RUNNING

        try:
            self.on_start()
        except Exception as exc:
            self._state = MissionState.FAILED
            self.completed_at = datetime.now()
            self._error = str(exc)
            raise

    def stop(self) -> MissionResult:
        """Stop a running mission and return its result."""

        if self._state != MissionState.RUNNING:
            return self.result(success=False)

        try:
            self.on_stop()
            self._state = MissionState.COMPLETED
        except Exception as exc:
            self._state = MissionState.FAILED
            self._error = str(exc)

        self.completed_at = datetime.now()

        return self.result(success=self._state == MissionState.COMPLETED)

    def cancel(self) -> MissionResult:
        """Cancel a running mission and return its result."""

        if self._state != MissionState.RUNNING:
            return self.result(success=False)

        try:
            self.on_cancel()
            self._state = MissionState.CANCELLED
        except Exception as exc:
            self._state = MissionState.FAILED
            self._error = str(exc)

        self.completed_at = datetime.now()

        return self.result(success=False)

    def fail(self, error: str) -> MissionResult:
        """Mark the mission as failed and return its result."""

        if not error:
            error = "mission failed"

        self._error = error
        self._state = MissionState.FAILED
        self.completed_at = datetime.now()

        return self.result(success=False)

    def add_observation(
        self,
        observation: dict[str, Any],
    ) -> None:
        """Add an observation to the current mission."""

        if self._state != MissionState.RUNNING:
            raise RuntimeError("mission is not running")

        self._observations.append(dict(observation))

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """Set mission metadata."""

        if not key:
            raise ValueError("metadata key must not be empty")

        self._metadata[key] = value

    def update_metadata(
        self,
        metadata: dict[str, Any],
    ) -> None:
        """Update mission metadata with multiple values."""

        self._metadata.update(metadata)

    def result(self, success: bool) -> MissionResult:
        """Build a mission result from the current mission state."""

        started_at = self.started_at or datetime.now()

        return MissionResult(
            mission_id=self.mission_id,
            mission_type=self.mission_type,
            success=success,
            started_at=started_at,
            completed_at=self.completed_at,
            observations=list(self._observations),
            metadata=dict(self._metadata),
            error=self._error,
            state=self._state,
        )

    def on_start(self) -> None:
        """Hook called after the mission enters the RUNNING state."""

    def on_stop(self) -> None:
        """Hook called when a running mission is being completed."""

    def on_cancel(self) -> None:
        """Hook called when a running mission is being cancelled."""

    @abstractmethod
    def execute(self) -> MissionResult:
        """Execute the mission-specific operation."""

        raise NotImplementedError


__all__ = [
    "MissionBase",
    "MissionResult",
    "MissionState",
    ]
