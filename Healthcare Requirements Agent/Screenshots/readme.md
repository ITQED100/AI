# Screenshots

This folder contains visual evidence from the Healthcare Requirements Agent lab.

## 01-baseline-without-rag.png

Shows the initial model response before retrieval-augmented generation was added.

The response was plausible but not grounded in company policy, which demonstrated the need for RAG.

## 02-rag-grounded-response.png

Shows the grounded RAG response after Azure AI Search was connected.

The response uses retrieved policy context and correctly denies access to another member's claim.

## 03-agentic-requirements-markdown.png

Shows structured software requirements generated after tool calling was added.

The model used the requirements template tool and returned the result in a business-readable format instead of raw JSON.

## 04-grounded-security-requirements-with-sources.png

Shows security and privacy requirements generated after grounding controls were tightened.

Each requirement is traceable to one or more retrieved source documents.

## Validation Summary

The screenshots demonstrate the progression from:

Baseline model output  
→ RAG-grounded output  
→ Tool-based requirements generation  
→ Multi-tool selection  
→ Source-traceable requirements
