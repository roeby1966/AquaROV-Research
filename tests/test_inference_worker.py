from aquarov.core.inference_worker import (
    InferenceFrame,
    InferenceResult,
    InferenceWorker,
    NullInferenceBackend,
)


def test_null_backend():
    backend = NullInferenceBackend()

    backend.start()

    frame = InferenceFrame(
        camera_id="cam-01",
        frame_id=1,
        timestamp=123.456,
        image=None,
    )

    result = backend.infer(frame)

    assert isinstance(result, InferenceResult)
    assert result.camera_id == "cam-01"
    assert result.frame_id == 1
    assert result.timestamp == 123.456
    assert result.detections == []
    assert result.metadata["backend"] == "null"

    backend.stop()


def test_inference_worker_start_stop():
    backend = NullInferenceBackend()
    worker = InferenceWorker(backend)

    assert worker.is_running is False

    worker.start()

    assert worker.is_running is True

    worker.stop()

    assert worker.is_running is False


def test_inference_worker_processes_frame():
    backend = NullInferenceBackend()
    results = []

    worker = InferenceWorker(
        backend,
        on_result=results.append,
    )

    worker.start()

    frame = InferenceFrame(
        camera_id="cam-01",
        frame_id=42,
        timestamp=123.456,
        image=None,
    )

    assert worker.submit(frame) is True

    worker.stop()

    assert len(results) == 1
    assert results[0].camera_id == "cam-01"
    assert results[0].frame_id == 42
    assert results[0].metadata["backend"] == "null"
