from datetime import datetime
from time import sleep

from aquarov.core.dto import Telemetry
from aquarov.core.rov_state import ROVState


def make_telemetry() -> Telemetry:
    return Telemetry(
        depth=12.5,
        heading=180.0,
        pitch=2.5,
        roll=-1.5,
        battery=85.0,
    )


def test_rov_state_starts_with_default_values() -> None:
    state = ROVState()

    assert state.connected is False
    assert state.armed is False
    assert state.operating is False
    assert state.telemetry is None
    assert isinstance(state.timestamp, datetime)


def test_set_connected_updates_state() -> None:
    state = ROVState()

    state.set_connected(True)

    assert state.connected is True


def test_set_armed_updates_state() -> None:
    state = ROVState()

    state.set_armed(True)

    assert state.armed is True


def test_set_operating_updates_state() -> None:
    state = ROVState()

    state.set_operating(True)

    assert state.operating is True


def test_update_telemetry_stores_telemetry() -> None:
    state = ROVState()
    telemetry = make_telemetry()

    state.update_telemetry(telemetry)

    assert state.telemetry is telemetry
    assert state.telemetry.depth == 12.5
    assert state.telemetry.heading == 180.0
    assert state.telemetry.pitch == 2.5
    assert state.telemetry.roll == -1.5
    assert state.telemetry.battery == 85.0


def test_set_connected_updates_timestamp() -> None:
    state = ROVState()
    before = state.timestamp

    sleep(0.001)
    state.set_connected(True)

    assert state.timestamp > before


def test_set_armed_updates_timestamp() -> None:
    state = ROVState()
    before = state.timestamp

    sleep(0.001)
    state.set_armed(True)

    assert state.timestamp > before


def test_set_operating_updates_timestamp() -> None:
    state = ROVState()
    before = state.timestamp

    sleep(0.001)
    state.set_operating(True)

    assert state.timestamp > before


def test_update_telemetry_updates_timestamp() -> None:
    state = ROVState()
    before = state.timestamp

    sleep(0.001)
    state.update_telemetry(make_telemetry())

    assert state.timestamp > before
