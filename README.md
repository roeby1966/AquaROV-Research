# AquaROV Research

## Underwater ROV Research & Mission Software Framework

AquaROV Research is an open-source research repository for developing a
hardware-agnostic software foundation for an intelligent underwater
Remotely Operated Vehicle (ROV).

The project focuses on building reusable mission, telemetry, data,
recording, and infrastructure-inspection software components that can
later be integrated with different underwater hardware platforms.

The software architecture is intentionally separated from specific
hardware vendors, cameras, sensors, AI accelerators, navigation systems,
and vehicle controllers.

---

## Project Vision

AquaROV is being developed as a research foundation for an intelligent
underwater inspection and monitoring system.

The long-term objective is to enable an ROV to support missions such as:

- Underwater infrastructure inspection
- Aquaculture cage inspection
- Net damage detection
- Marine debris detection
- Fish monitoring
- Environmental observation
- Water-quality monitoring
- Underwater recording and documentation
- AI-assisted inspection
- Telemetry and mission monitoring
- Future autonomous or semi-autonomous operation

The repository focuses on the software architecture and mission logic
rather than tying the system to a particular ROV hardware configuration.

---

## Design Philosophy

### Hardware Agnostic

The mission layer should not depend directly on:

- Specific cameras
- Specific thrusters
- Specific flight controllers
- Specific sonar systems
- Specific AI accelerators
- Specific navigation hardware
- Specific communication hardware

Hardware adapters can be connected at a later stage.

This allows the same mission software to operate across different
underwater platforms.

---

## Architecture

The project follows a modular architecture:

```text
                    AquaROV Application
                          │
                          ▼
                    Mission Control
                          │
          ┌─────────┼──────────┐
          │              │                │
          ▼              ▼                ▼
      Telemetry        Recording        Inspection
       Manager          Manager           Missions
          │               │                │
          └─────── ──┼──────────┘
                           │
                           ▼
                     Core Services
                           │
              ┌───────┼───────┐
              │           │           │
              ▼           ▼           ▼
           Sensors       Cameras       AI
              │           │           │
              ────────┼───────┘
                           │
                           ▼
                    Hardware Adapters
                           │
                           ▼
                    ROV Hardware
