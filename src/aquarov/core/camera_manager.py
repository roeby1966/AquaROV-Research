from typing import Any, Callable, Optional


class CameraManager:
    """Generic camera manager for the AquaROV platform."""

    def __init__(
        self,
        frame_callback: Optional[Callable[[Any], None]] = None,
    ) -> None:
        self.frame_callback = frame_callback
        self.camera = None
        self.running = False

    def open(self, source: Any = 0) -> bool:
        """Open a camera or video source."""
        self.camera = source
        self.running = True
        return True

    def close(self) -> None:
        """Close the current camera source."""
        self.running = False
        self.camera = None

    def process_frame(self, frame: Any) -> None:
        """Send a captured frame to the registered callback."""
        if self.frame_callback and self.running:
            self.frame_callback(frame)

    @property
    def is_open(self) -> bool:
        """Return whether the camera is currently open."""
        return self.running
