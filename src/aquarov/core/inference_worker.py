from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

from .dto import Detection


class InferenceModel(ABC):
    """Base interface for AI inference models."""

    @abstractmethod
    def predict(self, frame: Any) -> list[Detection]:
        """Run inference on a single frame."""
        raise NotImplementedError


class InferenceWorker:
    """Generic inference worker for the AquaROV platform."""

    def __init__(
        self,
        model: InferenceModel,
        result_callback: Optional[Callable[[list[Detection]], None]] = None,
    ) -> None:
        self.model = model
        self.result_callback = result_callback
        self.running = False

    def process_frame(self, frame: Any) -> list[Detection]:
        """Process one video frame through the active AI model."""
        detections = self.model.predict(frame)

        if self.result_callback:
            self.result_callback(detections)

        return detections

    def start(self) -> None:
        """Start inference processing."""
        self.running = True

    def stop(self) -> None:
        """Stop inference processing."""
        self.running = False
