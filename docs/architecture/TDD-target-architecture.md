# Technical Design Document: Fylum Target Architecture

## 1. Introduction

This document describes the target architecture for the Fylum application, focusing on the V1.0.0 CLI tool. The goal is to create a modular, testable, and extensible system that can be easily maintained and evolved.

## 2. Architectural Goals & Constraints

*   **Modularity:** The system should be composed of independent, well-defined components.
*   **Testability:** Each component should be testable in isolation.
*   **Configurability:** The application's behavior should be primarily driven by a user-editable configuration file.
*   **Extensibility:** The architecture should be flexible enough to accommodate future features like a GUI and additional cleaning rules.
*   **Constraint: CLI-First:** The initial version will be a command-line application.
*   **Constraint: Python:** The application will be built using Python.

## 3. High-Level Architecture

This diagram illustrates the main components (containers) of the Fylum system and their interactions.

```mermaid
C4Container
    title Fylum Application Architecture

    Person(user, "User")

    System_Boundary(cli_app, "Fylum CLI Application") {
        Container(cli, "CLI", "Python (Typer/Click)", "The command-line interface for the user.")
        Container(config_loader, "Configuration Loader", "Python", "Loads and validates the config.yaml file.")
        Container(rule_engine, "Rule Engine", "Python", "Processes files based on user-defined rules.")
        Container(file_processor, "File Processor", "Python", "Executes file operations (move, rename).")
        Container(index_writer, "Index Writer", "Python", "Writes the index manifest file.")
    }

    System_Ext(filesystem, "File System")

    Rel(user, cli, "Uses")
    Rel(cli, config_loader, "Uses")
    Rel(cli, rule_engine, "Uses")
    Rel(rule_engine, file_processor, "Uses")
    Rel(file_processor, index_writer, "Uses")

    Rel(config_loader, filesystem, "Reads config.yaml from")
    Rel(rule_engine, filesystem, "Scans files from")
    Rel(file_processor, filesystem, "Moves/renames files on")
    Rel(index_writer, filesystem, "Writes _fylum_index.md to")
```

## 4. Component Breakdown

*   **CLI (Command-Line Interface):**
    *   The main entry point for the user.
    *   Built using a library like `Typer` or `Click`.
    *   Parses command-line arguments and options.
    *   Orchestrates the calls to other components.

*   **Configuration Loader:**
    *   Responsible for finding, reading, and parsing the `config.yaml` file.
    *   Validates the configuration against a defined schema (e.g., using `Pydantic`).
    *   Provides the configuration as a Python object to other components.

*   **Rule Engine:**
    *   Scans the target directories for files.
    *   For each file, it iterates through the user-defined rules from the configuration.
    *   Determines the action to be taken for each file (e.g., which subfolder to move it to, how to rename it).
    *   Passes a list of planned file operations to the `File Processor`.

*   **File Processor:**
    *   Receives a list of file operations from the `Rule Engine`.
    *   Executes the file operations (e.g., `os.rename`, `shutil.move`).
    *   Handles potential errors during file operations (e.g., file in use, permissions error).
    *   Notifies the `Index Writer` of successful operations.

*   **Index Writer:**
    *   Receives information about successful file movements.
    *   Appends entries to the `_fylum_index.md` file in a structured format.

## 5. Data Model

### Configuration (`config.yaml`)

```yaml
# Example config.yaml
target_directories:
  - "~/Downloads"
  - "~/Desktop"

ignore_patterns:
  - ".DS_Store"
  - "*.tmp"

rename_format: "{date:%Y-%m-%d}_{original_filename}"

rules:
  - name: "Images"
    extensions: [".jpg", ".jpeg", ".png", ".gif"]
    destination: "~/Pictures/Fylum/Images"
  - name: "Documents"
    extensions: [".pdf", ".docx", ".xlsx"]
    destination: "~/Documents/Fylum/Documents"
```

### Index Entry (`_fylum_index.md`)

```markdown
| Original Path | New Path | Timestamp |
|---|---|---|
| `~/Downloads/photo.jpg` | `~/Pictures/Fylum/Images/2025-10-07_photo.jpg` | `2025-10-07T10:00:00Z` |
```

## 6. Workflow (Sequence Diagram)

This diagram shows the sequence of events when a user runs the `fylum clean` command.

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant ConfigLoader
    participant RuleEngine
    participant FileProcessor
    participant IndexWriter
    participant FileSystem

    User->>CLI: fylum clean --dir ~/Downloads
    CLI->>ConfigLoader: load_config()
    ConfigLoader->>FileSystem: Read config.yaml
    FileSystem-->>ConfigLoader: Return config content
    ConfigLoader-->>CLI: Return config object

    CLI->>RuleEngine: process_directory(config, dir)
    RuleEngine->>FileSystem: Scan directory
    FileSystem-->>RuleEngine: Return file list
    RuleEngine->>RuleEngine: Apply rules to files
    RuleEngine-->>CLI: Return list of operations

    CLI->>FileProcessor: execute_operations(operations)
    loop for each operation
        FileProcessor->>FileSystem: Move/rename file
        FileSystem-->>FileProcessor: Confirm operation
        FileProcessor->>IndexWriter: log_operation(details)
        IndexWriter->>FileSystem: Append to _fylum_index.md
    end
    FileProcessor-->>CLI: Return results
    CLI-->>User: Print summary
```

## 7. Future Considerations

*   **GUI:** A future GUI application can be built on top of the core logic defined here. The `Rule Engine` and `File Processor` can be packaged as a library that the GUI can call.
*   **Plugin Architecture:** The `Rule Engine` could be designed to allow for plugins, enabling users to add new types of rules or actions without modifying the core application.
