import os
import json
import requests
from openai import OpenAI

from requirements_tool import (
    get_requirements_template,
    get_security_requirements,
    get_test_case_template,
)


question = "Create a complete software requirements document for allowing members to view why their claim was denied."


# ----------------------------
# 1. Retrieve policy context
# ----------------------------

search_endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
search_key = os.environ["AZURE_SEARCH_KEY"]

search_url = (
    f"{search_endpoint}/indexes/healthcare-rag/docs/search"
    "?api-version=2024-07-01"
)

search_headers = {
    "Content-Type": "application/json",
    "api-key": search_key,
}

search_body = {
    "select": "title,chunk",
    "vectorQueries": [
        {
            "kind": "text",
            "text": question,
            "fields": "text_vector",
            "k": 3,
        }
    ],
}

search_response = requests.post(
    search_url,
    headers=search_headers,
    json=search_body,
)

search_response.raise_for_status()

results = search_response.json()["value"]

context = "\n\n".join(
    f"Source: {result['title']}\n{result['chunk']}"
    for result in results
)

print("\n--- RETRIEVED POLICY CONTEXT ---\n")
print(context)
print("\n--- END RETRIEVED CONTEXT ---\n")


# ----------------------------
# 2. Create model client
# ----------------------------

client = OpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)


# ----------------------------
# 3. Tell model about our tools
# ----------------------------

tools = [
    {
        "type": "function",
        "name": "get_requirements_template",
        "description": (
            "Use this when the user wants a complete software requirements document."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "get_security_requirements",
        "description": (
            "Use this when the user specifically asks for security, privacy, "
            "authentication, authorization, logging, or data protection requirements."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "get_test_case_template",
        "description": (
            "Use this when the user specifically asks for test cases, validation, "
            "negative testing, security testing, or edge cases."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
]


instructions = """
You are a healthcare requirements engineering assistant.

Use the provided company policy context as the authoritative source.

Choose the tool that best matches the user's request.

Use:
- get_requirements_template for a complete software requirements document
- get_security_requirements for security, privacy, authentication,
  authorization, logging, or data protection requirements
- get_test_case_template for test cases, validation, negative testing,
  security testing, or edge cases

Select exactly one tool that best matches the user's request.

Do not call more than one tool unless the user explicitly asks for
multiple different deliverables.

Only include requirements that are directly supported by the provided policy context.

Do not add general industry best practices, security recommendations,
implementation details, or assumptions unless they are explicitly stated
in the retrieved context.

If a requirement is not supported by the context, omit it.

For every requirement, base the wording on the retrieved policy context.
Do not expand beyond the source material.

For every requirement you include, provide the source document name
that supports it.

Use this format:

- Requirement text
  Source: Document_Name.md

If you cannot identify a supporting source from the retrieved context,
omit the requirement.

Return the final answer as a human-readable requirements document.

Use Markdown headings such as:

## Business Request Summary
## User Story
## Acceptance Criteria
## Functional Requirements
## Security & Privacy Considerations
## Test Cases
## Source References

Use normal sentences and bullet points under the headings.

Do not return JSON, Python dictionaries, braces, brackets,
or quoted field names.

Do not offer additional work or add conversational closing statements
after the requirements document.
"""


user_input = f"""
User request:
{question}

Company policy context:
{context}
"""


# ----------------------------
# 4. Let the model decide
#    whether to call a tool
# ----------------------------

response = client.responses.create(
    model="gpt-4.1-mini",
    instructions=instructions,
    input=user_input,
    tools=tools,
    parallel_tool_calls=False,
)


# ----------------------------
# 5. Execute requested tool
# ----------------------------

tool_outputs = []

for item in response.output:

    if item.type == "function_call":

        if item.name == "get_requirements_template":
            result = get_requirements_template()

        elif item.name == "get_security_requirements":
            result = get_security_requirements()

        elif item.name == "get_test_case_template":
            result = get_test_case_template()

        else:
            continue

        print(f"Tool selected: {item.name}")

        tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(result),
            }
        )


# ----------------------------
# 6. Give tool result back
#    to the model
# ----------------------------

if tool_outputs:

    final_response = client.responses.create(
        model="gpt-4.1-mini",
        previous_response_id=response.id,
        input=tool_outputs,
        instructions=instructions,
    )

    print(final_response.output_text)

else:

    print(response.output_text)
