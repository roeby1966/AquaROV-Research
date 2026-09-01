from __future__ import annotations

from threading import Event
from time import sleep

import pytest

from aquarov.core.inference_worker import (
    InferenceFrame,
    InferenceResult,
    InferenceWorker,
    NullInferenceBackend,
)


def make_frame(
    camera_id: str = "cam-01",
    frame_id: int = 1,
    timestamp: float = 123.456,
) -> InferenceFrame:
    return InferenceFrame(
        camera_id=camera_id,
        frame_id=frame_id,
        timestamp=timestamp,
        image=None,
    )


def test_null_backend():
    backend = NullInferenceBackend()

    backend.start()

    frame = make_frame()
    result = backend.infer(frame)

    assert isinstance(result, InferenceResult)
    assert result.camera_id == "cam-01"
    assert result.frame_id == 1
    assert result.timestamp == 123.456
    assert result.detections == []
    assert result.inference_time_ms == 0.0
    assert result.metadata["backend"] == "null"

    backend.stop()


def test_inference_worker_rejects_invalid_queue_size():
    backend = NullInferenceBackend()

    with pytest.raises(ValueError, match="queue_size"):
        InferenceWorker(backend, queue_size=0)


def test_inference_worker_submit_when_stopped():
    backend = NullInferenceBackend()
    worker = InferenceWorker(backend)

    frame = make_frame()

    assert worker.is_running is False
    assert worker.submit(frame) is False


def test_inference_worker_start_stop():
    backend = NullInferenceBackend()
    worker = InferenceWorker(backend)

    assert worker.is_running is False

    worker.start()

    assert worker.is_running is True

    worker.stop()

    assert worker.is_running is False


def test_inference_worker_start_is_idempotent():
    backend = NullInferenceBackend()
    worker = InferenceWorker(backend)

    worker.start()
    worker.start()

    assert worker.is_running is True

    worker.stop()
    worker.stop()

    assert worker.is_running is False


def test_inference_worker_processes_frame():
    backend = NullInferenceBackend()
    results = []
    processed = Event()

    def on_result(result: InferenceResult) -> None:
        results.append(result)
        processed.set()

    worker = InferenceWorker(
        backend,
        on_result=on_result,
    )

    worker.start()

    try:
        frame = make_frame(frame_id=42)

        assert worker.submit(frame) is True
        assert processed.wait(timeout=1.0) is True

        assert len(results) == 1
        assert results[0].camera_id == "cam-01"
        assert results[0].frame_id == 42
        assert results[0].timestamp == 123.456
        assert results[0].detections == []
        assert results[0].metadata["backend"] == "null"
    finally:
        worker.stop()


def test_inference_worker_queue_size():
    backend = NullInferenceBackend()
    worker = InferenceWorker(backend, queue_size=2)

    worker.start()

    try:
        assert worker.queue_size() == 0

        first = make_frame(frame_id=1)
        second = make_frame(frame_id=2)

        assert worker.submit(first) is True
        assert worker.submit(second) is True
    finally:
        worker.stop()


def test_inference_worker_error_callback():
    class FailingBackend:
        def start(self) -> None:
            pass

        def stop(self) -> None:
            pass

        def infer(self, frame: InferenceFrame) -> InferenceResult:
            raise RuntimeError("inference failed")

    errors = []
    error_received = Event()

    def on_error(error: Exception) -> None:
        errors.append(error)
        error_received.set()

    worker = InferenceWorker(
        FailingBackend(),
        on_error=on_error,
    )

    worker.start()

    try:
        assert worker.submit(make_frame()) is True
        assert error_received.wait(timeout=1.0) is True

        assert len(errors) == 1
        assert isinstance(errors[0], RuntimeError)
        assert str(errors[0]) == "inference failed"
    finally:
        worker.stop()


def test_inference_worker_measures_inference_time():
    class SlowBackend:
        def start(self) -> None:
            pass

        def stop(self) -> None:
            pass

        def infer(self, frame: InferenceFrame) -> InferenceResult:
            sleep(0.01)

            return InferenceResult(
                camera_id=frame.camera_id,
                frame_id=frame.frame_id,
                timestamp=frame.timestamp,
                detections=[],
                inference_time_ms=0.0,
            )

    results = []
    result_received = Event()

    def on_result(result: InferenceResult) -> None:
        results.append(result)
        result_received.set()

    worker = InferenceWorker(
        SlowBackend(),
        on_result=on_result,
    )

    worker.start()

    try:
        assert worker.submit(make_frame()) is True
        assert result_received.wait(timeout=1.0) is True

        assert len(results) == 1
        assert results[0].inference_time_ms > 0.0
    finally:
        worker.stop()
