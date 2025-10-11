# Fylum Documentation

Welcome to the Fylum documentation! This directory contains all technical documentation, planning documents, and guides.

## 📚 Documentation Structure

### Getting Started
- [Main README](../README.md) - User guide and quick start
- [AGENTS.md](../AGENTS.md) - AI assistant context and development guide

### Planning & Roadmap
- [ROADMAP.md](ROADMAP.md) - Product roadmap and version plans
- [V2_PLANNING.md](V2_PLANNING.md) - V2.0.0 detailed planning document

### Architecture
- [ADR001: CLI-First Approach](architecture/ADR001-cli-first-approach.md)
- [ADR002: GUI Framework Selection](architecture/ADR002-gui-framework-selection.md)
- [TDD Target Architecture](architecture/TDD-target-architecture.md)
- [ADR Template](architecture/adr-template.md)

### Testing
- [TESTING.md](testing/TESTING.md) - Complete testing guide
- [UAT Test Plan](testing/UAT_TEST_PLAN.md) - User acceptance testing procedures
- [UAT Testing Guide](testing/UAT_TESTING_GUIDE.md) - Guide for UAT testers
- [Test Execution Reports](../tests/test-execution-reports/) - Historical UAT results

### Releases
- [v1.0.0 Release Notes](releases/RELEASE_NOTES_v1.0.0.md)
- [GitHub Release Instructions](releases/GITHUB_RELEASE_INSTRUCTIONS.md)

## 🔍 Quick Links

### For Users
- [Installation Guide](../README.md#installation)
- [Quick Start](../README.md#quick-start)
- [Configuration Guide](../README.md#configuration)

### For Contributors
- [Testing Guide](testing/TESTING.md)
- [TDD Workflow](testing/TESTING.md#test-driven-development)
- [Running Tests](testing/TESTING.md#running-tests)

### For AI Assistants
- [AGENTS.md](../AGENTS.md) - Full development context
- [Testing Reference](testing/TESTING.md)
- [Architecture Decisions](architecture/)

## 📊 Project Stats

**V1.0.0 (Released):**
- 23 tests
- 96% coverage
- 15 MB executable

**V2.0.0 (In Development):**
- 95 tests
- 87% coverage
- 29 MB executable
- GUI + CLI

## 🎯 Current Focus

See [V2_PLANNING.md](V2_PLANNING.md) for V2.0.0 development status and upcoming features.

## 📝 Document Conventions

- **ADRs**: Architectural Decision Records - use template in `architecture/`
- **Test Plans**: Follow format in `testing/UAT_TEST_PLAN.md`
- **Release Notes**: Use `releases/RELEASE_NOTES_v1.0.0.md` as template

## 🤝 Contributing to Documentation

When adding new documentation:

1. Place in appropriate subdirectory
2. Update this README with link
3. Follow existing formatting conventions
4. Include date and version information
5. Add to git with descriptive commit message

---

**Last Updated:** October 10, 2025  
**Documentation Version:** 2.0.0
