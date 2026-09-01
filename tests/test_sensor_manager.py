from __future__ import annotations

from aquarov.core.dto import SensorReading
from aquarov.core.sensor_manager import SensorBackend, SensorManager


class FakeSensorBackend(SensorBackend):
    def __init__(
        self,
        sensor_name: str,
        value: float,
        unit: str,
    ) -> None:
        self.sensor_name = sensor_name
        self.value = value
        self.unit = unit

    def read(self) -> SensorReading:
        return SensorReading(
            sensor_name=self.sensor_name,
            value=self.value,
            unit=self.unit,
        )


def test_sensor_manager_starts_empty() -> None:
    manager = SensorManager()

    assert manager.sensor_names() == ()
    assert list(manager.read_all()) == []


def test_register_sensor() -> None:
    manager = SensorManager()
    backend = FakeSensorBackend("temperature", 28.5, "C")

    manager.register("temperature", backend)

    assert manager.has_sensor("temperature") is True
    assert manager.sensor_names() == ("temperature",)


def test_register_empty_sensor_name_raises() -> None:
    manager = SensorManager()
    backend = FakeSensorBackend("temperature", 28.5, "C")

    try:
        manager.register("", backend)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "sensor_name must not be empty" in str(exc)


def test_read_sensor() -> None:
    manager = SensorManager()
    backend = FakeSensorBackend("temperature", 28.5, "C")

    manager.register("temperature", backend)

    reading = manager.read("temperature")

    assert reading.sensor_name == "temperature"
    assert reading.value == 28.5
    assert reading.unit == "C"


def test_read_unregistered_sensor_raises_key_error() -> None:
    manager = SensorManager()

    try:
        manager.read("temperature")
        assert False, "Expected KeyError"
    except KeyError as exc:
        assert "Sensor 'temperature' is not registered" in str(exc)


def test_unregister_sensor() -> None:
    manager = SensorManager()
    backend = FakeSensorBackend("temperature", 28.5, "C")

    manager.register("temperature", backend)
    manager.unregister("temperature")

    assert manager.has_sensor("temperature") is False
    assert manager.sensor_names() == ()


def test_unregister_unknown_sensor_is_safe() -> None:
    manager = SensorManager()

    manager.unregister("temperature")

    assert manager.sensor_names() == ()


def test_read_all_sensors() -> None:
    manager = SensorManager()

    temperature = FakeSensorBackend("temperature", 28.5, "C")
    pressure = FakeSensorBackend("pressure", 1.2, "bar")
    depth = FakeSensorBackend("depth", 15.0, "m")

    manager.register("temperature", temperature)
    manager.register("pressure", pressure)
    manager.register("depth", depth)

    readings = list(manager.read_all())

    assert len(readings) == 3
    assert readings[0].sensor_name == "temperature"
    assert readings[1].sensor_name == "pressure"
    assert readings[2].sensor_name == "depth"


def test_sensor_names_preserve_registration_order() -> None:
    manager = SensorManager()

    manager.register(
        "temperature",
        FakeSensorBackend("temperature", 28.5, "C"),
    )
    manager.register(
        "pressure",
        FakeSensorBackend("pressure", 1.2, "bar"),
    )
    manager.register(
        "depth",
        FakeSensorBackend("depth", 15.0, "m"),
    )

    assert manager.sensor_names() == (
        "temperature",
        "pressure",
        "depth",
    )


def test_register_same_sensor_replaces_backend() -> None:
    manager = SensorManager()

    first = FakeSensorBackend("temperature", 28.5, "C")
    second = FakeSensorBackend("temperature", 30.0, "C")

    manager.register("temperature", first)
    manager.register("temperature", second)

    reading = manager.read("temperature")

    assert reading.value == 30.0
    assert manager.sensor_names() == ("temperature",)
