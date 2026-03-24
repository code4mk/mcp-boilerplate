# Architecture Decision Records (ADR)

This directory contains the Architecture Decision Records (ADRs) for the **MCP Server Python Template** project. ADRs capture important architectural and technical decisions along with their context, rationale, and consequences.

## What is an ADR?

An Architecture Decision Record is a short document that describes a significant decision made during the development of a project. Each ADR explains **what** was decided, **why** it was decided, and **what trade-offs** were accepted.

ADRs provide a decision log that helps current and future team members understand the reasoning behind key choices — especially when the original decision-makers are no longer available.

## ADR Index

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [001](001-choose-fastmcp.md) | Use FastMCP as the MCP Server Framework | Accepted | 2025-06-01 |
| [002](002-choose-httpx.md) | Use HTTPX as the HTTP Client Library | Accepted | 2026-03-24 |

## How to Create a New ADR

1. Copy the template file:
   ```bash
   cp _docs/adr/ADR-template.md _docs/adr/<number>-<short-title>.md
   ```

2. Follow the numbering convention: `NNN-short-descriptive-title.md`
   - Use zero-padded three-digit numbers: `001`, `002`, `003`, ...
   - Use lowercase kebab-case for titles

3. Fill in all sections of the template:
   - **Context** — Why is this decision needed?
   - **Decision** — What was decided?
   - **Rationale** — Why this option over others?
   - **Consequences** — What are the positive and negative outcomes?
   - **Alternatives Considered** — What else was evaluated?

4. Set the initial status to `Proposed` and update to `Accepted` once approved.

## ADR Lifecycle

Each ADR follows a defined lifecycle:

```
Proposed → Accepted → [ Deprecated | Superseded ]
                   → Rejected
```

| Status | Meaning |
|--------|---------|
| **Proposed** | Decision is under discussion and review |
| **Accepted** | Decision has been approved and is in effect |
| **Rejected** | Decision was considered but not adopted |
| **Deprecated** | Decision is no longer relevant |
| **Superseded** | Decision has been replaced by a newer ADR |

## Guidelines

- **Immutable records**: Once accepted, ADRs should not be modified. If a decision changes, create a new ADR that supersedes the old one.
- **Keep it concise**: ADRs should be readable in a few minutes.
- **Be honest about trade-offs**: Document both the benefits and the risks.
- **Link related ADRs**: Cross-reference related decisions to build a decision graph.

## Template

See [ADR-template.md](ADR-template.md) for the standard ADR format used in this project.

