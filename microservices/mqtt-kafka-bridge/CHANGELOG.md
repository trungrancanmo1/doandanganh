# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), 
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

---

## [1.1.0] - 2025-04-15
### Added
- Added a new Kafka producer service

### Changed
- Moved to use Kafka dedicated message queue with microservices
architecture

### Deprecated
- The celery task worker and redis integration

### Removed

### Fixed

### Security

---

## [1.0.0] - 2025-04-01
### Added
- Released the initial version of the local processing service
- Added celery worker with redis in-memory database for caching
### Deprecated
- adafruitio_client, firebase, mqtt_client, routes