# Fylum Roadmap

This document outlines the development roadmap for the Fylum application, detailing the planned features for upcoming versions.

---

## V1.0.0: The CLI Foundation

**Goal:** To deliver a robust, configurable CLI tool that provides immediate value for organizing files and serves as a solid foundation for future development.

### Core Features

*   **Core CLI Tool:**
    *   A primary interface for all functionality, designed to be used in the terminal by users, power users, and AI agents.

*   **YAML Configuration File:**
    *   A human-readable `config.yaml` file for customization.
    *   **Folder Selection:** Specify target directories for cleaning.
    *   **Ignore Lists:** Define file patterns or directories to be excluded.
    *   **Customizable Rules:** Define rules for file classification and subfolder organization.

*   **Smart File Renaming:**
    *   Rename files to a consistent, customizable format (e.g., `YYYY-MM-DD_original-filename.ext`).

*   **Index Manifest:**
    *   Generate a `_fylum_index.md` file that logs all file movements, mapping original paths to their new locations.

*   **Standalone Executable:**
    *   Package the application as a single executable for easy distribution.

### Foundational Practices

*   **Comprehensive Testing:** Implement a full suite of unit and integration tests to ensure reliability.
*   **Basic Security Hardening:** Ensure file paths are handled safely and permissions are managed correctly.
*   **Robust Encoding Support:** Natively support various character encodings in filenames to prevent errors across different systems and languages.

---

## V2.0.0: The GUI Experience

**Goal:** To create a user-friendly Graphical User Interface (GUI) that makes the application accessible to a broader, less technical audience.

### Features

*   **Graphical User Interface (GUI):**
    *   A desktop application that wraps the core logic of the CLI tool.

*   **Interactive Mode:**
    *   Provide an interactive mode where users can preview and approve file operations before they are executed.

*   **Scheduling:**
    *   Ability to schedule the cleaning process to run automatically at specified intervals.

*   **System Notifications:**
    *   Provide native desktop notifications on task completion.

*   **Installer:**
    *   A simple installer for easy integration with the user's operating system.

---

## Future Development & Backlog

**Goal:** A collection of ideas and major features that are being considered for versions beyond V2.0.0.

### Potential Features

*   **Advanced Duplicate File Detection:**
    *   Implement a robust system to identify and manage duplicate files, potentially using file hashes.

*   **"Undo" Functionality:**
    *   A feature to safely revert the last cleaning operation, likely leveraging the Index Manifest.

*   **Performance Benchmarking & Optimization:**
    *   Establish performance benchmarks and optimize the application for handling very large volumes of files.

*   **Plugin Architecture for Extensibility:**
    *   Refactor the core logic to support plugins, allowing for community contributions of new rules and actions.

*   **Full Internationalization (i18n):**
    *   Translate the application's UI into multiple languages.