"""
AquaROV Research - Telemetry Manager

Hardware-agnostic telemetry management for the AquaROV core.

This module manages the current ROV telemetry state using the
Telemetry data transfer object. Hardware-specific telemetry sources
can be connected later without changing the core telemetry manager.
"""

from __future__ import annotations

from typing import Optional

from .dto import Telemetry


class TelemetryManager:
    """Manage the current ROV telemetry data."""

    def __init__(self) -> None:
        self._telemetry: Optional[Telemetry] = None

    def update(self, telemetry: Telemetry) -> None:
        """Update the current telemetry data."""
        self._telemetry = telemetry

    def get(self) -> Optional[Telemetry]:
        """Return the current telemetry data."""
        return self._telemetry

    def clear(self) -> None:
        """Clear the current telemetry data."""
        self._telemetry = None

    def has_data(self) -> bool:
        """Return whether telemetry data is available."""
        return self._telemetry is not None


__all__ = ["TelemetryManager"]
