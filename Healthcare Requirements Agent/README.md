# Healthcare Requirements Agent

## Overview
AI-assisted healthcare requirements lab using Azure Foundry, Azure AI Search, RAG, and tool calling.

## Architecture
Business request
→ Azure AI Search retrieves relevant policy context
→ GPT-4.1-mini selects an appropriate tool
→ Python executes the tool
→ Model generates grounded requirements
→ Each requirement is traceable to source policy

## Demonstrated Capabilities
- Baseline model response without RAG
- Vector retrieval from healthcare policy documents
- Grounded RAG responses
- Multiple tool selection
- Requirements generation
- Security/privacy requirements generation
- Test-case generation
- Per-requirement source traceability

## Validation Findings
During testing, the model initially added plausible but unsupported security requirements.

The implementation was corrected by:
- tightening grounding instructions
- applying instructions to the final model call
- requiring source references for each requirement
- rerunning the same test to verify the fix

See `Docs/grounding-validation-note.md`.

## Security
Secrets are stored in environment variables and are not committed to the repository.

## Status
Lab implementation complete.
