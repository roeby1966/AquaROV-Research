# AquaROV Research

## Modular AI-Enabled Underwater ROV Platform

AquaROV Research is an independent R&D project exploring modular underwater ROV systems enhanced with AI for underwater exploration, mapping, inspection, and marine monitoring.

The project is designed as a reusable software and AI foundation for a future-generation AquaROV platform, where different mission capabilities can operate on the same ROV system.

## Mission Capabilities

### Aquaculture Inspection

- Fish detection and counting
- Fish activity monitoring
- Net damage detection
- Marine debris detection
- Environmental sensor integration
- Underwater inspection and monitoring

### Shipwreck Survey

- Underwater object detection
- Shipwreck structure recognition
- Photogrammetry
- 3D reconstruction
- Survey coverage tracking
- Sonar-assisted mapping

### Other Research Applications

- Marine ecosystem monitoring
- Underwater infrastructure inspection
- Marine species recognition
- Environmental data collection
- Underwater mapping and exploration

## Architecture

AquaROV follows a modular architecture:

```text
ROV Hardware
     ↓
Sensors & Telemetry
     ↓
Perception
     ↓
AI Inference
     ↓
Mission Modules
     ↓
Operator Console
     ↓
Recording & Data

The architecture is intended to
allow hardware-specific implementations, AI models, and mission modules to evolve
independently while sharing the
same core platform.
Core Software
The current repository
establishes the hardware-agnostic
core software architecture,
including:
Data Transfer Objects (DTOs)
Asynchronous AI inference worker
Camera management
ROV state management
Sensor management
Telemetry management
The core is designed so that
hardware drivers and AI
accelerator implementations can
be connected later without
requiring major changes to the
core architecture.
Testing
The project uses pytest for
automated testing.
The current test suite covers the
core modules and is continuously
verified through GitHub Actions.
Current status:
54 tests passing
Project Status
AquaROV Research is in the early
research and development stage.
The current priority is
establishing a reliable, modular
software foundation that can
support future AI, sensor,
navigation, mission-control,
recording, database, and
operator-console capabilities.
Future development will add
mission-specific capabilities on
top of the reusable core
architecture.
Collaboration
AquaROV Research is an
independent R&D project and is
open to future collaboration with:
Researchers
Universities
Engineers
Marine scientists
AI researchers
Underwater robotics communities
License
This project is released under
the MIT License.
