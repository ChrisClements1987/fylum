# Folder Cleaner Roadmap

This document outlines the development roadmap for the Folder Cleaner application, from its current state to the target V1.0.0 release.

## Current State (Pre-release)

The application is currently a single Python script with the following features:

- **File Organization:** Moves files from the user's `Downloads` folder into subdirectories based on file type.
- **Recursive Processing:** Scans all subdirectories within the `Downloads` folder.
- **Predefined Categories:** Uses a hardcoded list of file extensions and corresponding destination folders.
- **Logging:** Creates a log file that records all file movements and errors.
- **Error Handling:** Handles cases where files are in use and avoids reprocessing already cleaned files.

## V1.0.0 Target State

The goal for V1.0.0 is to evolve the script into a robust, user-friendly, and distributable application. This will be achieved through the following epics, features, and user stories.

---

### Epic 1: Core Cleaning Engine

**Goal:** To create a powerful and flexible cleaning engine that can handle a variety of scenarios.

**Features:**

- **Duplicate File Detection:** The ability to identify and handle duplicate files.
- **"Undo" Functionality:** The ability to revert the last cleaning operation.
- **Customizable Cleaning Rules:** The ability to define custom rules for how files are organized.

**User Stories:**

- *As a user, I want to be able to find and delete duplicate files so that I can free up disk space.*
- *As a user, I want to be able to undo a cleaning operation so that I can easily recover a file if it was moved by mistake.*
- *As a user, I want to be able to define my own rules for how files are organized so that I can customize the cleaning process to my specific needs.*

---

### Epic 2: User Configuration

**Goal:** To allow users to easily configure the application to their needs.

**Features:**

- **Configuration File:** A user-editable file for customizing settings.
- **Folder Selection:** The ability to choose which folders to clean.
- **Ignore Lists:** The ability to specify files and folders to ignore.

**User Stories:**

- *As a user, I want to be able to configure the application through a simple text file so that I can easily customize its behavior.*
- *As a user, I want to be able to select which folders the application should clean so that I am not limited to just the `Downloads` folder.*
- *As a user, I want to be able to specify a list of files and folders to ignore so that I can prevent the application from moving important files.*

---

### Epic 3: Usability and Interface

**Goal:** To create a user-friendly and intuitive interface for the application.

**Features:**

- **Graphical User Interface (GUI):** A simple GUI for interacting with the application.
- **Interactive Mode:** The ability to confirm actions before they are taken.
- **Scheduling:** The ability to schedule automatic cleaning.

**User Stories:**

- *As a user, I want to be able to interact with the application through a simple graphical interface so that I don't have to use the command line.*
- *As a user, I want to be prompted for confirmation before the application moves any files so that I have full control over the process.*
- *As a user, I want to be able to schedule the cleaning process to run automatically so that I don't have to manually run the application every time.*

---

### Epic 4: Distribution and Installation

**Goal:** To make the application easy to install and run for non-technical users.

**Features:**

- **Standalone Executable:** A single executable file that can be run without any dependencies.
- **Installer:** An installer that guides the user through the installation process.

**User Stories:**

- *As a user, I want to be able to download and run the application as a single file so that I don't have to install Python or any other dependencies.*
- *As a user, I want to be able to install the application using a simple installer so that it is properly integrated with my operating system (e.g., with a desktop shortcut and an uninstaller).*
