# Documentation

This folder contains project documentation, design notes, validation findings, and lessons learned from the Healthcare Requirements Agent lab.

## Documents

### Healthcare Requirements Agent - Project Charter

Defines the project objective, scope, expected capabilities, and lab goals.

### Grounding Validation Note

Documents a grounding defect discovered during testing, the root cause, the corrective changes, and the validation results.

See:

[Grounding Validation Note](grounding-validation-note.md)

## Documentation Purpose

The documentation in this folder captures not only what was built, but also how the design evolved during testing.

Key themes include:

- Retrieval-augmented generation (RAG)
- Tool selection
- Requirements traceability
- Security and privacy validation
- Grounding against authoritative policy sources
- Lessons learned during implementation

## Key Engineering Lesson

Generated requirements should not be accepted simply because they sound reasonable.

For this lab, requirements were validated against retrieved policy context and adjusted so that each requirement could be traced back to an authoritative source.
