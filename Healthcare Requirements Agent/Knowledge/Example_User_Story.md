# Example User Story

## Business Request

Members need a way to view the current status of a submitted claim without contacting customer service.

## Business Request Summary

Members currently rely on customer service to determine the status of submitted claims. The requested capability is a self-service claim status view within the member portal.

## User Story

As a health plan member,  
I want to view the current status of my submitted claim,  
so that I can understand where the claim is in the processing lifecycle without contacting customer service.

## Acceptance Criteria

1. The member must be authenticated before claim information is displayed.

2. The application must verify that the requested claim belongs to the authenticated member.

3. The application must display the current claim status from the authoritative claims system.

4. The application must display a clear error message if claim status cannot be retrieved.

5. Sensitive claim information must not be written to application logs.

## Functional Requirements

1. The application must accept a claim identifier.

2. The application must retrieve the current claim status from the claims data source.

3. The application must verify member ownership before returning claim information.

4. The application must display the claim identifier and current status.

5. The application must handle unavailable or invalid claim data without generating or guessing a status.

## Security and Privacy Considerations

- Require authentication before accessing claim data.
- Perform server-side authorization checks.
- Restrict members to their own claims.
- Minimize sensitive data displayed to the user.
- Avoid storing sensitive claim details in application logs.

## Test Cases

1. Authenticated member successfully views the status of their own claim.

2. Authenticated member attempts to view another member's claim and access is denied.

3. Unauthenticated user attempts to access claim information and is denied.

4. Member submits an invalid claim identifier and receives an appropriate error.

5. Claims data source is unavailable and the application returns an error without inventing a claim status.

6. Application logs are reviewed to verify that sensitive claim information was not recorded.

## Source References

- Authentication Standard
- Member Privacy Policy
- Secure Logging Standard
