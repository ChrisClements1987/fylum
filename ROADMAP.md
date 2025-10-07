# Fylum Roadmap

This document outlines the development roadmap for the Fylum application, detailing the planned features for upcoming versions.

---

## V1.0.0: The CLI Foundation

**Goal:** To deliver a robust, configurable CLI tool that provides immediate value for organizing files and serves as a solid foundation for future development.

### Features

*   **Core CLI Tool:**
    *   A primary interface for all functionality, designed to be used in the terminal by users, power users, and AI agents.

*   **YAML Configuration File:**
    *   A human-readable `config.yaml` file for customization.
    *   **Folder Selection:** Specify target directories for cleaning.
    *   **Ignore Lists:** Define file patterns or directories to be excluded.
    *   **Customizable Rules:** Define rules for file classification and subfolder organization (e.g., mapping `.jpg` and `.png` to an `Images` folder).

*   **Smart File Renaming:**
    *   Rename files to a consistent format. The default will be `YYYY-MM-DD_original-filename.ext`, but this will be customizable via the configuration file.

*   **Index Manifest:**
    *   Generate a `_fylum_index.md` file that logs all file movements, mapping original paths to their new locations. This is a crucial first step for potential future features like "undo" functionality.

*   **Standalone Executable:**
    *   Package the application as a single executable for easy distribution and execution without requiring a Python installation.

---

## V2.0.0: The GUI Experience

**Goal:** To create a user-friendly Graphical User Interface (GUI) that makes the application accessible to a broader, less technical audience.

### Features

*   **Graphical User Interface (GUI):**
    *   A desktop application that wraps the core logic of the CLI tool.
    *   Will allow users to select folders, configure rules, and run the cleaning process from a visual interface.

*   **Interactive Mode:**
    *   The GUI will provide an interactive mode where users can preview and approve file operations before they are executed.

*   **Scheduling:**
    *   Ability to schedule the cleaning process to run automatically at specified intervals (e.g., daily, weekly).

*   **Installer:**
    *   A simple installer to properly integrate the application with the user's operating system (e.g., adding a desktop shortcut, entry in the start menu, and an uninstaller).

---

## Future Development & Backlog

**Goal:** A collection of ideas and major features that are being considered for versions beyond V2.0.0.

### Potential Features

*   **Advanced Duplicate File Detection:**
    *   Implement a robust system to identify and manage duplicate files, potentially using file hashes instead of just filenames.

*   **"Undo" Functionality:**
    *   A feature to safely revert the last cleaning operation, likely leveraging the data from the Index Manifest.
