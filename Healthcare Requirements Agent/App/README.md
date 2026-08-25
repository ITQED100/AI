# Application

This folder contains the Python scripts used to test and demonstrate the Healthcare Requirements Agent.

## Files

### `test_model.py`

Tests the direct connection to the deployed `gpt-4.1-mini` model in Azure Foundry.

This script demonstrates the baseline model response before retrieval-augmented generation is added.

### `rag_test.py`

Demonstrates retrieval-augmented generation using Azure AI Search.

The script:

1. Sends the user question to Azure AI Search.
2. Retrieves the top relevant policy chunks.
3. Combines the retrieved content into context.
4. Sends the question and policy context to `gpt-4.1-mini`.
5. Returns a grounded response based on the retrieved policies.

### `requirements_tool.py`

Contains reusable Python functions that provide structured templates for:

- Complete software requirements
- Security and privacy requirements
- Test cases

These functions are exposed to the model as callable tools.

### `agent_test.py`

Demonstrates the complete agent workflow.

The script:

1. Retrieves relevant policy context using Azure AI Search.
2. Provides multiple tools to the model.
3. Allows the model to select the tool that best matches the user's request.
4. Executes the selected Python function.
5. Returns the tool result to the model.
6. Generates a human-readable requirements document.
7. Requires generated requirements to remain grounded in retrieved policy sources.

## Tool Selection

The current implementation demonstrates three tool-selection paths:

- Complete requirements request  
  → `get_requirements_template()`

- Security or privacy request  
  → `get_security_requirements()`

- Testing or validation request  
  → `get_test_case_template()`

## Configuration

The scripts use environment variables for Azure service configuration and credentials.

Expected variables include:

- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_SEARCH_ENDPOINT`
- `AZURE_SEARCH_KEY`

Secrets are not stored directly in the Python source files.

## Current Purpose

These scripts are lab and portfolio code intended to demonstrate:

- Azure Foundry model integration
- Azure AI Search
- Vector retrieval
- RAG grounding
- Tool calling
- Agentic tool selection
- Requirements generation
- Policy traceability
- Security and privacy validation
