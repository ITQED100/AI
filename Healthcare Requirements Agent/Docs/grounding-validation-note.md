# Grounding Validation Note

## Purpose

This note documents a grounding issue discovered during testing of the Healthcare Requirements Agent and the changes made to correct it.

## Issue Identified

During testing, the agent correctly selected the security requirements tool but generated several security requirements that were not explicitly supported by the retrieved company policy context.

Examples included:

- Multi-factor authentication
- Specific TLS implementation guidance
- Exact audit log fields such as member ID, timestamp, and access outcome
- Breach investigation requirements
- Additional security best practices not stated in the source policies

These recommendations were reasonable from a general security perspective, but they were not directly traceable to the retrieved policy documents.

## Why This Matters

The goal of the agent is to generate requirements based on authoritative company policies.

A requirement that sounds reasonable is not necessarily a valid requirement if it is not supported by the source material.

For a healthcare requirements workflow, traceability is important because generated requirements may influence security, privacy, access control, and compliance decisions.

## Root Cause

The initial grounding instructions told the model not to invent unsupported requirements.

However, the final requirements were generated during a second model call after the tool was executed.

The grounding instructions were not explicitly included in that second call.

As a result, the model sometimes expanded the policy content using general security knowledge.

## Changes Made

The following changes were implemented:

1. The grounding instructions were also passed to the final model call.

2. The model was instructed to include only requirements directly supported by retrieved policy context.

3. General industry best practices and implementation assumptions were prohibited unless explicitly present in the source material.

4. Every generated requirement was required to include the name of the supporting source document.

5. Requirements without an identifiable supporting source were instructed to be omitted.

## Validation Test

The same security and privacy request was executed again after the changes.

The agent selected:

`get_security_requirements`

The final output included a source reference for every requirement, such as:

- Members must be authenticated before viewing claim denial information.  
  Source: Claims_Denial_Policy.md, Example_User_Story.md

- Members may only access claim denial information associated with their own account.  
  Source: Claims_Denial_Policy.md, Member_Privacy_Policy.md, Example_User_Story.md

- Sensitive healthcare or member information must not be written to application logs, debugging output, or error messages.  
  Source: Claims_Denial_Policy.md, Member_Privacy_Policy.md, Example_User_Story.md

The previously unsupported additions, such as MFA requirements and specific audit log fields, were no longer included.

## Result

- Tool selection: PASS
- Relevant policy retrieval: PASS
- Requirement traceability: PASS
- Grounding against retrieved policy context: PASS

## Lesson Learned

Prompt instructions alone are not sufficient for reliable requirements grounding.

A stronger design combines:

- Retrieval from authoritative sources
- Explicit grounding instructions
- Source traceability
- Application-level validation
- Repeatable testing against expected requirements

For high-impact workflows, the system should prefer traceable requirements over plausible but unsupported recommendations.
