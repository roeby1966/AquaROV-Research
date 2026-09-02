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
    """Mission for inspecting underwater infrastructure."""

    mission_type = "infrastructure_inspection"

    def __init__(self, mission_id: str) -> None:
        super().__init__(mission_id)
        self._inspection_summary: dict[str, Any] = {
            "structure_observations": 0,
            "defects_detected": 0,
            "critical_defects": 0,
            "coverage_percent": 0.0,
            "inspection_records": 0,
        }

    @property
    def inspection_summary(self) -> dict[str, Any]:
        """Return the current infrastructure inspection summary."""
        return dict(self._inspection_summary)

    def record_structure_observation(
        self,
        structure_type: str,
        condition: str,
        location: str | None = None,
        description: str | None = None,
    ) -> None:
        """Record an observation of an underwater structure."""
        if not structure_type:
            raise ValueError("structure_type must not be empty")

        if not condition:
            raise ValueError("condition must not be empty")

        self.add_observation(
            {
                "type": "structure",
                "structure_type": structure_type,
                "condition": condition,
                "location": location,
                "description": description,
            }
        )

        self._inspection_summary["structure_observations"] += 1

    def record_defect(
        self,
        defect_type: str,
        severity: str,
        location: str | None = None,
        description: str | None = None,
    ) -> None:
        """Record a detected structural defect."""
        if not defect_type:
            raise ValueError("defect_type must not be empty")

        if not severity:
            raise ValueError("severity must not be empty")

        self.add_observation(
            {
                "type": "defect",
                "defect_type": defect_type,
                "severity": severity,
                "location": location,
                "description": description,
            }
        )

        self._inspection_summary["defects_detected"] += 1

        if severity.lower() == "critical":
            self._inspection_summary["critical_defects"] += 1

    def record_coverage(self, percent: float) -> None:
        """Record the estimated percentage of the inspection area covered."""
        if not 0.0 <= percent <= 100.0:
            raise ValueError("coverage percent must be between 0 and 100")

        self.add_observation(
            {
                "type": "coverage",
                "percent": percent,
            }
        )

        self._inspection_summary["coverage_percent"] = percent

    def record_inspection_record(
        self,
        record_id: str,
        inspection_type: str,
        location: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Record a formal inspection record."""
        if not record_id:
            raise ValueError("record_id must not be empty")

        if not inspection_type:
            raise ValueError("inspection_type must not be empty")

        self.add_observation(
            {
                "type": "inspection_record",
                "record_id": record_id,
                "inspection_type": inspection_type,
                "location": location,
                "metadata": dict(metadata or {}),
            }
        )

        self._inspection_summary["inspection_records"] += 1

    def execute(self) -> MissionResult:
        """Execute the underwater infrastructure inspection mission."""
        self.start()

        return self.stop()


__all__ = [
    "InfrastructureInspectionMission",
      ]
