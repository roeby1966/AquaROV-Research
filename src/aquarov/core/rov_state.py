"""
AquaROV Research - ROV State

Hardware-agnostic representation of the current ROV operating state.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .dto import Telemetry


@dataclass
class ROVState:
    """Current operational state of the ROV."""

    connected: bool = False
    armed: bool = False
    operating: bool = False
    telemetry: Optional[Telemetry] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def update_telemetry(self, telemetry: Telemetry) -> None:
        """Update the current telemetry data."""
        self.telemetry = telemetry
        self.timestamp = datetime.now()

    def set_connected(self, connected: bool) -> None:
        """Update the ROV connection state."""
        self.connected = connected
        self.timestamp = datetime.now()

    def set_armed(self, armed: bool) -> None:
        """Update the ROV armed state."""
        self.armed = armed
        self.timestamp = datetime.now()

    def set_operating(self, operating: bool) -> None:
        """Update the ROV operating state."""
        self.operating = operating
        self.timestamp = datetime.now()


__all__ = ["ROVState"]
