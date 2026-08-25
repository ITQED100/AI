# Knowledge Base

This folder contains the policy and standards documents used by the Healthcare Requirements Agent as its source of truth.

These files are uploaded to Azure Blob Storage and indexed by Azure AI Search for retrieval-augmented generation (RAG).

## Documents

- `Authentication_Standard.md`
- `Claims_Denial_Policy.md`
- `Member_Privacy_Policy.md`
- `Secure_Logging_Standard.md`
- `Requirements_Template.md`
- `Example_User_Story.md`

## How the Knowledge Base Is Used

When a user submits a request:

1. Azure AI Search retrieves the most relevant policy chunks.
2. The retrieved text is passed to the model as context.
3. The model generates requirements using the retrieved policies as the authoritative source.
4. Generated requirements are required to reference the supporting source documents.

## Purpose

The knowledge base helps reduce unsupported assumptions and improves traceability between business requirements and company policy.
