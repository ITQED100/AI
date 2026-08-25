import os
import requests
from openai import OpenAI

question = "Can a member view another member's claim?"

search_endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
search_key = os.environ["AZURE_SEARCH_KEY"]

search_url = (
    f"{search_endpoint}/indexes/healthcare-rag/docs/search"
    "?api-version=2024-07-01"
)

search_headers = {
    "Content-Type": "application/json",
    "api-key": search_key
}

search_body = {
    "count": True,
    "select": "title,chunk",
    "vectorQueries": [
        {
            "kind": "text",
            "text": question,
            "fields": "text_vector",
            "k": 3
        }
    ]
}

search_response = requests.post(
    search_url,
    headers=search_headers,
    json=search_body
)

search_response.raise_for_status()

results = search_response.json()["value"]

context = "\n\n".join(
    f"Source: {result['title']}\n{result['chunk']}"
    for result in results
)

client = OpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"]
)

prompt = f"""
Answer the user's question using only the provided company policy context.

If the answer is not supported by the context, say that the available policies
do not provide enough information.

User question:
{question}

Company policy context:
{context}
"""

response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt
)

print(response.output_text)
