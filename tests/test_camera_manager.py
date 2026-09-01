"""
Tests for AquaROV CameraManager.
"""

from aquarov.core.camera_manager import CameraManager, MemoryCameraBackend
from aquarov.core.dto import CameraChannel
from aquarov.core.inference_worker import InferenceFrame

class FakeInferenceWorker:
    """Minimal fake inference worker for testing frame submission."""

    def __init__(self) -> None:
        self.frames: list[InferenceFrame] = []

    def submit(self, frame: InferenceFrame) -> bool:
        self.frames.append(frame)
        return True


def make_channel(camera_id: str = "cam-1") -> CameraChannel:
    """Create a test camera channel."""
    return CameraChannel(
        camera_id=camera_id,
        name=f"Camera {camera_id}",
        source_type="memory",
    )


def test_manager_starts_empty() -> None:
    manager = CameraManager()

    assert manager.list_cameras() == []
    assert manager.connected_cameras() == []


def test_register_camera() -> None:
    manager = CameraManager()
    backend = MemoryCameraBackend()
    channel = make_channel()

    manager.register_camera(channel, backend)

    assert manager.list_cameras() == [channel]
    assert manager.connected_cameras() == []


def test_duplicate_camera_registration_raises() -> None:
    manager = CameraManager()
    backend = MemoryCameraBackend()
    channel = make_channel()

    manager.register_camera(channel, backend)

    try:
        manager.register_camera(channel, MemoryCameraBackend())
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "Camera already registered" in str(exc)


def test_open_camera_updates_state() -> None:
    manager = CameraManager()
    backend = MemoryCameraBackend()

    manager.register_camera(make_channel(), backend)
    manager.open_camera("cam-1")

    state = manager.get_state("cam-1")

    assert state.connected is True
    assert state.last_error is None
    assert manager.connected_cameras() == ["cam-1"]


def test_close_camera_updates_state() -> None:
    manager = CameraManager()
    backend = MemoryCameraBackend()

    manager.register_camera(make_channel(), backend)
    manager.open_camera("cam-1")
    manager.close_camera("cam-1")

    state = manager.get_state("cam-1")

    assert state.connected is False
    assert manager.connected_cameras() == []


def test_read_frame_returns_inference_frame() -> None:
    manager = CameraManager()
    backend = MemoryCameraBackend()
    backend.add_frame("frame-data")

    manager.register_camera(make_channel(), backend)
    manager.open_camera("cam-1")

    frame = manager.read_frame("cam-1")

    assert frame is not None
    assert isinstance(frame, InferenceFrame)
    assert frame.camera_id == "cam-1"
    assert frame.frame_id == 0
    assert frame.image == "frame-data"
    assert frame.timestamp > 0


def test_read_frame_increments_frame_count() -> None:
    manager = CameraManager()
    backend = MemoryCameraBackend()
    backend.add_frame("frame-1")
    backend.add_frame("frame-2")

    manager.register_camera(make_channel(), backend)
    manager.open_camera("cam-1")

    first = manager.read_frame("cam-1")
    second = manager.read_frame("cam-1")

    assert first is not None
    assert second is not None
    assert first.frame_id == 0
    assert second.frame_id == 1

    state = manager.get_state("cam-1")
    assert state.frame_count == 2


def test_on_frame_callback_is_called() -> None:
    received: list[InferenceFrame] = []

    manager = CameraManager(on_frame=received.append)
    backend = MemoryCameraBackend()
    backend.add_frame("frame-data")

    manager.register_camera(make_channel(), backend)
    manager.open_camera("cam-1")

    frame = manager.read_frame("cam-1")

    assert frame is not None
    assert received == [frame]


def test_frame_is_submitted_to_inference_worker() -> None:
    worker = FakeInferenceWorker()
    manager = CameraManager(inference_worker=worker)

    backend = MemoryCameraBackend()
    backend.add_frame("frame-data")

    manager.register_camera(make_channel(), backend)
    manager.open_camera("cam-1")

    frame = manager.read_frame("cam-1")

    assert frame is not None
    assert worker.frames == [frame]


def test_read_frame_when_camera_is_closed_raises() -> None:
    manager = CameraManager()
    backend = MemoryCameraBackend()

    manager.register_camera(make_channel(), backend)

    try:
        manager.read_frame("cam-1")
        assert False, "Expected RuntimeError"
    except RuntimeError as exc:
        assert "Camera is not connected" in str(exc)


def test_unknown_camera_raises_key_error() -> None:
    manager = CameraManager()

    try:
        manager.get_state("unknown")
        assert False, "Expected KeyError"
    except KeyError:
        pass

    try:
        manager.open_camera("unknown")
        assert False, "Expected KeyError"
    except KeyError:
        pass


def test_memory_backend_requires_open() -> None:
    backend = MemoryCameraBackend()
    backend.add_frame("frame-data")

    try:
        backend.read()
        assert False, "Expected RuntimeError"
    except RuntimeError as exc:
        assert "not open" in str(exc)


def test_memory_backend_requires_frames() -> None:
    backend = MemoryCameraBackend()
    backend.open()

    try:
        backend.read()
        assert False, "Expected RuntimeError"
    except RuntimeError as exc:
        assert "No frames available" in str(exc)


def test_memory_backend_cycles_frames() -> None:
    backend = MemoryCameraBackend()
    backend.add_frame("frame-1")
    backend.add_frame("frame-2")
    backend.open()

    assert backend.read() == "frame-1"
    assert backend.read() == "frame-2"
    assert backend.read() == "frame-1"


def test_read_error_returns_none_and_calls_error_callback() -> None:
    errors: list[tuple[str, Exception]] = []

    manager = CameraManager(
        on_error=lambda camera_id, exc: errors.append((camera_id, exc))
    )

    backend = MemoryCameraBackend()

    manager.register_camera(make_channel(), backend)
    manager.open_camera("cam-1")

    result = manager.read_frame("cam-1")

    assert result is None
    assert len(errors) == 1
    assert errors[0][0] == "cam-1"

    state = manager.get_state("cam-1")
    assert state.last_error == "No frames available"


def test_unregister_camera_removes_camera() -> None:
    manager = CameraManager()
    backend = MemoryCameraBackend()

    manager.register_camera(make_channel(), backend)
    manager.open_camera("cam-1")
    manager.unregister_camera("cam-1")

    assert manager.list_cameras() == []
    assert manager.connected_cameras() == []

    try:
        manager.get_state("cam-1")
        assert False, "Expected KeyError"
    except KeyError:
        pass
