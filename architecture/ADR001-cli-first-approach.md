# ADR001: CLI-First Approach

**Status:** Accepted

## Context

The project needs a clear direction for the primary user interface to guide initial development. The main goals are to deliver value quickly, provide a tool that can be used by power users and AI agents, and lay a solid foundation for future enhancements. The three main interface ideas considered were:

1.  A script executed directly within the target directory.
2.  A desktop GUI application.
3.  A command-line interface (CLI) tool.

## Decision

We will adopt a CLI-first approach. The initial version of the application (V1.0.0) will be a CLI tool. This tool will encapsulate all the core file organization logic. A GUI is a likely future enhancement but is out of scope for the initial release.

## Consequences

### Positive

*   **Faster Development:** A CLI allows for a more rapid development cycle, focusing on core logic without the overhead of GUI design and implementation.
*   **Automation-Friendly:** A CLI is easily scriptable and can be used by other programs and AI agents, fulfilling a key requirement.
*   **Solid Foundation:** The CLI's core logic can be exposed as a library that a future GUI can use, preventing code duplication.

### Negative

*   **Reduced Accessibility:** A CLI is less approachable for non-technical users compared to a GUI.
*   **Marketing and Adoption:** A GUI can sometimes be easier to market and may have a broader initial appeal.
