from aquarov.core.camera_manager import CameraManager


def test_camera_manager_starts_closed():
    manager = CameraManager()

    assert manager.is_open is False
    assert manager.camera is None


def test_camera_manager_open():
    manager = CameraManager()

    assert manager.open("test-source") is True
    assert manager.is_open is True
    assert manager.camera == "test-source"


def test_camera_manager_close():
    manager = CameraManager()

    manager.open("test-source")
    manager.close()

    assert manager.is_open is False
    assert manager.camera is None


def test_camera_manager_open_twice():
    manager = CameraManager()

    assert manager.open("source-1") is True
    assert manager.open("source-2") is True

    assert manager.is_open is True
    assert manager.camera == "source-2"


def test_camera_manager_close_when_already_closed():
    manager = CameraManager()

    manager.close()

    assert manager.is_open is False
    assert manager.camera is None


def test_camera_manager_process_frame():
    frames = []

    manager = CameraManager(
        frame_callback=frames.append,
    )

    manager.open("test-source")

    frame = object()
    manager.process_frame(frame)

    assert len(frames) == 1
    assert frames[0] is frame


def test_camera_manager_does_not_process_when_closed():
    frames = []

    manager = CameraManager(
        frame_callback=frames.append,
    )

    frame = object()
    manager.process_frame(frame)

    assert frames == []


def test_camera_manager_process_frame_without_callback():
    manager = CameraManager()

    manager.open("test-source")

    frame = object()

    manager.process_frame(frame)

    assert manager.is_open is True


def test_camera_manager_callback_receives_multiple_frames():
    frames = []

    manager = CameraManager(
        frame_callback=frames.append,
    )

    manager.open("test-source")

    frame_1 = object()
    frame_2 = object()
    frame_3 = object()

    manager.process_frame(frame_1)
    manager.process_frame(frame_2)
    manager.process_frame(frame_3)

    assert frames == [frame_1, frame_2, frame_3]
