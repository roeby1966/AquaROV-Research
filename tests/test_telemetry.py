from aquarov.core.dto import Telemetry
from aquarov.core.telemetry import TelemetryManager


def make_telemetry() -> Telemetry:
    return Telemetry(
        depth=12.5,
        heading=180.0,
        pitch=2.5,
        roll=-1.5,
        battery=85.0,
    )


def test_telemetry_manager_starts_without_data() -> None:
    manager = TelemetryManager()

    assert manager.get() is None
    assert manager.has_data() is False


def test_update_stores_telemetry() -> None:
    manager = TelemetryManager()
    telemetry = make_telemetry()

    manager.update(telemetry)

    assert manager.get() is telemetry
    assert manager.has_data() is True


def test_update_replaces_previous_telemetry() -> None:
    manager = TelemetryManager()

    first = make_telemetry()
    second = Telemetry(
        depth=20.0,
        heading=270.0,
        pitch=1.0,
        roll=0.5,
        battery=70.0,
    )

    manager.update(first)
    manager.update(second)

    assert manager.get() is second
    assert manager.get().depth == 20.0
    assert manager.get().heading == 270.0
    assert manager.get().battery == 70.0


def test_clear_removes_telemetry() -> None:
    manager = TelemetryManager()

    manager.update(make_telemetry())
    manager.clear()

    assert manager.get() is None
    assert manager.has_data() is False


def test_has_data_reflects_current_state() -> None:
    manager = TelemetryManager()

    assert manager.has_data() is False

    manager.update(make_telemetry())

    assert manager.has_data() is True

    manager.clear()

    assert manager.has_data() is False
