# Secure Logging Standard

## Purpose

This standard defines logging requirements for applications that process member, claims, and other sensitive healthcare information.

## Logging Requirements

1. Applications should record operational and security events needed for troubleshooting, monitoring, and auditing.

2. Logs must not contain sensitive healthcare information, full claim details, authentication credentials, access tokens, secrets, or passwords.

3. Applications should log important events such as:
   - Successful and failed authentication attempts
   - Authorization failures
   - Application errors
   - External service failures
   - AI or search service failures
   - MCP tool invocation success or failure

4. Logs should contain enough information to support troubleshooting without exposing sensitive business or member data.

5. Where possible, applications should use non-sensitive identifiers such as correlation IDs or request IDs to trace activity across services.

6. Error logs should record technical failure details while avoiding unnecessary member information.

7. Access to application logs should be restricted to authorized personnel.

8. Logging failures should not expose sensitive information to the end user.

## AI Application Logging

For AI-enabled applications, logs may include:

- Request timestamp
- Request or correlation ID
- Retrieval success or failure
- Number of documents retrieved
- Model invocation status
- MCP tool name
- Tool execution status
- Response latency

Prompts and model responses containing sensitive information should not be logged by default.

## Acceptable Log Example

RequestId=8F42A  
Event=ClaimsPolicyRetrieval  
DocumentsRetrieved=3  
Status=Success

## Unacceptable Log Example

Member=Jane Smith  
Claim=CLM-10042  
Diagnosis=Diabetes  
DenialReason=Treatment not medically necessary

## Example Business Rule

The application may record that claim information was successfully retrieved, but it must not record the member's sensitive claim content in the application log.
