from aquarov.missions.ecosystem import EcosystemMonitoringMission


def test_ecosystem_mission_starts_inactive() -> None:
    mission = EcosystemMonitoringMission("eco-001")
    assert mission.active is False
    assert mission.observations == []


def test_ecosystem_mission_execute() -> None:
    mission = EcosystemMonitoringMission("eco-001")
    result = mission.execute()
    assert result.success is True
    assert result.mission_id == "eco-001"
    assert result.mission_type == "ecosystem_monitoring"


def test_record_species_observation() -> None:
    mission = EcosystemMonitoringMission("eco-001")
    mission.start()
    mission.record_species_observation("snapper", 25, "reef-east", "active")
    assert mission.ecosystem_summary["species_observations"] == 1
    assert mission.ecosystem_summary["unique_species"] == 1
    assert mission.observations[0]["species"] == "snapper"


def test_record_species_observation_tracks_unique_species() -> None:
    mission = EcosystemMonitoringMission("eco-001")
    mission.start()
    mission.record_species_observation("snapper", 10)
    mission.record_species_observation("snapper", 15)
    mission.record_species_observation("grouper", 5)
    assert mission.ecosystem_summary["species_observations"] == 3
    assert mission.ecosystem_summary["unique_species"] == 2


def test_record_species_observation_rejects_empty_species() -> None:
    mission = EcosystemMonitoringMission("eco-001")
    mission.start()
    try:
        mission.record_species_observation("")
        assert False
    except ValueError as exc:
        assert str(exc) == "species must not be empty"


def test_record_species_observation_rejects_negative_count() -> None:
    mission = EcosystemMonitoringMission("eco-001")
    mission.start()
    try:
        mission.record_species_observation("snapper", -1)
        assert False
    except ValueError as exc:
        assert str(exc) == "species count must not be negative"


def test_record_environmental_measurement() -> None:
    mission = EcosystemMonitoringMission("eco-001")
    mission.start()
    mission.record_environmental_measurement({"temperature": 28.5, "ph": 7.9})
    assert mission.ecosystem_summary["environmental_observations"] == 1
    assert mission.observations[0]["type"] == "environment"


def test_record_biological_observation() -> None:
    mission = EcosystemMonitoringMission("eco-001")
    mission.start()
    mission.record_biological_observation("coral", "healthy coral colony", "reef-west")
    assert mission.ecosystem_summary["biological_observations"] == 1
    assert mission.observations[0]["category"] == "coral"


def test_record_biological_observation_rejects_empty_category() -> None:
    mission = EcosystemMonitoringMission("eco-001")
    mission.start()
    try:
        mission.record_biological_observation("", "observation")
        assert False
    except ValueError as exc:
        assert str(exc) == "category must not be empty"


def test_record_habitat_observation() -> None:
    mission = EcosystemMonitoringMission("eco-001")
    mission.start()
    mission.record_habitat_observation("healthy", "clear reef habitat", "reef-north")
    assert mission.ecosystem_summary["habitat_observations"] == 1
    assert mission.observations[0]["type"] == "habitat"


def test_ecosystem_mission_collects_multiple_observations() -> None:
    mission = EcosystemMonitoringMission("eco-001")
    mission.start()
    mission.record_species_observation("snapper", 20, "reef-east", "active")
    mission.record_species_observation("grouper", 5, "reef-east", "normal")
    mission.record_environmental_measurement({"temperature": 29.0, "ph": 8.0})
    mission.record_biological_observation("coral", "healthy coral colony", "reef-west")
    mission.record_habitat_observation("healthy", "stable reef structure", "reef-west")
    assert len(mission.observations) == 5
    assert mission.ecosystem_summary["species_observations"] == 2
    assert mission.ecosystem_summary["unique_species"] == 2
    assert mission.ecosystem_summary["environmental_observations"] == 1
    assert mission.ecosystem_summary["biological_observations"] == 1
    assert mission.ecosystem_summary["habitat_observations"] == 1
