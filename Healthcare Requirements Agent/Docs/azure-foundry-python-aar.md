# AAR — Azure Foundry Python Connection

## Objective

Run `test_model.py` locally on macOS and successfully call the deployed `gpt-4.1-mini` model in Microsoft Foundry.

## Environment

* macOS
* Python 3.13.2
* pip 24.3.1
* OpenAI Python package
* Microsoft Foundry
* `gpt-4.1-mini`
* Environment variables used for endpoint and API key

## Error 1 — API Key Not Visible to Python

The first execution failed with:

```text
KeyError: 'AZURE_OPENAI_API_KEY'
```

### Cause

The API key and endpoint existed as shell variables, but they had not been exported.

The shell could display the values with `echo`, but child processes such as Python could not inherit them.

### Fix

Export the existing variables:

```bash
export AZURE_OPENAI_API_KEY
export AZURE_OPENAI_ENDPOINT
```

Verify that Python can see the API key without printing the actual secret:

```bash
python3 -c 'import os; print("key set" if os.getenv("AZURE_OPENAI_API_KEY") else "key missing")'
```

Expected result:

```text
key set
```

## Error 2 — Missing API Version

After exporting the variables, the Python process successfully reached Azure but returned:

```text
openai.BadRequestError:
Missing required query parameter: api-version
```

### Observation

This was progress.

The problem had moved from the local environment layer to the Azure API layer.

Python could now access the credentials and send a request to Azure.

## Attempted Fix — AzureOpenAI Client

The script was temporarily changed to use:

```python
from openai import AzureOpenAI
```

and an explicit API version:

```python
api_version="2024-10-21"
```

The request then returned:

```text
API version not supported
```

### Lesson

The deployed Microsoft Foundry endpoint was using the newer OpenAI v1 endpoint pattern rather than the older dated Azure OpenAI API-version pattern.

The `AzureOpenAI` approach was therefore not appropriate for this endpoint configuration.

## Error 3 — Wrong Endpoint Type

The next troubleshooting step was to inspect the endpoint stored in the environment variable without exposing the API key.

Command:

```bash
python3 -c 'import os; from urllib.parse import urlparse; u=urlparse(os.environ["AZURE_OPENAI_ENDPOINT"]); print("HOST:", u.netloc); print("PATH:", u.path)'
```

Result:

```text
HOST: foundry-healthcare-requirements-agent.services.ai.azure.com
PATH: /api/projects/proj-healthcare-requirements-agent
```

### Root Cause

The environment variable contained the Microsoft Foundry **project endpoint**:

```text
/api/projects/proj-healthcare-requirements-agent
```

The OpenAI client required the **OpenAI v1 endpoint**:

```text
/openai/v1/
```

## Final Fix

Update the environment variable to the correct OpenAI v1 endpoint:

```bash
export AZURE_OPENAI_ENDPOINT="https://foundry-healthcare-requirements-agent.services.ai.azure.com/openai/v1/"
```

Verify the endpoint path:

```bash
python3 -c 'import os; from urllib.parse import urlparse; print(urlparse(os.environ["AZURE_OPENAI_ENDPOINT"]).path)'
```

Expected result:

```text
/openai/v1/
```

## Working Code

```python
import os
from openai import OpenAI

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
api_key = os.environ["AZURE_OPENAI_API_KEY"]

client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Members want to see why their claim was denied."
)

print(response.output_text)
```

## Successful Execution

The script was executed with:

```bash
python3 test_model.py
```

The model returned a valid natural-language response explaining possible claim-denial information for members.

This confirmed successful communication between:

```text
Local Python
    ↓
Environment variables
    ↓
Microsoft Foundry OpenAI v1 endpoint
    ↓
gpt-4.1-mini deployment
    ↓
Model response
```

## Troubleshooting Flow

```text
Run test_model.py
        ↓
KeyError: API key missing
        ↓
Export environment variables
        ↓
Python can access credentials
        ↓
400: Missing api-version
        ↓
Try AzureOpenAI client
        ↓
400: API version unsupported
        ↓
Inspect endpoint
        ↓
Discover Foundry project endpoint
        ↓
Replace with /openai/v1/
        ↓
Run test_model.py again
        ↓
SUCCESS
```

## Key Lessons

1. A shell variable is not automatically available to child processes such as Python unless it is exported.

2. Microsoft Foundry exposes different endpoint types for different purposes.

3. A Foundry project endpoint and an OpenAI model endpoint are not interchangeable.

4. The OpenAI v1 endpoint uses a different API pattern from older Azure OpenAI deployments that require dated `api-version` parameters.

5. Error progression is useful during troubleshooting. Moving from a local `KeyError` to an Azure HTTP error indicated that the request had advanced to a deeper layer of the stack.

6. Troubleshooting should proceed layer by layer:

```text
Local environment
→ Python process
→ Credentials
→ Endpoint
→ API format
→ Model deployment
→ Response
```

7. API keys should not be hard-coded into source code or committed to GitHub.
