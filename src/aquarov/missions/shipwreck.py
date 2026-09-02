"""
AquaROV Research - Shipwreck Survey Mission

Hardware-agnostic mission module for underwater shipwreck surveys.
"""

from __future__ import annotations

from typing import Any

from .base import MissionBase, MissionResult


class ShipwreckSurveyMission(MissionBase):
    """Mission for surveying and documenting underwater shipwrecks."""

    mission_type = "shipwreck_survey"

    def __init__(self, mission_id: str) -> None:
        super().__init__(mission_id)
        self._survey_summary: dict[str, Any] = {
            "objects_detected": 0,
            "structural_observations": 0,
            "coverage_percent": 0.0,
            "photogrammetry_frames": 0,
            "sonar_observations": 0,
        }

    @property
    def survey_summary(self) -> dict[str, Any]:
        """Return the current shipwreck survey summary."""
        return dict(self._survey_summary)

    def record_object_observation(
        self,
        object_type: str,
        description: str | None = None,
        location: str | None = None,
    ) -> None:
        """Record an underwater object or structure observation."""
        if not object_type:
            raise ValueError("object_type must not be empty")

        self.add_observation(
            {
                "type": "object",
                "object_type": object_type,
                "description": description,
                "location": location,
            }
        )
        self._survey_summary["objects_detected"] += 1

    def record_structural_observation(
        self,
        condition: str,
        location: str | None = None,
        severity: str | None = None,
        description: str | None = None,
    ) -> None:
        """Record the condition of a shipwreck structure."""
        if not condition:
            raise ValueError("condition must not be empty")

        self.add_observation(
            {
                "type": "structure",
                "condition": condition,
                "location": location,
                "severity": severity,
                "description": description,
            }
        )
        self._survey_summary["structural_observations"] += 1

    def record_coverage(self, percent: float) -> None:
        """Record the estimated percentage of the survey area covered."""
        if not 0.0 <= percent <= 100.0:
            raise ValueError("coverage percent must be between 0 and 100")

        self.add_observation({"type": "coverage", "percent": percent})
        self._survey_summary["coverage_percent"] = percent

    def record_photogrammetry_frame(
        self,
        frame_id: str,
        location: str | None = None,
    ) -> None:
        """Record a frame intended for photogrammetry or 3D reconstruction."""
        if not frame_id:
            raise ValueError("frame_id must not be empty")

        self.add_observation(
            {
                "type": "photogrammetry",
                "frame_id": frame_id,
                "location": location,
            }
        )
        self._survey_summary["photogrammetry_frames"] += 1

    def record_sonar_observation(
        self,
        description: str,
        range_m: float | None = None,
        bearing_deg: float | None = None,
    ) -> None:
        """Record an observation from an underwater sonar system."""
        if not description:
            raise ValueError("description must not be empty")
        if range_m is not None and range_m < 0:
            raise ValueError("range_m must not be negative")

        self.add_observation(
            {
                "type": "sonar",
                "description": description,
                "range_m": range_m,
                "bearing_deg": bearing_deg,
            }
        )
        self._survey_summary["sonar_observations"] += 1

    def execute(self) -> MissionResult:
        """Execute the shipwreck survey mission."""
        self.start()
        return self.stop()


__all__ = [
    "ShipwreckSurveyMission",
]
