"""
AquaROV Research - Marine Ecosystem Monitoring Mission

Hardware-agnostic mission module for underwater marine ecosystem
monitoring.

This module provides the mission-level workflow for recording species,
biodiversity, environmental measurements, biological observations,
and habitat conditions. Hardware-specific cameras, AI models, and
sensors can be connected without changing the mission lifecycle.
"""

from __future__ import annotations

from typing import Any

from .base import MissionBase, MissionResult


class EcosystemMonitoringMission(MissionBase):
    """Mission for monitoring underwater marine ecosystems."""

    mission_type = "ecosystem_monitoring"

    def __init__(self, mission_id: str) -> None:
        super().__init__(mission_id)
        self._ecosystem_summary: dict[str, Any] = {
            "species_observations": 0,
            "unique_species": 0,
            "environmental_observations": 0,
            "biological_observations": 0,
            "habitat_observations": 0,
        }
        self._observed_species: set[str] = set()

    @property
    def ecosystem_summary(self) -> dict[str, Any]:
        """Return the current ecosystem monitoring summary."""
        return dict(self._ecosystem_summary)

    def record_species_observation(
        self,
        species: str,
        count: int = 1,
        location: str | None = None,
        behavior: str | None = None,
    ) -> None:
        """Record an observation of a marine species."""
        if not species:
            raise ValueError("species must not be empty")

        if count < 0:
            raise ValueError("species count must not be negative")

        self.add_observation(
            {
                "type": "species",
                "species": species,
                "count": count,
                "location": location,
                "behavior": behavior,
            }
        )

        self._observed_species.add(species)
        self._ecosystem_summary["species_observations"] += 1
        self._ecosystem_summary["unique_species"] = len(self._observed_species)

    def record_environmental_measurement(
        self,
        measurements: dict[str, Any],
    ) -> None:
        """Record environmental measurements."""
        self.add_observation(
            {
                "type": "environment",
                "measurements": dict(measurements),
            }
        )

        self._ecosystem_summary["environmental_observations"] += 1

    def record_biological_observation(
        self,
        category: str,
        description: str,
        location: str | None = None,
    ) -> None:
        """Record a biological observation."""
        if not category:
            raise ValueError("category must not be empty")

        if not description:
            raise ValueError("description must not be empty")

        self.add_observation(
            {
                "type": "biological",
                "category": category,
                "description": description,
                "location": location,
            }
        )

        self._ecosystem_summary["biological_observations"] += 1

    def record_habitat_observation(
        self,
        condition: str,
        description: str | None = None,
        location: str | None = None,
    ) -> None:
        """Record an observation of habitat condition."""
        if not condition:
            raise ValueError("condition must not be empty")

        self.add_observation(
            {
                "type": "habitat",
                "condition": condition,
                "description": description,
                "location": location,
            }
        )

        self._ecosystem_summary["habitat_observations"] += 1

    def execute(self) -> MissionResult:
        """Execute the marine ecosystem monitoring mission."""
        self.start()

        return self.stop()


__all__ = [
    "EcosystemMonitoringMission",
]
