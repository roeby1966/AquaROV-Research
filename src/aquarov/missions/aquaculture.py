"""
AquaROV Research - Aquaculture Inspection Mission

Hardware-agnostic mission module for underwater aquaculture inspection.

This module provides the mission-level workflow for monitoring fish,
net condition, marine debris, and environmental observations.
Hardware-specific cameras, AI models, and sensors can be connected
through observations without changing the mission lifecycle.
"""

from __future__ import annotations

from typing import Any

from .base import MissionBase, MissionResult


class AquacultureInspectionMission(MissionBase):
    """Mission for inspecting underwater aquaculture environments."""

    mission_type = "aquaculture_inspection"

    def __init__(self, mission_id: str) -> None:
        super().__init__(mission_id)
        self._inspection_summary: dict[str, Any] = {
            "fish_count": 0,
            "fish_activity": None,
            "net_damage_detected": False,
            "marine_debris_detected": False,
            "environmental_observations": 0,
        }

    @property
    def inspection_summary(self) -> dict[str, Any]:
        """Return the current aquaculture inspection summary."""
        return dict(self._inspection_summary)

    def record_fish_observation(
        self,
        count: int,
        activity: str | None = None,
    ) -> None:
        """Record fish count and activity observations."""
        if count < 0:
            raise ValueError("fish count must not be negative")

        self.add_observation(
            {
                "type": "fish",
                "count": count,
                "activity": activity,
            }
        )

        self._inspection_summary["fish_count"] = count

        if activity is not None:
            self._inspection_summary["fish_activity"] = activity

    def record_net_condition(
        self,
        damaged: bool,
        location: str | None = None,
        severity: str | None = None,
    ) -> None:
        """Record the condition of the aquaculture net."""
        self.add_observation(
            {
                "type": "net_condition",
                "damaged": damaged,
                "location": location,
                "severity": severity,
            }
        )

        if damaged:
            self._inspection_summary["net_damage_detected"] = True

    def record_marine_debris(
        self,
        detected: bool,
        description: str | None = None,
        location: str | None = None,
    ) -> None:
        """Record a marine debris observation."""
        self.add_observation(
            {
                "type": "marine_debris",
                "detected": detected,
                "description": description,
                "location": location,
            }
        )

        if detected:
            self._inspection_summary["marine_debris_detected"] = True

    def record_environmental_observation(
        self,
        measurements: dict[str, Any],
    ) -> None:
        """Record environmental sensor observations."""
        self.add_observation(
            {
                "type": "environment",
                "measurements": dict(measurements),
            }
        )

        self._inspection_summary["environmental_observations"] += 1

    def execute(self) -> MissionResult:
        """Execute the aquaculture inspection mission."""
        self.start()

        return self.stop()


__all__ = [
    "AquacultureInspectionMission",
  ]
