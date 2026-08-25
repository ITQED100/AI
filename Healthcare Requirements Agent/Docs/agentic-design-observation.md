# Agentic Design Observation

## Initial Implementation

The first tool-calling implementation exposed only one tool:

- `get_requirements_template()`

The model was also explicitly instructed to call that tool when creating software requirements.

## Observation

Although the model produced a function call, there was very little real decision-making involved because:

- only one tool was available
- the prompt strongly directed the model to use it

This is best described as minimally agentic behavior.

## Design Improvement

To demonstrate meaningful tool selection, the agent should be given multiple tools with distinct purposes, for example:

- `get_requirements_template()`
- `get_security_requirements()`
- `get_policy_context()`

The model can then choose which tool or tools are appropriate for a given request.

## Engineering Lesson

Tool availability alone does not make a system strongly agentic.

A stronger agentic design allows the model to select among multiple valid actions based on the task and context.

For safety-critical healthcare decisions, deterministic application logic should still enforce authorization and access control rather than delegating those decisions to the model.
