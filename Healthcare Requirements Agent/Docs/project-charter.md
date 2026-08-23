# Healthcare Requirements Agent — Project Charter

## 1. Project Purpose

Build a small Azure-based GenAI application that converts unstructured healthcare business requests into structured software requirements.

The project is designed to demonstrate practical experience with RAG, MCP, Azure AI services, structured LLM output, security considerations, and basic observability.

## 2. Problem Statement

Healthcare business requests often begin as incomplete or loosely written descriptions of a desired feature or operational need.

Business analysts and engineers must convert those requests into consistent development artifacts such as:

- User stories
- Acceptance criteria
- Technical requirements
- Security considerations
- Test cases

This process can be repetitive and may produce inconsistent results when organizational standards and policies are not applied consistently.

## 3. Project Objective

Create an AI-assisted workflow that:

1. Accepts an unstructured healthcare-related business request.
2. Retrieves relevant organizational policies and standards.
3. Uses retrieved information to ground an LLM response.
4. Generates structured development requirements.
5. Uses at least one MCP-accessible business tool.
6. Records basic application activity for troubleshooting and observability.

## 4. Target User

Primary users:

- Business Analyst
- Product Owner
- Requirements Analyst
- Software Engineer

## 5. Example Business Scenario

A user submits:

> Members are contacting customer service because they do not understand why their insurance claims were denied. We want members to be able to view the denial reason through the member portal.

The Healthcare Requirements Agent should use relevant policies and standards to generate structured development requirements.

## 6. Expected Output

The application should generate:

- User story
- Acceptance criteria
- Functional requirements
- Security and privacy considerations
- Test cases
- References to relevant retrieved policies

## 7. Core Technologies

- Python
- Microsoft Azure
- Azure OpenAI / Microsoft Foundry
- Azure AI Search
- Model Context Protocol (MCP)
- Azure Container Apps
- Azure Key Vault
- Application Insights / Log Analytics
- GitHub

## 8. Data

The project will use only synthetic, fictional, or publicly available healthcare data.

No real patient information, PHI, member data, or production healthcare information will be used.

Potential data sources include:

- CMS synthetic claims data
- Synthea-generated healthcare records
- Fictional internal policies created specifically for the lab

## 9. In Scope

- One primary business workflow
- One LLM
- Small healthcare knowledge base
- RAG-based document retrieval
- Structured LLM output
- One MCP server
- At least one MCP tool
- Azure-hosted AI services
- Basic secret management
- Basic logging and observability
- Basic functional testing
- Architecture documentation
- GitHub portfolio documentation

## 10. Out of Scope

- Real PHI
- Production HIPAA compliance certification
- Multi-agent architecture
- Long-term agent memory
- Model fine-tuning
- Full Jira integration
- Enterprise authentication system
- Kubernetes
- Production-scale databases
- Complex CI/CD pipelines
- Production deployment at enterprise scale

## 11. Security Principles

The application will demonstrate:

- No hard-coded credentials
- Secure handling of Azure secrets
- Separation between retrieved knowledge and executable tools
- Restricted tool capabilities
- No use of real PHI
- Awareness of prompt injection and unauthorized tool invocation risks
- Basic audit and application logging

## 12. Success Criteria

The project is successful when:

1. A user can submit an unstructured healthcare business request.
2. Azure AI Search retrieves relevant policy information.
3. The LLM uses the retrieved information to generate grounded requirements.
4. The response follows a consistent structured format.
5. The application successfully interacts with at least one MCP tool.
6. Application activity can be inspected through basic Azure logging.
7. The completed project can be clearly explained through its GitHub documentation.

## 13. Deliverables

- Working Healthcare Requirements Agent
- Source code
- Synthetic knowledge documents
- MCP server and tool
- Architecture diagram
- Screenshots
- Test examples
- Project charter
- README
- Security notes
- Cost notes

## 14. Time Constraint

Target build time: approximately **8 hours**.

If a feature threatens the time limit without materially improving the learning or portfolio value of the project, it will be simplified or removed.

## 15. Project Definition of Done

The project is considered complete when a reviewer can:

1. Understand the business problem from the README.
2. Understand the architecture from the diagram.
3. Submit a sample business request.
4. Observe relevant information being retrieved.
5. Receive structured, grounded requirements.
6. See at least one MCP-based tool interaction.
7. Review basic tests and logging evidence.
8. Understand the security and cost decisions made during the project.
