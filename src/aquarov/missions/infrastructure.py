"""
AquaROV Research - Underwater Infrastructure Inspection Mission

Hardware-agnostic mission module for inspecting underwater
infrastructure.

This module provides the mission-level workflow for recording
structure observations, defects, inspection coverage, and
inspection records. Hardware-specific cameras, AI models,
sonar systems, and navigation systems can be connected without
changing the mission lifecycle.
"""

from __future__ import annotations

from typing import Any

from .base import MissionBase, MissionResult


class InfrastructureInspectionMission(MissionBase):
    """Mission for recording underwater infrastructure inspections."""

    mission_type = "infrastructure_inspection"

    def __init__(
        self,
        mission_id: str = "infrastructure-inspection",
    ) -> None:
        super().__init__(mission_id)

        self._structure_observations: list[dict[str, Any]] = []
        self._defects: list[dict[str, Any]] = []
        self._coverage: list[dict[str, Any]] = []
        self._inspection_records: list[dict[str, Any]] = []

    @property
    def structure_observations(self) -> list[dict[str, Any]]:
        """Return a copy of recorded structure observations."""
        return [dict(item) for item in self._structure_observations]

    @property
    def defects(self) -> list[dict[str, Any]]:
        """Return a copy of recorded defects."""
        return [dict(item) for item in self._defects]

    @property
    def coverage(self) -> list[dict[str, Any]]:
        """Return a copy of recorded inspection coverage."""
        return [dict(item) for item in self._coverage]

    @property
    def inspection_records(self) -> list[dict[str, Any]]:
        """Return a copy of inspection records."""
        return [dict(item) for item in self._inspection_records]

    @property
    def inspection_summary(self) -> dict[str, Any]:
        """Return a summary of the inspection mission."""
        return {
            "structure_observations": len(self._structure_observations),
            "defects": len(self._defects),
            "coverage_records": len(self._coverage),
            "inspection_records": len(self._inspection_records),
        }

    def record_structure_observation(
        self,
        structure_type: str,
        condition: str,
        notes: str | None = None,
    ) -> None:
        """Record an observation about an inspected structure."""

        if not structure_type.strip():
            raise ValueError("structure_type must not be empty")

        if not condition.strip():
            raise ValueError("condition must not be empty")

        observation = {
            "structure_type": structure_type,
            "condition": condition,
        }

        if notes is not None:
            observation["notes"] = notes

        self._structure_observations.append(observation)

        self.add_observation(
            {
                "type": "structure_observation",
                **observation,
            }
        )

    def record_defect(
        self,
        defect_type: str,
        severity: str,
        location: str | None = None,
        notes: str | None = None,
    ) -> None:
        """Record a defect identified during inspection."""

        if not defect_type.strip():
            raise ValueError("defect_type must not be empty")

        if not severity.strip():
            raise ValueError("severity must not be empty")

        defect = {
            "defect_type": defect_type,
            "severity": severity,
        }

        if location is not None:
            defect["location"] = location

        if notes is not None:
            defect["notes"] = notes

        self._defects.append(defect)

        self.add_observation(
            {
                "type": "defect",
                **defect,
            }
        )

    def record_coverage(
        self,
        area: str,
        percentage: float,
        notes: str | None = None,
    ) -> None:
        """Record inspection coverage for an area."""

        if not area.strip():
            raise ValueError("area must not be empty")

        if not 0.0 <= percentage <= 100.0:
            raise ValueError("percentage must be between 0 and 100")

        coverage = {
            "area": area,
            "percentage": percentage,
        }

        if notes is not None:
            coverage["notes"] = notes

        self._coverage.append(coverage)

        self.add_observation(
            {
                "type": "coverage",
                **coverage,
            }
        )

    def record_inspection(
        self,
        inspection_type: str,
        status: str,
        notes: str | None = None,
    ) -> None:
        """Record a general inspection event."""

        if not inspection_type.strip():
            raise ValueError("inspection_type must not be empty")

        if not status.strip():
            raise ValueError("status must not be empty")

        record = {
            "inspection_type": inspection_type,
            "status": status,
        }

        if notes is not None:
            record["notes"] = notes

        self._inspection_records.append(record)

        self.add_observation(
            {
                "type": "inspection",
                **record,
            }
        )

    def on_start(self) -> None:
        """Prepare the infrastructure inspection mission."""

        self.set_metadata("mission_category", "underwater_infrastructure")
        self.set_metadata("inspection_mode", "manual_or_ai_assisted")

    def on_stop(self) -> None:
        """Finalize the infrastructure inspection mission."""

        self.set_metadata(
            "structure_observation_count",
            len(self._structure_observations),
        )
        self.set_metadata(
            "defect_count",
            len(self._defects),
        )
        self.set_metadata(
            "coverage_record_count",
            len(self._coverage),
        )
        self.set_metadata(
            "inspection_record_count",
            len(self._inspection_records),
        )

    def execute(self) -> MissionResult:
        """Execute the infrastructure inspection mission.

        The actual camera, sensor, sonar, navigation, and AI systems
        are intentionally not implemented here. Hardware-specific
        systems can populate the mission through the recording
        methods while the mission lifecycle remains unchanged.
        """

        if not self.active:
            raise RuntimeError("mission is not running")

        return self.stop()


__all__ = ["InfrastructureInspectionMission"]
