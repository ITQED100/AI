# Requirements Template

## Purpose

This template defines the standard structure the Healthcare Requirements Agent should use when converting an unstructured business request into development-ready requirements.

## 1. Business Request Summary

Provide a concise summary of the original business request.

The summary should describe:

- What problem is being reported
- Who is affected
- What capability is being requested
- Why the capability is needed

## 2. User Story

Use the following format:

As a [type of user],  
I want [capability],  
so that [business value or outcome].

## 3. Acceptance Criteria

Acceptance criteria should be:

- Specific
- Testable
- Relevant to the requested capability
- Grounded in applicable policies and standards

Each criterion should describe an observable system behavior.

## 4. Functional Requirements

Identify the functional behavior the application must support.

Functional requirements may include:

- Required user actions
- Required system responses
- Data that must be retrieved
- Validation requirements
- Error handling
- External system interactions

## 5. Security and Privacy Considerations

Identify applicable security and privacy requirements.

Consider:

- Authentication
- Authorization
- Data minimization
- Sensitive data exposure
- Logging
- Audit requirements
- Secure error handling

## 6. Test Cases

Generate test cases that validate both expected and unexpected behavior.

Test cases should include:

- Successful workflow
- Authentication failure
- Authorization failure
- Invalid or missing data
- External service failure
- Security or privacy validation

## 7. Source References

List the organizational policies, standards, or other knowledge documents used to generate the requirements.

Do not cite a source unless it contributed to the generated output.

## Output Format

The Healthcare Requirements Agent should return results using this structure:

### Business Request Summary

[Summary]

### User Story

As a [user],  
I want [capability],  
so that [value].

### Acceptance Criteria

1. [Criterion]
2. [Criterion]
3. [Criterion]

### Functional Requirements

1. [Requirement]
2. [Requirement]
3. [Requirement]

### Security and Privacy Considerations

- [Consideration]
- [Consideration]
- [Consideration]

### Test Cases

1. [Test case]
2. [Test case]
3. [Test case]

### Source References

- [Policy or standard]
- [Policy or standard]

## Example Business Rule

Generated requirements must follow this template and should be grounded in the retrieved knowledge documents rather than invented organizational rules.
